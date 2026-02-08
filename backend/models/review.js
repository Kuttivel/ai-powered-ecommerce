import mongoose from "mongoose";

const reviewSchema = new mongoose.Schema(
    {
        reviewerId: {
            type: String,
            default: "DATASET_USER",
        },
        productId: {
            type: String,
            default: "DATASET_PRODUCT",
        },
        reviewText: {
            type: String,
            required: true,
        },
        
        rating: {
            type: Number,
            default: null,
            min: 1,
            max: 5,
        },
        reviewDate: {
            type: Date,
            default: Date.now,
        },

        // AI prediction results:
        isFake: {
            type: Boolean,
            default: null,
        },
        confidenceScore: {
            type: Number,
            default: null,
        },
        aiModel: {
            type: String,
            default: "LogisticRegression"
        },
    },

    {
        timestamps: true,
    }
);

const Review = mongoose.model("Review", reviewSchema);

export default Review;