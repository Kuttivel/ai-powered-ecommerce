import mongoose from "mongoose";

const reviewSchema = new mongoose.Schema(
    {
        reviewerId: {
            type: String,
            default: "_uel",
        },
        productId: {
            type: String,
            default: "test_product",
        },
        reviewText: {
            type: String,
            required: true,
        },
        rating: {
            type: Number,
            required: true,
            min: 1,
            max: 5,
        },
        reviewDate: {
            type: Date,
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
        aiPredictionCode: {
            type: Number,
            default: null,
        },
        aiPredictionLabel: {
            type: String,
            default: null,
        },
        probFake: {
            type: Number,
            default: null,
        },
        probReal: {
            type: Number,
            default: null,
        },
        predictedAt: {
            type: Date,
            default: null,
        },
        moderationStatus: {
            type: String,
            default: "pending",
        },
    },

    {
        timestamps: true,
    }
);

const Review = mongoose.models.Review || mongoose.model("Review", reviewSchema);

export default Review;