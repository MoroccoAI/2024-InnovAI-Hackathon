from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import jwt
import hashlib
import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = "PLEASEDONOTTROWSAUSAGEPIZZAAWAY"
ALGORITHM = "HS256"
security = HTTPBearer()

DATABASE_URL_USERS = "sqlite:///./users.db"
DATABASE_URL_WELLS = "sqlite:///./wells.db"

engine_users = create_engine(DATABASE_URL_USERS, connect_args={"check_same_thread": False})
engine_wells = create_engine(DATABASE_URL_WELLS, connect_args={"check_same_thread": False})

SessionLocalUsers = sessionmaker(autocommit=False, autoflush=False, bind=engine_users)
SessionLocalWells = sessionmaker(autocommit=False, autoflush=False, bind=engine_wells)

BaseUsers = declarative_base()
BaseWells = declarative_base()

class User(BaseUsers):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    nationality = Column(String, nullable=False)
    id_number = Column(String, nullable=False)
    city = Column(String, nullable=False)

class Well(BaseWells):
    __tablename__ = "wells"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    nationality = Column(String, nullable=False)
    id_number = Column(String, nullable=False)
    city = Column(String, nullable=False)
    lon = Column(Float, nullable=False)
    lat = Column(Float, nullable=False)
    licensed = Column(Boolean, default=False)
    license_code = Column(String, nullable=True)
    predicted_depth = Column(Float, nullable=False)

BaseUsers.metadata.create_all(bind=engine_users)
BaseWells.metadata.create_all(bind=engine_wells)

def get_db_users():
    db = SessionLocalUsers()
    try:
        yield db
    finally:
        db.close()

def get_db_wells():
    db = SessionLocalWells()
    try:
        yield db
    finally:
        db.close()

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def create_jwt_token(username: str) -> str:
    payload = {
        "sub": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_jwt_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

class UserCreate(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str
    gender: str
    nationality: str
    id_number: str
    city: str

class UserUpdate(BaseModel):
    username: str | None = None  # Optional field for changing username
    first_name: str
    last_name: str
    gender: str
    nationality: str
    id_number: str
    city: str
    password: str  # Current password for verification
    new_password: str | None = None  # Optional field for updating password

class UserLogin(BaseModel):
    username: str
    password: str

class CoordinatesModel(BaseModel):
    lat: float
    lon: float

class LicenseWellRequest(BaseModel):
    lat: float
    lon: float
    predicted_depth: float

current_coordinates = {"lat": None, "lon": None}

@app.post("/signup")
def signup(user: UserCreate, db: SessionLocalUsers = Depends(get_db_users)):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="User already exists")
    
    new_user = User(
        username=user.username,
        hashed_password=hash_password(user.password),
        first_name=user.first_name,
        last_name=user.last_name,
        gender=user.gender,
        nationality=user.nationality,
        id_number=user.id_number,
        city=user.city,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"success": True, "message": "Account created successfully"}

@app.post("/login")
def login(user: UserLogin, db: SessionLocalUsers = Depends(get_db_users)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or db_user.hashed_password != hash_password(user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_jwt_token(user.username)
    return {"success": True, "token": token}

@app.post("/set_coordinates")
async def set_coordinates(coords: CoordinatesModel):
    current_coordinates["lat"] = coords.lat
    current_coordinates["lon"] = coords.lon
    return {"status": "success"}

@app.get("/get_coordinates")
async def get_coordinates():
    return current_coordinates

@app.post("/license_well")
def license_well(
    request: LicenseWellRequest,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db_users: SessionLocalUsers = Depends(get_db_users),
    db_wells: SessionLocalWells = Depends(get_db_wells)
):
    username = decode_jwt_token(credentials.credentials)

    user = db_users.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if request.lat is None or request.lon is None:
        raise HTTPException(status_code=400, detail="Coordinates not set")
    
    new_well = Well(
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        gender=user.gender,
        nationality=user.nationality,
        id_number=user.id_number,
        city=user.city,
        lon=request.lon,
        lat=request.lat,
        licensed=False,
        license_code=None,
        predicted_depth=request.predicted_depth
    )
    db_wells.add(new_well)
    db_wells.commit()
    db_wells.refresh(new_well)
    return {"success": True, "message": "Well licensed", "well_id": new_well.id}
@app.get("/wells/{username}")
def get_wells_by_user(username: str, db: SessionLocalWells = Depends(get_db_wells)):
    wells = db.query(Well).filter(Well.username == username).all()
    if not wells:
        raise HTTPException(status_code=404, detail="No wells found for this user")
    return wells

# Helper function to convert Well model to dictionary format for JSON response
def well_to_dict(well: Well):
    return {
        "id": well.id,
        "lat": well.lat,
        "lon": well.lon,
        "predicted_depth": well.predicted_depth,
        "licensed": well.licensed,
        "license_code": well.license_code,
    }
    
@app.get("/get_user/{username}")
def get_user_info(username: str, db: SessionLocalUsers = Depends(get_db_users)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "gender": user.gender,
        "nationality": user.nationality,
        "id_number": user.id_number,
        "city": user.city,
    }
    
@app.post("/update_user_info/{username}")
def update_user_info(
    username: str,
    user_data: UserUpdate,
    db_users: SessionLocalUsers = Depends(get_db_users),
    db_wells: SessionLocalWells = Depends(get_db_wells),
):
    user = db_users.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify current password
    if user.hashed_password != hash_password(user_data.password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    
    # Check for new username conflict
    if user_data.username and user_data.username != username:
        if db_users.query(User).filter(User.username == user_data.username).first():
            raise HTTPException(status_code=400, detail="Username already exists")
        user.username = user_data.username

    # Update other user details
    user.first_name = user_data.first_name
    user.last_name = user_data.last_name
    user.gender = user_data.gender
    user.nationality = user_data.nationality
    user.id_number = user_data.id_number
    user.city = user_data.city

    # Update password if provided
    if user_data.new_password:
        user.hashed_password = hash_password(user_data.new_password)

    # Update corresponding wells data
    wells = db_wells.query(Well).filter(Well.username == username).all()
    for well in wells:
        well.username = user_data.username or username  # Update username if changed
        well.first_name = user_data.first_name
        well.last_name = user_data.last_name
        well.gender = user_data.gender
        well.nationality = user_data.nationality
        well.id_number = user_data.id_number
        well.city = user_data.city

    db_users.commit()
    db_wells.commit()
    return {"success": True, "message": "User information updated successfully"}
