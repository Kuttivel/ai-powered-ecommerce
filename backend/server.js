import express from "express";
import dotenv from "dotenv";
import { connectDataBase } from "./config/database.js";


dotenv.config();

const app = express();

const PORT = process.env.PORT || 5000;

connectDataBase();


app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});