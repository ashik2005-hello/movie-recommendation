import numpy as np
from app.models import Movie, Rating

class RecommendationEngine:
    @staticmethod
    def get_personalized_recommendations(user_id, num_recommendations=10):
        user_ratings = Rating.query.filter_by(user_id=user_id).all()
        if not user_ratings:
            return RecommendationEngine.get_popular_movies(num_recommendations)
        
        rated_movie_ids = [rating.movie_id for rating in user_ratings]
        high_rated_ids = [rating.movie_id for rating in user_ratings if rating.score >= 7]
        all_movies = Movie.query.all()
        unwatched_movies = [m for m in all_movies if m.id not in rated_movie_ids]
        
        if not unwatched_movies:
            return []
        
        return RecommendationEngine.content_based_filtering(high_rated_ids, unwatched_movies, num_recommendations)
    
    @staticmethod
    def content_based_filtering(liked_movie_ids, candidate_movies, num_recommendations):
        if not liked_movie_ids or not candidate_movies:
            return []
        
        liked_movies = Movie.query.filter(Movie.id.in_(liked_movie_ids)).all()
        all_genres = set()
        for movie in liked_movies + candidate_movies:
            if movie.genre:
                all_genres.update(movie.genre.split(','))
        
        all_genres = sorted(list(all_genres))
        
        def get_genre_vector(movie):
            vector = np.zeros(len(all_genres))
            if movie.genre:
                movie_genres = [g.strip() for g in movie.genre.split(',')]
                for i, genre in enumerate(all_genres):
                    if genre in movie_genres:
                        vector[i] = 1
            return vector
        
        liked_vectors = np.array([get_genre_vector(m) for m in liked_movies])
        avg_liked_vector = np.mean(liked_vectors, axis=0)
        
        scores = []
        for candidate in candidate_movies:
            candidate_vector = get_genre_vector(candidate)
            similarity = np.dot(avg_liked_vector, candidate_vector) / (np.linalg.norm(avg_liked_vector) * np.linalg.norm(candidate_vector) + 1e-6)
            scores.append((candidate, similarity))
        
        scores.sort(key=lambda x: x[1], reverse=True)
        return [movie.to_dict() for movie, _ in scores[:num_recommendations]]
    
    @staticmethod
    def get_similar_movies(movie_id, num_similar=5):
        movie = Movie.query.get(movie_id)
        if not movie:
            return []
        similar_movies = Movie.query.filter(Movie.id != movie_id, Movie.genre.ilike(f'%{movie.genre}%') if movie.genre else True).all()
        if not similar_movies:
            return []
        scores = [(m, m.rating * 0.5) for m in similar_movies]
        scores.sort(key=lambda x: x[1], reverse=True)
        return [m.to_dict() for m, _ in scores[:num_similar]]
    
    @staticmethod
    def get_popular_movies(num_movies=10):
        movies = Movie.query.order_by(Movie.rating.desc()).limit(num_movies).all()
        return [m.to_dict() for m in movies]
    
    @staticmethod
    def get_trending_movies(num_movies=10):
        movies = Movie.query.order_by(Movie.created_at.desc()).limit(num_movies).all()
        return [m.to_dict() for m in movies]
