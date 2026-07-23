# 🎬 Movie Recommendation System

A beautiful, fully-functional movie recommendation application built with React, Flask, and machine learning algorithms.

## Features

✨ **Smart Recommendations** - Personalized movie suggestions based on user preferences and ratings
🎨 **Beautiful UI** - Modern, responsive interface with smooth animations
🔍 **Advanced Search** - Filter movies by genre, year, rating, and more
⭐ **Rating System** - Rate movies and get better recommendations
📊 **Analytics** - View your watchlist and recommendation history
🚀 **Fast Performance** - Optimized algorithms for instant recommendations

## Tech Stack

**Frontend:**
- React 18+
- Tailwind CSS
- Axios for API calls
- Framer Motion for animations

**Backend:**
- Python 3.9+
- Flask
- Scikit-learn for ML algorithms
- SQLAlchemy for ORM

## Quick Start

### Terminal 1 - Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

### Terminal 2 - Frontend
```bash
cd frontend
npm install
npm start
```

Then open: http://localhost:3000

## API Endpoints

- `GET /api/movies` - Get all movies
- `GET /api/movies/search?q=query` - Search movies
- `POST /api/recommendations` - Get personalized recommendations
- `POST /api/ratings` - Add a rating
- `POST /api/watchlist` - Add to watchlist

## Features

✅ Browse movies
✅ Search & filter
✅ Rate movies
✅ Add to watchlist
✅ Get recommendations
✅ Beautiful UI
✅ Mobile responsive
