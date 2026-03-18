import { useEffect, useState } from "react";
import { getVisibleReviews } from "../lib/api.js";
import { ReviewForm } from "./ReviewForm.jsx";

export function ReviewSection({ productId }) {
    const [reviews, set_reviews] = useState([]);
    const [loading, set_loading] = useState(true);
    const [error, set_error] = useState("");

    async function loadReviews() {
        try {
            set_loading(true);
            const data = await getVisibleReviews(productId);
            set_reviews(data.reviews || []);
            set_error("");
        }
        catch (load_error) {
            set_error(load_error.message || "Unable to load reviews.");
        }
        finally {
            set_loading(false);
        }
    }

    useEffect(() => {
        loadReviews();
    }, [productId]);

    return (
        <div className="review_layout">
            <ReviewForm
                productId={productId}
                onReviewCreated={() => {
                    loadReviews();
                }}
            />

            <section className="review_panel">
                <h3>Public reviews</h3>
                <p>Reviews flagged as fake by the AI moderation feature are hidden from this public list.</p>

                {loading ? <p>Loading reviews...</p> : null}
                {error ? <p className="status_text">{error}</p> : null}
                {!loading && !reviews.length ? <p>No visible reviews yet.</p> : null}

                <div className="review_list">
                    {reviews.map((review) => (
                        <article className="review_item" key={review._id}>
                            <div className="review_item_top">
                                <strong>{review.reviewerId || "User"}</strong>
                                <span>{review.rating}/5</span>
                            </div>
                            <p>{review.reviewText}</p>
                            <small>{new Date(review.createdAt).toLocaleString()}</small>
                        </article>
                    ))}
                </div>
            </section>
        </div>
    );
}