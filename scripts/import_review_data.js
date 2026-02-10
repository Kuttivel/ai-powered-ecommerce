import fs from "fs";
import path from "path";
import dotenv from "dotenv";
import Review from "../backend/models/Review.js";
import { connectDataBase } from "../backend/config/database.js";

dotenv.config({ path: path.resolve(process.cwd(), "../../.env") });

function readTextFiles(folderPath, isFakeReview) {
    const reviews = [];
    const folders = fs.readdirSync(folderPath);

    for(const folder of folders) {
        const foldPath = path.join(folderPath, folder);
        const files = fs.readdirSync(foldPath);

        for(const file of files) {
            if(!file.endsWith(".txt"))
                continue;

            const filePath = path.join(foldPath, file);
            const reviewText = fs.readFileSync(filePath, "utf8").trim();

            if(reviewText.length === 0)
                continue;

            reviews.push({
                reviewText: reviewText,
                isFake: isFakeReview
            });
        }
    }

    return reviews;
}

async function importReviewData() {
    try {
        console.log("Connecting to MONGODB.....");
        await connectDataBase();

        const projectRoot = path.resolve(process.cwd(), "../../");

        const datasetPath = path.join(projectRoot,
                                      "datasets",
                                      "reviews",
                                      "P11-1032-Datasets");
        
        const mturkPath = path.join(datasetPath, "MTurk");
        const tripAdvisorPath = path.join(datasetPath, "TripAdvisor");

        console.log("Reading deceptive reviews..");
        const fakeReviews = readTextFiles(mturkPath, true);

        console.log("Reading truthfull reviews..");
        const realReview = readTextFiles(tripAdvisorPath, false);

        const allReviews = [...fakeReviews, ...realReview];

        console.log(`Importing ${allReviews.length} reviews to MONGODB`);
        await Review.insertMany(allReviews);
        process.exit(0);
    } 
    catch (error) {
        console.error("Error importing reviews to MONGODB", error.message);
        process.exit(1);
    }
}

importReviewData();