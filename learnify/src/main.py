
import config
import llm
import keys
import os

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))


app = FastAPI()
os.environ["OPENAI_API_KEY"] = keys.key

#### --------- Mounting static files to be served at the "/static" endpoint ------------------ ####
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    #### ---------- Serving the static index.html file when the root ("/") is accessed -------------- ####
    return FileResponse('static/index.html')

@app.get("/query")
async def get_query_response(query: str = Query(..., description="Enter your query here")):
    #### ------Creating a QueryRunner object with the document path and model name --------------####
    query_runner = llm.QueryRunner(document_path = config.DOCUMENT_PATH ,model_name=config.MODEL_NAME)

    #### ------ Running the query and getting the response ------------------####
    response = query_runner.run_query(query)

    #### --------  Returning the response as a JSON object -------- ####
    return {"response": response}
