const API_BASE_URL = "/api";

async function requestJson(path, options = {}) {
    const response = await fetch(`${API_BASE_URL}${path}`, {
        headers: {
            "Content-Type": "application/json",
            ...(options.headers || {}),
        },
        ...options,
    });

    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
        throw new Error(data.message || "Request failed.");
    }

    return data;
}

export async function getProducts(params = {}) {
    const query = new URLSearchParams();

    Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined && value !== null && value !== "") {
            query.set(key, value);
        }
    });

    const queryString = query.toString();
    return requestJson(`/products${queryString ? `?${queryString}` : ""}`);
}

export async function getProductById(productId) {
    return requestJson(`/products/${productId}`);
}

export async function getVisibleReviews(productId) {
    const queryString = productId ? `?productId=${encodeURIComponent(productId)}` : "";
    return requestJson(`/reviews/visible${queryString}`);
}

export async function createReview(reviewPayload) {
    return requestJson("/reviews", {
        method: "POST",
        body: JSON.stringify(reviewPayload),
    });
}

export async function sendChatMessage(chatPayload) {
    return requestJson("/chat", {
        method: "POST",
        body: JSON.stringify(chatPayload),
    });
}