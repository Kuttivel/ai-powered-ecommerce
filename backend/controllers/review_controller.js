import Review from "../models/Review.js";
import axios from "axios";

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
        const {reviewerId, productId, reviewText, rating} = req.body;

        if(!reviewText) {
            return res.status(400).json({ message: "Review text is required" });
        }

        const aiResponse = await axios.post("http://localhost:5001/predict", {reviewText});

        const { isFake, confidenceScore } = aiResponse.data;

        const newReview = await Review.create({reviewerId,
                                               productId,   
                                               reviewText,
                                               rating,
                                               isFake,
                                               confidenceScore,
                                               aiModel: "LogisticRegression"});

        res.status(201).json({ message: "Review added successfully & analysed.", 
                               added_review: newReview })
    } catch (error) {
        
        console.error(`Error in createReview controller ${error}`);

        res.status(500).json({ message: "Internal server error" });
    }
}