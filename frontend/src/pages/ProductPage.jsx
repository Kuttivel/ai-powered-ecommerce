import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { getProductById } from "../lib/api.js";
import { ImageWithFallback } from "../components/ImageWithFallback.jsx";
import { ReviewSection } from "../components/ReviewSection.jsx";

export function ProductPage() {
    const { productId } = useParams();
    const [product, set_product] = useState(null);
    const [loading, set_loading] = useState(true);
    const [error, set_error] = useState("");

    useEffect(() => {
        loadProduct();
    }, [productId]);

    async function loadProduct() {
        try {
            set_loading(true);
            const data = await getProductById(productId);
            set_product(data.product || null);
            set_error("");
        }
        catch (load_error) {
            set_error(load_error.message || "Unable to load product.");
        }
        finally {
            set_loading(false);
        }
    }

    if (loading) {
        return <div className="page_content"><p>Loading product...</p></div>;
    }

    if (error || !product) {
        return <div className="page_content"><p className="status_text">{error || "Product not found."}</p></div>;
    }

    return (
        <div className="page_content">
            <section className="product_detail_card">
                <div>
                    <div className="breadcrumb_row detail_breadcrumb">
                        <Link to="/">Home</Link>
                        <span>/</span>
                        <span>Product</span>
                    </div>

                    <ImageWithFallback
                        src={product.imageUrl}
                        alt={product.name}
                        className="product_detail_image"
                        fallbackClassName="product_image_placeholder large"
                    />
                </div>

                <div className="product_detail_content">
                    <p className="product_category">{product.category || "General"}</p>
                    <h1>{product.name}</h1>
                    <p className="product_brand">{product.brand || "No brand listed"}</p>

                    <div className="product_detail_meta">
                        <span className="product_price large">{product.priceDisplay || "Price unavailable"}</span>
                        <span>{product.rating ? `${product.rating}/5 rating` : "No rating"}</span>
                    </div>

                    <p className="product_description">
                        {product.description || "No product description available for this item."}
                    </p>

                    {product.tags?.length ? (
                        <div className="tag_row">
                            {product.tags.slice(0, 8).map((tag) => (
                                <span className="tag_chip" key={tag}>{tag}</span>
                            ))}
                        </div>
                    ) : null}
                </div>
            </section>

            <ReviewSection productId={product._id} />
        </div>
    );
}