import axios from "axios";
import Review from "../models/Review.js";

const AI_URL = process.env.AI_URL || "http://localhost:5001";

export async function getAllReviews(req, res) {
    try {
        const query = {};

        if (req.query.productId) {
            query.productId = String(req.query.productId);
        }

        const reviews = await Review.find(query).sort({ createdAt: -1 }).lean();
        res.status(200).json({ reviews });
    }
    catch (error) {
        console.error("Error in getAllReviews controller", error.message);
        res.status(500).json({ message: "Internal server error." });
    }
}

export async function createReview(req, res) {
    try {
        const { reviewerId, productId, reviewText, rating, reviewDate } = req.body;
        const numericRating = Number(rating);

        switch (true) {
            case typeof productId !== "string" || productId.trim() === "":
                return res.status(400).json({ message: "productId is required." });
            case typeof reviewText !== "string":
                return res.status(400).json({ message: "reviewText must be a string." });
            case reviewText.trim() === "":
                return res.status(400).json({ message: "reviewText is required." });
            case rating === undefined || rating === null:
                return res.status(400).json({ message: "rating is required." });
            case Number.isNaN(numericRating) || !Number.isInteger(numericRating):
                return res.status(400).json({ message: "rating must be an integer." });
            case numericRating < 1 || numericRating > 5:
                return res.status(400).json({ message: "rating must be between 1 and 5." });
        }

        const newReview = new Review({
            reviewerId: typeof reviewerId === "string" && reviewerId.trim() !== "" ? reviewerId.trim() : "User",
            productId: productId.trim(),
            reviewText: reviewText.trim(),
            rating: numericRating,
            reviewDate: reviewDate || new Date(),
            moderationStatus: "pending",
        });

        try {
            const ai_response = await axios.post(`${AI_URL}/api/feature-1/predict`, {
                review_text: reviewText.trim(),
                rating: numericRating,
            });

            const aiData = ai_response.data;
            const prediction_code = Number(aiData.prediction_code);
            const prob_fake = Number(aiData.prob_fake);
            const prob_real = Number(aiData.prob_real);
            const confidence_score = Number(aiData.confidence_score);

            if (Number.isFinite(prediction_code)) {
                newReview.aiPredictionCode = prediction_code;
                newReview.aiPredictionLabel = aiData.prediction_label;
                newReview.isFake = prediction_code === 1;
                newReview.predictedAt = new Date();
                newReview.moderationStatus = prediction_code === 1 ? "flagged_fake" : "approved";
            }

            newReview.probFake = Number.isFinite(prob_fake) ? prob_fake : null;
            newReview.probReal = Number.isFinite(prob_real) ? prob_real : null;
            newReview.confidenceScore = Number.isFinite(confidence_score) ? confidence_score : null;
        }
        catch (error) {
            console.error("AI microservice error in createReview controller", error.message);
            newReview.moderationStatus = "ai_unavailable";
        }

        const savedReview = await newReview.save();

        res.status(201).json({
            message: "Review added successfully.",
            review: savedReview,
            visibility: {
                visible: isReviewVisible(savedReview),
                rule: savedReview.isFake ? "Hidden from public reviews because it was flagged as fake." : "Visible in public reviews.",
            },
        });
    }
    catch (error) {
        console.error("Error in createReview controller", error.message);
        res.status(500).json({ message: "Internal server error." });
    }
}

export async function getVisibleReviews(req, res) {
    try {
        const query = {
            $or: [
                { isFake: { $ne: true } },
                { isFake: null },
            ],
        };

        if (req.query.productId) {
            query.productId = String(req.query.productId);
        }

        const reviews = await Review.find(query).sort({ createdAt: -1 }).lean();
        const visibleReviews = reviews.filter((review) => isReviewVisible(review));

        res.status(200).json({ reviews: visibleReviews });
    }
    catch (error) {
        console.error("Error in getVisibleReviews controller", error.message);
        res.status(500).json({ message: "Internal server error." });
    }
}

function isReviewVisible(review) {
    return review?.isFake !== true;
}