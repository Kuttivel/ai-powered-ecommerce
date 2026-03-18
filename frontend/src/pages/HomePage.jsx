import { useEffect, useState } from "react";
import { getProducts } from "../lib/api.js";
import { ProductGrid } from "../components/ProductGrid.jsx";

export function HomePage() {
    const [products, set_products] = useState([]);
    const [search, set_search] = useState("");
    const [loading, set_loading] = useState(true);
    const [error, set_error] = useState("");

    useEffect(() => {
        loadProducts();
    }, []);

    async function loadProducts(nextSearch = "") {
        try {
            set_loading(true);

            const data = await getProducts(
                nextSearch ? { search: nextSearch, limit: 24 } : { limit: 24 }
            );

            set_products(data.products || []);
            set_error("");
        } catch (load_error) {
            set_error(load_error.message || "Unable to load products.");
        } finally {
            set_loading(false);
        }
    }

    function handleSubmit(event) {
        event.preventDefault();
        loadProducts(search.trim());
    }

    function handleClearSearch() {
        set_search("");
        loadProducts("");
    }

    return (
        <div className="page_content">
            <section className="hero_block">
                <div className="hero_text">
                    <p className="eyebrow_text">Final dissertation scope</p>
                    <h1>Simple AI-powered e-commerce prototype</h1>
                    <p>
                        This project focuses on two implemented features: fake review detection and
                        conversational product search.
                    </p>
                    <div className="hero_points">
                        <span>Feature 1: Fake review detection</span>
                        <span>Feature 3: Conversational product search</span>
                    </div>
                </div>

                <form className="search_form" onSubmit={handleSubmit}>
                    <label>
                        <span>Search products</span>
                        <input
                            type="text"
                            value={search}
                            onChange={(event) => set_search(event.target.value)}
                            placeholder="Search by product or brand"
                        />
                    </label>

                    <div className="search_button_row">
                        <button className="primary_button" type="submit">
                            Search
                        </button>

                        <button className="secondary_button" type="button" onClick={handleClearSearch}>
                            Clear
                        </button>
                    </div>
                </form>
            </section>

            {loading ? <p>Loading products...</p> : null}
            {error ? <p className="status_text">{error}</p> : null}

            {!loading && !error ? (
                <ProductGrid
                    title="Products"
                    products={products}
                />
            ) : null}
        </div>
    );
}