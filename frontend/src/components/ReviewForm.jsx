import { useState } from "react";
import { createReview } from "../lib/api.js";

export function ReviewForm({ productId, onReviewCreated }) {
    const [review_text, set_review_text] = useState("");
    const [rating, set_rating] = useState("5");
    const [submitting, set_submitting] = useState(false);
    const [message, set_message] = useState("");

    async function handleSubmit(event) {
        event.preventDefault();

        if (!review_text.trim()) {
            set_message("Please enter your review text.");
            return;
        }

        try {
            set_submitting(true);
            set_message("");

            const data = await createReview({
                productId,
                reviewText: review_text.trim(),
                rating: Number(rating),
            });

            if (data.review?.isFake) {
                set_message("Your review was submitted and flagged by the AI moderation check, so it is hidden from public reviews.");
            }
            else {
                set_message("Review submitted successfully.");
            }

            set_review_text("");
            set_rating("5");
            onReviewCreated?.(data.review);
        } catch (error) {
            set_message(error.message || "Unable to submit review.");
        } finally {
            set_submitting(false);
        }
    }

    return (
        <section className="review_panel">
            <h3>Leave a review</h3>
            <form className="review_form" onSubmit={handleSubmit}>
                <label>
                    <span>Rating</span>
                    <select value={rating} onChange={(event) => set_rating(event.target.value)}>
                        <option value="5">5</option>
                        <option value="4">4</option>
                        <option value="3">3</option>
                        <option value="2">2</option>
                        <option value="1">1</option>
                    </select>
                </label>

                <label>
                    <span>Review text</span>
                    <textarea
                        rows="4"
                        value={review_text}
                        onChange={(event) => set_review_text(event.target.value)}
                        placeholder="Write your review here"
                        required
                    />
                </label>

                <button className="primary_button" type="submit" disabled={submitting}>
                    {submitting ? "Submitting..." : "Post review"}
                </button>
            </form>
            {message ? <p className="status_text">{message}</p> : null}
        </section>
    );
}