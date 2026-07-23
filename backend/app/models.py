from app import db
from datetime import datetime

class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    genre = db.Column(db.String(100))
    release_year = db.Column(db.Integer)
    director = db.Column(db.String(255))
    cast = db.Column(db.Text)
    rating = db.Column(db.Float, default=0.0)
    poster_url = db.Column(db.String(500))
    backdrop_url = db.Column(db.String(500))
    runtime = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    ratings = db.relationship('Rating', backref='movie', lazy=True, cascade='all, delete-orphan')
    watchlist_items = db.relationship('Watchlist', backref='movie', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id, 'title': self.title, 'description': self.description,
            'genre': self.genre, 'release_year': self.release_year, 'director': self.director,
            'cast': self.cast, 'rating': self.rating, 'poster_url': self.poster_url,
            'backdrop_url': self.backdrop_url, 'runtime': self.runtime,
        }

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    ratings = db.relationship('Rating', backref='user', lazy=True, cascade='all, delete-orphan')
    watchlist = db.relationship('Watchlist', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {'id': self.id, 'username': self.username, 'email': self.email}

class Rating(db.Model):
    __tablename__ = 'ratings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    score = db.Column(db.Float, nullable=False)
    review = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {'id': self.id, 'user_id': self.user_id, 'movie_id': self.movie_id, 'score': self.score, 'review': self.review}

class Watchlist(db.Model):
    __tablename__ = 'watchlist'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    status = db.Column(db.String(20), default='to_watch')
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {'id': self.id, 'user_id': self.user_id, 'movie_id': self.movie_id, 'status': self.status}
