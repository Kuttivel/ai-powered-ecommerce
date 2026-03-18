import Product from "../models/Product.js";
import { formatProductResponse } from "../utils/product_helper.js";

export async function getProducts(req, res) {
    try {
        const { category, search, limit = "24", page = "1" } = req.query;
        const query = {};

        if (category) {
            query.category = new RegExp(`^${escapeRegex(category)}$`, "i");
        }

        if (search && String(search).trim() !== "") {
            const searchRegex = new RegExp(escapeRegex(String(search).trim()), "i");
            query.$or = [
                { name: searchRegex },
                { description: searchRegex },
                { category: searchRegex },
                { brand: searchRegex },
                { tags: searchRegex },
            ];
        }

        const safeLimit = Math.min(Math.max(Number(limit) || 24, 1), 60);
        const safePage = Math.max(Number(page) || 1, 1);
        const skip = (safePage - 1) * safeLimit;

        const [products, total] = await Promise.all([
            Product.find(query).sort({ name: 1, _id: -1 }).skip(skip).limit(safeLimit).lean(),
            Product.countDocuments(query),
        ]);

        res.status(200).json({
            products: products.map(formatProductResponse),
            pagination: {
                page: safePage,
                limit: safeLimit,
                total,
                totalPages: Math.max(Math.ceil(total / safeLimit), 1),
            },
        });
    }
    catch (error) {
        console.error("Error in getProducts controller", error.message);
        res.status(500).json({ message: "Internal server error." });
    }
}

export async function getProductById(req, res) {
    try {
        const { productId } = req.params;
        const product = await Product.findById(productId).lean();

        if (!product) {
            return res.status(404).json({ message: "Product not found." });
        }

        res.status(200).json({ product: formatProductResponse(product) });
    } catch (error) {
        console.error("Error in getProductById controller", error.message);
        res.status(500).json({ message: "Internal server error." });
    }
}

function escapeRegex(value) {
    return String(value).replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}