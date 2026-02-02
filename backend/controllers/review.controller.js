import Review from "../models/Review.js";

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
    const newReview = new Review({reviewerId: reviewerId, 
                                  productId: productId, 
                                  reviewText: reviewText,
                                  rating: rating, 
                                  reviewDate: reviewDate});
    
    await newReview.save();
    res.status(201).json({ message: "Review added successfully." })
} catch (error) {
    
    console.error(`Error in createReview controller ${error}`);

    res.status(500).json({ message: "Internal server error" });
}}