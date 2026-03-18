import os
import sys
import json
import pickle
import pandas as pd
from scipy.sparse import csr_matrix, hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, precision_score, recall_score, f1_score, confusion_matrix

this_file_path = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(this_file_path, "../..")))

from nlp import clean_and_stem_text


# Importing pre-fixed paths via settings.py from /config.

from config.settings import load_settings

settings = load_settings()
dataset_path = settings["FEATURE_1_DATASET_PATH"]
model_path = settings["FEATURE_1_MODEL_PATH"]
vectorizer_path = settings["FEATURE_1_VECTORIZER_PATH"]
metrics_path = settings["FEATURE_1_METRICS_PATH"]



def main():
    
    # Load Csv:
    
    df = pd.read_csv(dataset_path) # dataset = 'fake review dataset':
                                        # It has "4 columns" and "40,432 rows". The four coulumns are,
                                            # 1. 'category'
                                            # 2. 'rating' - 1 to 5.
                                            # 3. 'label' - CG/OR.
                                            # 4. 'text_' - review text.
    # print(df.shape)
    # print(df.head())
    # print(df.isnull().sum())  # No missing values in all 4 columns.
    
    df = df.dropna(subset=["rating", "text_", "label"])

    df["text_"] = df["text_"].apply(clean_and_stem_text)
    # print(df["text_"])


    # Normalization:
    
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df = df.dropna(subset=["rating"])
    df = df[(df["rating"] >= 1) & (df["rating"] <= 5)]
    df["rating"] = df["rating"].astype(int)

    df["label"] = df["label"].apply(lambda x: 1 if x == "CG" else 0) # "label" column has 2 values, which is "CG" and "OR".
                                                                    # "CG" - Computer Generated review
                                                                    # "OR" - Original review
                                                                    # I used "lambda function" to assign '1' for "CG" and '0' for "OR".

    x_text = df["text_"].values
    x_rating = df["rating"].values
    y = df["label"].values
    # print(X_text)
    # print(X_rating)
    # print(Y)
    
    x_text_train, x_text_test, x_rating_train, x_rating_test, y_train, y_test = train_test_split(
        x_text,
        x_rating,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )
    # TF-IDF vectorizer:

    vectorizer = TfidfVectorizer(ngram_range=(1, 2),  # used unigrams + bigrams (1,2) to capture short phrases.
                                 max_features=30000,  # max_features limits vocabulary size to control memory/time.
                                 min_df=2,
                                 sublinear_tf=True)
      
    x_text_train_vec = vectorizer.fit_transform(x_text_train)
    x_text_test_vec = vectorizer.transform(x_text_test)

    x_rating_train_vec = csr_matrix(x_rating_train.reshape(-1, 1))
    x_rating_test_vec = csr_matrix(x_rating_test.reshape(-1, 1))

    x_train_vec = hstack([x_text_train_vec, x_rating_train_vec])
    x_test_vec = hstack([x_text_test_vec, x_rating_test_vec])


    # Model: Logistic regression

    model = LogisticRegression(max_iter=1500)
    model.fit(x_train_vec, y_train)


    # Evaluation - [Acccuracy score, Classification report]

    y_pred = model.predict(x_test_vec)

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    matrix = confusion_matrix(y_test, y_pred).tolist()


    # Save the trained model as pickle file  in './models/feature_1/'
        
    with open(model_path, "wb") as model_file:
        pickle.dump(model, model_file)
        
    print("\n - 'fake_review_model.pkl' successfully in ./models/feature_1/")

    # Save the trained vectorizer as pickle file  in './models/feature_1/'
        
    with open(vectorizer_path, "wb") as vectorizer_file:
        pickle.dump(vectorizer, vectorizer_file)
        
    print("\n - 'fake_review_vectorizer.pkl' successfully in ./models/feature_1/")
    
    # Save the training metrics as json file  in './models/feature_1/'
    
    metrics = {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "confusion_matrix": matrix,
        "rating_used": True,
    }

    with open(metrics_path, "w", encoding="utf-8") as metrics_file:
        json.dump(metrics, metrics_file, indent=4)
    
    print("\n - 'training_metrics.json' successfully in ./evaluations/feature_1/")
    print("\n")

if __name__ == "__main__":
    main()