import express from "express";
import dotenv from "dotenv";
import { connectDataBase } from "./config/database.js";
import reviewRoutes from "./routes/review_route.js";
import chatRoutes from "./routes/chat_route.js";


dotenv.config();

const app = express();

const PORT = process.env.PORT || 5000;

connectDataBase();

app.use(express.json());

app.use("/api/reviews", reviewRoutes);
app.use("/api/chat", chatRoutes);


app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});