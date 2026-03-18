# Setup Guide

## 1. Root environment file
Create a `.env` file in the project root by copying `.env.example`.

## 2. Backend
1. Install root dependencies with `npm install`
2. Start backend with `npm run dev`
3. Backend runs on `http://localhost:5000`

## 3. AI Service
1. Create and activate a Python virtual environment inside `ai/`
2. Install Python dependencies from `ai/requirements.txt`
3. Start the AI service with `python main.py`
4. AI service runs on `http://localhost:5001`

## 4. Frontend
1. Install frontend dependencies with `npm install` inside `frontend`
2. Start frontend with `npm run dev`
3. Frontend runs on `http://localhost:5002`

## 5. Manual product dataset import
Feature 3 product data import is a manual preparation step only.
It is not called automatically by backend startup.

Run this from inside `ai/` after MongoDB is ready:

```bash
python scripts/feature_3/import_dataset.py
```

## 6. Manual model training
Run this from inside `ai/`:

```bash
python scripts/feature_1/train_model.py
```

## 7. Optional Feature 3 evaluation
Run this from the project root:

```bash
npm run check:feature3
```

## 8. Application flow
1. Products load from MongoDB through `/api/products`
2. Reviews submit through `/api/reviews`
3. Public reviews load from `/api/reviews/visible`
4. Assistant chat uses `/api/chat`
5. Fake reviews are stored with AI prediction metadata and hidden from the public review list