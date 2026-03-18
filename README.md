# AI-Powered E-Commerce Platform

This project is a dissertation-focused prototype that combines a MERN backend with a Flask AI service.

## Final dissertation scope
1. Feature 1 - Fake Review Detection
2. Feature 3 - Conversational Product Search

## Project purpose
This project focuses on two practical AI features for an e-commerce system:
- detecting fake product reviews using a trained machine learning model
- helping users search for products using a simple conversational assistant

The implementation scope was intentionally kept small and dissertation-safe so that the system remains easy to explain, test, and demonstrate.

## Stack
- React frontend
- Node.js / Express backend
- MongoDB
- Python Flask AI service

## Frontend
A simple React + Vite frontend is included in `frontend/` for the final dissertation scope only.

Implemented frontend features:
- product listing from MongoDB through `GET /api/products`
- product detail page
- review submission through `POST /api/reviews`
- visible review display through `GET /api/reviews/visible`
- floating AI assistant and right-side chat drawer through `POST /api/chat`

## Important implementation notes
- friendly small-talk replies are handled through `ai/intent.json`
- both AI features are kept in one simple `ai/main.py`
- product dataset import is manual only
- fake reviews are hidden from the public review list after AI prediction
- the project is a prototype, not a production-scale system

## Project structure
```text
ai/
    main.py
    intent.json
    config/
    feature_1/
    feature_3/
    scripts/
        feature_1/
            train_model.py
        feature_3/
            import_dataset.py
backend/
frontend/
datasets/
docs/
```

## Start commands
### 1. Backend
From the project root:

```bash
npm install
npm run dev
```

### 2. Frontend
In a separate terminal:

```bash
cd frontend
npm install
npm run dev
```

### 3. AI service
In a third terminal:

```bash
cd ai
pip install -r requirements.txt
python main.py
```

Make sure the backend runs on `5000`, the AI service runs on `5001`, and the frontend runs on `5002`.

## Manual preparation scripts
### Train Feature 1 model
From inside `ai/`:

```bash
python scripts/feature_1/train_model.py
```

### Import Feature 3 product dataset
From inside `ai/`:

```bash
python scripts/feature_3/import_dataset.py
```

## Evaluation helper
From the project root:

```bash
npm run check:feature3
```

Use the suggested messages in the frontend chat drawer and record screenshots/results for dissertation evaluation.