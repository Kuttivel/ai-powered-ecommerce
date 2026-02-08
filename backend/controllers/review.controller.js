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
        const newReview = new Review({reviewerId, 
                                      productId, 
                                      reviewText,
                                      rating});
        
        const savedReview = await newReview.save();

        const aiResponse = await axios.post("http://127.0.0.1:5000/predict-review",{reviewText});

        savedReview.isFake = aiResponse.data.prediction === "FAKE";
        savedReview.confidenceScore = aiResponse.data.confidence;

        await savedReview.save();

        res.status(201).json({ message: "Review added successfully & analysed.", 
                               added_review: savedReview })
    } catch (error) {
        
        console.error(`Error in createReview controller ${error}`);

        res.status(500).json({ message: "Internal server error" });
    }
}