from flask import Blueprint, request, jsonify
from app import db
from app.models import Movie, User, Rating, Watchlist
from app.recommendations import RecommendationEngine
from sqlalchemy import or_

api_bp = Blueprint('api', __name__)

@api_bp.route('/movies', methods=['GET'])
def get_movies():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    movies = Movie.query.paginate(page=page, per_page=per_page)
    return jsonify({'success': True, 'data': [m.to_dict() for m in movies.items], 'total': movies.total, 'pages': movies.pages, 'current_page': page})

@api_bp.route('/movies/search', methods=['GET'])
def search_movies():
    query = request.args.get('q', '', type=str)
    if not query:
        return jsonify({'success': False, 'message': 'Search query required'}), 400
    movies = Movie.query.filter(or_(Movie.title.ilike(f'%{query}%'), Movie.director.ilike(f'%{query}%'), Movie.genre.ilike(f'%{query}%'))).limit(50).all()
    return jsonify({'success': True, 'data': [m.to_dict() for m in movies], 'count': len(movies)})

@api_bp.route('/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify({'success': False, 'message': 'Movie not found'}), 404
    movie_data = movie.to_dict()
    avg_rating = db.session.query(db.func.avg(Rating.score)).filter_by(movie_id=movie_id).scalar()
    movie_data['average_user_rating'] = float(avg_rating) if avg_rating else 0.0
    return jsonify({'success': True, 'data': movie_data})

@api_bp.route('/movies/genre/<genre>', methods=['GET'])
def get_movies_by_genre(genre):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    movies = Movie.query.filter(Movie.genre.ilike(f'%{genre}%')).paginate(page=page, per_page=per_page)
    return jsonify({'success': True, 'data': [m.to_dict() for m in movies.items], 'total': movies.total, 'pages': movies.pages})

@api_bp.route('/recommendations', methods=['POST'])
def get_recommendations():
    data = request.get_json()
    user_id = data.get('user_id')
    num_recommendations = data.get('num_recommendations', 10)
    if not user_id:
        return jsonify({'success': False, 'message': 'user_id required'}), 400
    recommendations = RecommendationEngine.get_personalized_recommendations(user_id, num_recommendations)
    return jsonify({'success': True, 'data': recommendations, 'count': len(recommendations)})

@api_bp.route('/recommendations/similar/<int:movie_id>', methods=['GET'])
def get_similar_movies(movie_id):
    num_similar = request.args.get('num_similar', 5, type=int)
    similar = RecommendationEngine.get_similar_movies(movie_id, num_similar)
    return jsonify({'success': True, 'data': similar, 'count': len(similar)})

@api_bp.route('/recommendations/popular', methods=['GET'])
def get_popular_movies():
    num_movies = request.args.get('num_movies', 10, type=int)
    popular = RecommendationEngine.get_popular_movies(num_movies)
    return jsonify({'success': True, 'data': popular, 'count': len(popular)})

@api_bp.route('/recommendations/trending', methods=['GET'])
def get_trending_movies():
    num_movies = request.args.get('num_movies', 10, type=int)
    trending = RecommendationEngine.get_trending_movies(num_movies)
    return jsonify({'success': True, 'data': trending, 'count': len(trending)})

@api_bp.route('/ratings', methods=['POST'])
def add_rating():
    data = request.get_json()
    required = ['user_id', 'movie_id', 'score']
    if not all(k in data for k in required):
        return jsonify({'success': False, 'message': 'user_id, movie_id, score required'}), 400
    if not (1 <= data['score'] <= 10):
        return jsonify({'success': False, 'message': 'score must be between 1 and 10'}), 400
    if not Movie.query.get(data['movie_id']):
        return jsonify({'success': False, 'message': 'Movie not found'}), 404
    if not User.query.get(data['user_id']):
        return jsonify({'success': False, 'message': 'User not found'}), 404
    rating = Rating.query.filter_by(user_id=data['user_id'], movie_id=data['movie_id']).first()
    if rating:
        rating.score = data['score']
        rating.review = data.get('review', rating.review)
    else:
        rating = Rating(user_id=data['user_id'], movie_id=data['movie_id'], score=data['score'], review=data.get('review'))
        db.session.add(rating)
    db.session.commit()
    return jsonify({'success': True, 'data': rating.to_dict()}), 201

@api_bp.route('/ratings/user/<int:user_id>', methods=['GET'])
def get_user_ratings(user_id):
    ratings = Rating.query.filter_by(user_id=user_id).all()
    return jsonify({'success': True, 'data': [r.to_dict() for r in ratings], 'count': len(ratings)})

@api_bp.route('/watchlist', methods=['POST'])
def add_to_watchlist():
    data = request.get_json()
    required = ['user_id', 'movie_id']
    if not all(k in data for k in required):
        return jsonify({'success': False, 'message': 'user_id and movie_id required'}), 400
    existing = Watchlist.query.filter_by(user_id=data['user_id'], movie_id=data['movie_id']).first()
    if existing:
        existing.status = data.get('status', 'to_watch')
        db.session.commit()
        return jsonify({'success': True, 'data': existing.to_dict()})
    watchlist = Watchlist(user_id=data['user_id'], movie_id=data['movie_id'], status=data.get('status', 'to_watch'))
    db.session.add(watchlist)
    db.session.commit()
    return jsonify({'success': True, 'data': watchlist.to_dict()}), 201

@api_bp.route('/watchlist/<int:user_id>', methods=['GET'])
def get_watchlist(user_id):
    status = request.args.get('status')
    query = Watchlist.query.filter_by(user_id=user_id)
    if status:
        query = query.filter_by(status=status)
    watchlist_items = query.all()
    data = []
    for item in watchlist_items:
        item_dict = item.to_dict()
        item_dict['movie'] = item.movie.to_dict()
        data.append(item_dict)
    return jsonify({'success': True, 'data': data, 'count': len(data)})

@api_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({'success': True, 'message': 'API is running'})
