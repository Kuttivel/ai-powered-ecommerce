import os
import sys
import json
import pickle
import pandas as pd
from scipy.sparse import csr_matrix, hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# clarify path for to fetch utils/nlp.py

CURRENT_FILE_PATH = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(CURRENT_FILE_PATH, "../..")))

from utils.nlp import clean_and_stem_text


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

    X_text = df["text_"].values
    X_rating = df["rating"].values
    Y = df["label"].values
    # print(X_text)
    # print(X_rating)
    # print(Y)
    
    X_text_train, X_text_test, X_rating_train, X_rating_test, Y_train, Y_test = train_test_split(X_text,
                                                                                                  X_rating,
                                                                                                  Y,
                                                                                                  test_size=0.2,
                                                                                                  random_state=2,
                                                                                                  stratify=Y)


    # TF-IDF vectorizer:

    vectorizer = TfidfVectorizer(ngram_range=(1, 2),  # used unigrams + bigrams (1,2) to capture short phrases.
                                 max_features=50000)  # max_features limits vocabulary size to control memory/time.
    X_text_train_vec = vectorizer.fit_transform(X_text_train)
    X_text_test_vec = vectorizer.transform(X_text_test)


    # Convert rating into sparse matrix and combine with text features:

    X_rating_train_vec = csr_matrix(X_rating_train.reshape(-1, 1))
    X_rating_test_vec = csr_matrix(X_rating_test.reshape(-1, 1))

    X_train_vec = hstack([X_text_train_vec, X_rating_train_vec])
    X_test_vec = hstack([X_text_test_vec, X_rating_test_vec])



    # Model: Logistic regression

    model = LogisticRegression(max_iter=2000)
    model.fit(X_train_vec, Y_train)


    # Evaluation - [Acccuracy score, Classification report]

    train_pred = model.predict(X_train_vec)
    test_pred = model.predict(X_test_vec)

    train_acc = accuracy_score(Y_train, train_pred)
    test_acc = accuracy_score(Y_test, test_pred)
    
    report = classification_report(Y_test, test_pred, output_dict=True)

    print("\n - Training Accuracy:", train_acc)
    print("\n - Test Accuracy:", test_acc)    


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
        "train_accuracy": train_acc,
        "test_accuracy": test_acc,
        "rating_used": True,
        "classification_report": report
    }

    with open(metrics_path, "w", encoding="utf-8") as metrics_file:
        json.dump(metrics, metrics_file, indent=4)
    
    print("\n - 'training_metrics.json' successfully in ./models/feature_1/")
    print("\n")

if __name__ == "__main__":
    main()