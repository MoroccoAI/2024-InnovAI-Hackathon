// Import dependencies
const express = require("express");
const mongoose = require("mongoose");
const bcrypt = require("bcrypt");
const jwt = require("jsonwebtoken");
const cors = require("cors");

// Initialize the app
const app = express();

// Middleware
app.use(express.json()); // Parse incoming JSON data
app.use(cors()); // Enable CORS for cross-origin requests

// MongoDB connection
mongoose.connect("mongodb://localhost:27017/my_db", {
    useNewUrlParser: true,
    useUnifiedTopology: true,
});

const db = mongoose.connection;
db.on("error", console.error.bind(console, "connection error:"));
db.once("open", () => console.log("Connected to MongoDB"));

// User Schema and Model
const userSchema = new mongoose.Schema({
    username: { type: String, required: true, unique: true },
    email: { type: String, required: true, unique: true },
    password: { type: String, required: true },
});

const User = mongoose.model("User", userSchema);

// Registration Route
app.post("/api/auth/register", async (req, res) => {
    console.log("Register route hit");
    const { username, email, password } = req.body;
    console.log('Registration request received:', { username, email });

    try {
        // Check if the user already exists
        const existingUser  = await User.findOne({ email });
        if (existingUser ) {
            console.log('Registration failed: User already exists');
            return res.status(400).json({ error: "User  already exists" });
        }

        // Hash the password before saving
        const hashedPassword = await bcrypt.hash(password, 10);
        const newUser  = new User({ username, email, password: hashedPassword });

        // Save the new user
        await newUser .save();
        console.log('User  registered successfully:', newUser );
        res.status(201).json({ message: "User  registered successfully" });
    } catch (err) {
        console.error('Error during registration:', err);
        res.status(500).json({ error: "Error registering user", details: err });
    }
});

// Login Route
app.post("/api/auth/login", async (req, res) => {
    console.log("Login route hit");
    const { email, password } = req.body;
    console.log('Login request received:', { email });

    try {
        // Find user by email
        const user = await User.findOne({ email });
        if (!user) {
            console.log('Login failed: User not found');
            return res.status(404).json({ error: "User  not found" });
        }

        // Compare the provided password with the stored hashed password
        const isPasswordValid = await bcrypt.compare(password, user.password);
        if (!isPasswordValid) {
            console.log('Login failed: Invalid credentials');
            return res.status(401).json({ error: "Invalid credentials" });
        }

        // Generate JWT token
        const token = jwt.sign({ userId: user._id }, "secret_key", { expiresIn: "1h" });

        // Send the response with the token
        console.log('Login successful:', { userId: user._id });
        res.json({ message: "Login successful", token });
    } catch (err) {
        console.error('Error during login:', err);
        res.status(500).json({ error: "Error logging in", details: err });
    }
});

// Fetch User (Optional for Testing)
app.get("/api/auth/user/:id", async (req, res) => {
    console.log('Fetch user request received for ID:', req.params.id);
    try {
        const user = await User.findById(req.params.id);
        if (!user) {
            console.log('Fetch user failed: User not found');
            return res.status(404).json({ error: "User  not found" });
        }

        res.json(user);
    } catch (err) {
        console.error('Error fetching user:', err);
        res.status(500).json({ error: "Error fetching user", details: err });
    }
});

// Start server
const PORT = 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
