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
        source: {
            type: String,
            enum: ["MTURK", "TRIPADVISOR"],
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
        detectionType: {
            type: String,
            enum: ["NLP", "BEHAVIOURAL", "HYBRID"],
            default: null,
        },
    },

    {
        timestamps: true,
    }
);

const Review = mongoose.model("Review", reviewSchema);

export default Review;