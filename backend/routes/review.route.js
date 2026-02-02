import express from "express";

const router = express.Router();

router.get("/", (_, res) => {
    res.status(200).send("Reviews here!");
});

router.post("/a", (_, res) => {
    res.status(201).json({message: "Review added successfully!"});
});

export default router;