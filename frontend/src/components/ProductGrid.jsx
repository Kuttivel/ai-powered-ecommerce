import { ProductCard } from "./ProductCard.jsx";

export function ProductGrid({ title, products = [] }) {
    return (
        <section className="section_block">
            <div className="section_heading">
                <h2>{title}</h2>
                <p>{products.length} items shown.</p>
            </div>

            {!products.length ? <p className="status_text">No products found.</p> : null}

            <div className="product_grid">
                {products.map((product) => (
                    <ProductCard key={product._id} product={product} />
                ))}
            </div>
        </section>
    );
}