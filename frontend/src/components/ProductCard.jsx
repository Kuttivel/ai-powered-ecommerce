import { Link } from "react-router-dom";
import { ImageWithFallback } from "./ImageWithFallback.jsx";

export function ProductCard({ product }) {
    return (
        <article className="product_card">
            <Link className="product_image_link" to={`/products/${product._id}`}>
                <ImageWithFallback
                    src={product.imageUrl}
                    alt={product.name}
                    className="product_image"
                    fallbackClassName="product_image product_image_placeholder"
                />
            </Link>

            <div className="product_content">
                <Link className="product_name" to={`/products/${product._id}`}>
                    {product.name}
                </Link>

                <p className="product_brand">{product.brand || "No brand listed"}</p>

                <div className="product_meta">
                    <span className="product_price">{product.priceDisplay || "Price unavailable"}</span>
                    <span className="product_rating">{product.rating ? `${product.rating}/5` : "No rating"}</span>
                </div>
            </div>
        </article>
    );
}