import mongoose from "mongoose";

const productSchema = new mongoose.Schema(
    {
        uniq_id: { type: String, index: true },
        name: { type: String, required: true, trim: true },
        price: { type: Number, default: null },
        priceDisplay: { type: String, default: "" },
        currency: { type: String, default: "GBP" },
        originalPriceInr: { type: Number, default: null },
        description: { type: String, default: "" },
        category: { type: String, default: "" },
        categoryPath: { type: String, default: "" },
        brand: { type: String, default: "" },
        imageUrl: { type: String, default: "" },
        rating: { type: Number, default: null },
        overall_rating: { type: Number, default: null },
        tags: { type: [String], default: [] },
        stock: { type: Number, default: 0 },
    },
    {
        collection: "products",
        timestamps: true,
    }
);

const Product = mongoose.models.Product || mongoose.model("Product", productSchema);

export default Product;
