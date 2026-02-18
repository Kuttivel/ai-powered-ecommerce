import fs from "fs";
import path from "path";
import dotenv from "dotenv";
import Review from "../backend/models/Review.js";
import { connectDataBase } from "../backend/config/database.js";

dotenv.config({path: path.resolve(process.cwd(), "../.env")});

function clean_POS_text(text) {

    const words = [];

    const tokens = text.split(/\s+/);

    for (let token of tokens) {

        if (token.includes("__")) {
            token = token.split("__").pop();
        }
        if (token.includes("/")) {
            token = token.substring(0, token.lastIndexOf("/"));
        }
        if (token.match(/^-(LRB|RRB|LSB|RSB)-$/)) {
            continue;
        }
        if (/^[a-zA-Z]+$/.test(token)) {
            words.push(token);
        }
    }
    const cleaned_words = words.filter((word, index) => {
        return index === 0 || word.toLowerCase() !== words[index - 1].toLowerCase();
    });

    return cleaned_words.join(" ");
} /* 
        clean_POS_text()'s written in order to convert,
            POS tagged text (Part Of Speech) -> readable text.
  */


function read_txt_files(target_folder_path, isFakeReview) {
    const reviews = [];
    const folder = fs.readdirSync(target_folder_path);

    for(const fold of folder) {
        const full_folder_path = path.join(target_folder_path, fold);
        const txt_files = fs.readdirSync(full_folder_path);

        for(const txt_file of txt_files) {
            if(!txt_file.endsWith(".txt")) {
                continue;
            }

            const file_path = path.join(full_folder_path, txt_file);
            let reviewText = fs.readFileSync(file_path, "utf8");

            if(!reviewText || reviewText.trim().length === 0) {
                continue;
            }

            let cleaned_reviewText = clean_POS_text(reviewText);

            reviews.push({
                reviewerId: "P11-1032 Dataset_USER",
                productId: "P11-1032 Dataset_PRODUCT",
                reviewText: cleaned_reviewText,
                rating: null,
                isFake: isFakeReview,
                confidenceScore: null,
                aiModel: "LogisticRegression"
            });
        }
    }

    return reviews;

}

export async function import_review_data() {
    try {
        await connectDataBase();

        await Review.deleteMany({});
        console.log("Existing reviews deleted successfully from MONGODB.");

        const projectRoot = path.resolve(process.cwd(), "../");

        const dataset_path = path.join(projectRoot, 
                                       "datasets", 
                                       "reviews", 
                                       "P11-1032-Datasets");

        const mTurk_folder = path.join(dataset_path, "MTurk");
        const tripAdvisor_folder = path.join(dataset_path, "TripAdvisor");

        console.log("Reading deceptive reviews. .. ...");
        const fakeReviews = read_txt_files(mTurk_folder, true);

        console.log("Reading truthful reviews. .. ...");
        const trueReviews = read_txt_files(tripAdvisor_folder, false);

        const allReviews = [...fakeReviews, ...trueReviews];
        console.log(`Importing ${allReviews.length} reviews.`);

        await Review.insertMany(allReviews);
        console.log("Data imported successfully.");

        process.exit(0);
    } 
    catch (error) {
        console.error("Error importing data:", error.message);
        process.exit(1);
    }
}

import_review_data();