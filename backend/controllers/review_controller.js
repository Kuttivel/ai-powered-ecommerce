import axios from "axios";
import Review from "../models/Review.js";

const AI_URL = process.env.AI_URL || "http://localhost:5001";


export async function getAllReviews(_, res) {
    try {
        const reviews = await Review.find();
        res.status(200).json(reviews);
    } 
    catch (error) {
        console.error(`Error in getAllReviews controller ${error}`);
        res.status(500).json({ message: "Internal server error" });
    }
}

export async function createReview(req, res) {
try {
    const {reviewerId, productId, reviewText, rating, reviewDate} = req.body;

    switch(true) {
        case (typeof reviewText !== "string"):
            return res.status(400).json({ message: "reviewText must be a string (non-integer)." });
        
        case (reviewText.trim() === ""): 
            return res.status(400).json({ message: "reviewText is required." });

        case (rating === undefined || rating === null):
            return res.status(400).json({ message: "rating is required." });

        case (Number.isNaN(rating) || !Number.isInteger(rating)):
            return res.status(400).json({ message: "rating must be an integer." });

        case (rating < 1 || rating > 5):
            return res.status(400).json({ message: "rating must be between 1 and 5." });
    }


    const newReview = new Review({reviewerId: reviewerId, 
                                  productId: productId, 
                                  reviewText: reviewText,
                                  rating: rating, 
                                  reviewDate: reviewDate});
    
    try {
        const aiResponse = await axios.post(`${AI_URL}/api/feature-1/predict`, {review_text: reviewText, rating: rating});
        
        const aiData = aiResponse.data;

        const predictionCode = Number(aiData.prediction_code);
        const predictionLabel = aiData.prediction_label;
        const probFake = Number(aiData.prob_fake);
        const probReal = Number(aiData.prob_real);
        const confidenceScore = Number(aiData.confidence_score);

        if (Number.isFinite(predictionCode)) {
            newReview.aiPredictionCode = predictionCode;
            newReview.aiPredictionLabel = predictionLabel;
            newReview.isFake = predictionCode === 1;
            newReview.predictedAt = new Date();
        }

        newReview.probFake = Number.isFinite(probFake) ? probFake : null;
        newReview.probReal = Number.isFinite(probReal) ? probReal : null;
        newReview.confidenceScore = Number.isFinite(confidenceScore) ? confidenceScore : null;
    } 
    catch (error) {
        console.error(`AI microservice error in createReview controller ${error}`);
    }

    const savedReview = await newReview.save();
    res.status(201).json({ 
        message: "Review added successfully.",
        review: savedReview,
    })

} 
catch (error) {
    console.error(`Error in createReview controller ${error}`);
    res.status(500).json({ message: "Internal server error" });
}}