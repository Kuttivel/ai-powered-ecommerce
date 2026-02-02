import mongoose from "mongoose";

const reviewSchema = new mongoose.Schema(
    {
        reviewerId: {
            type: String,
            required: true,
        },
        productId: {
            type: String,
            required: true,
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
            required: true,
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
        detationType: {
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