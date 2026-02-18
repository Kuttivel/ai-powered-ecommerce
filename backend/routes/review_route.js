import express from "express";
import { createReview, getAllReviews } from "../controllers/review_controller.js";

const router = express.Router();

router.get("/", getAllReviews);
router.post("/", createReview);

export default router;