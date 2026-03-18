import express from "express";
import { createReview, getAllReviews, getVisibleReviews } from "../controllers/review_controller.js";

const router = express.Router();

router.get("/visible", getVisibleReviews);
router.get("/", getAllReviews);
router.post("/", createReview);

export default router;