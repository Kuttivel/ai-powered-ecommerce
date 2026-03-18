export function normaliseImageUrl(imageUrl) {
    if (!imageUrl) {
        return "";
    }

    if (Array.isArray(imageUrl)) {
        return String(imageUrl[0] || "").trim();
    }

    const text = String(imageUrl).trim();

    if (text === "") {
        return "";
    }

    if (text.startsWith("[")) {
        try {
            const parsedValue = JSON.parse(text.replace(/'/g, '"'));

            if (Array.isArray(parsedValue) && parsedValue.length > 0) {
                return String(parsedValue[0] || "").trim();
            }
        } catch {
            const matchedUrl = text.match(/https?:\/\/[^\s"'\\\],]+/i);

            if (matchedUrl) {
                return String(matchedUrl[0]).trim();
            }
        }
    }

    return text;
}

export function buildCategorySlug(categoryName) {
    return String(categoryName || "")
        .trim()
        .toLowerCase()
        .replace(/&/g, "and")
        .replace(/[^a-z0-9]+/g, "-")
        .replace(/^-+|-+$/g, "");
}

export function formatProductResponse(product) {
    const categoryName = String(product.category || "").trim();
    const numericPrice = Number(product.price);

    return {
        _id: String(product._id),
        uniq_id: product.uniq_id || "",
        name: product.name || "",
        price: Number.isFinite(numericPrice) ? numericPrice : null,
        priceDisplay:
            product.priceDisplay ||
            (Number.isFinite(numericPrice) ? `£${numericPrice.toFixed(2)}` : "Price unavailable"),
        currency: product.currency || "GBP",
        originalPriceInr: product.originalPriceInr ?? null,
        description: product.description || "",
        category: categoryName,
        categoryPath: product.categoryPath || categoryName,
        categorySlug: buildCategorySlug(categoryName),
        brand: product.brand || "",
        imageUrl: normaliseImageUrl(product.imageUrl),
        rating: product.rating ?? product.overall_rating ?? null,
        overall_rating: product.overall_rating ?? null,
        tags: Array.isArray(product.tags) ? product.tags : [],
        stock: typeof product.stock === "number" ? product.stock : 0,
        createdAt: product.createdAt,
        updatedAt: product.updatedAt,
    };
}