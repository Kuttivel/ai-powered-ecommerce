import express from "express";
import dotenv from "dotenv";
import cors from "cors";

import { connectDataBase } from "./config/database.js";

import productRoutes from "./routes/product_route.js";
import reviewRoutes from "./routes/review_route.js";
import chatRoutes from "./routes/chat_route.js";


dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;
const frontendOrigins = [
    process.env.FRONTEND_URL || "http://localhost:5002",
    "http://localhost:5002",
    "http://localhost:5173",
];


app.use(cors({
    origin: frontendOrigins, 
    credentials: true,
}));
app.use(express.json());

app.get("/health", (_, res) => {
    res.status(200).json({ status: "ok", service: "backend" });
});

app.use("/api/products", productRoutes);
app.use("/api/reviews", reviewRoutes);
app.use("/api/chat", chatRoutes);

// 404 handling
app.use((_, res) => {
    res.status(404).json({ message: "404! Route not found." });
});

// Global error handling
app.use((error, _, res, __) => {
    console.error("Unhandled backend error:", error);
    res.status(500).json({ message: "Internal server error." });
});


async function startServer() {

    await connectDataBase();

    app.listen(PORT, () => {
        console.log(`Server is running on http://localhost:${PORT}`);
    });
}

startServer().catch((error) => {
    console.error("Error starting backend server:", error);
    process.exit(1);
});