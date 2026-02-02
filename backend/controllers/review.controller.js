export function getAllReviews(req, res) {
    res.status(200).send("Reviews here!");
}

export function createReview(req, res) {
    res.status(201).json({message: "Review added successfully!"});
}