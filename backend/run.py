import os
from app import create_app, db
from app.models import Movie

app = create_app(os.environ.get('FLASK_ENV', 'development'))

def seed_database():
    if Movie.query.first():
        print("Database already seeded.")
        return
    
    sample_movies = [
        Movie(title="The Shawshank Redemption", description="Two imprisoned men bond over a number of years.", genre="Drama", release_year=1994, director="Frank Darabont", cast="Tim Robbins, Morgan Freeman", rating=9.3, runtime=142, poster_url="https://via.placeholder.com/300x450?text=Shawshank", backdrop_url="https://via.placeholder.com/1280x720?text=Shawshank"),
        Movie(title="The Godfather", description="The aging patriarch of an organized crime dynasty.", genre="Crime, Drama", release_year=1972, director="Francis Ford Coppola", cast="Marlon Brando, Al Pacino", rating=9.2, runtime=175, poster_url="https://via.placeholder.com/300x450?text=Godfather", backdrop_url="https://via.placeholder.com/1280x720?text=Godfather"),
        Movie(title="The Dark Knight", description="When the menace known as the Joker wreaks havoc.", genre="Action, Crime, Drama", release_year=2008, director="Christopher Nolan", cast="Christian Bale, Heath Ledger", rating=9.0, runtime=152, poster_url="https://via.placeholder.com/300x450?text=Dark+Knight", backdrop_url="https://via.placeholder.com/1280x720?text=Dark+Knight"),
        Movie(title="Pulp Fiction", description="The lives of two mob hitmen, a boxer, a gangster.", genre="Crime, Drama", release_year=1994, director="Quentin Tarantino", cast="John Travolta, Samuel L. Jackson", rating=8.9, runtime=154, poster_url="https://via.placeholder.com/300x450?text=Pulp+Fiction", backdrop_url="https://via.placeholder.com/1280x720?text=Pulp+Fiction"),
        Movie(title="Forrest Gump", description="The presidencies of Kennedy and Johnson unfold.", genre="Drama, Romance", release_year=1994, director="Robert Zemeckis", cast="Tom Hanks, Sally Field", rating=8.8, runtime=142, poster_url="https://via.placeholder.com/300x450?text=Forrest+Gump", backdrop_url="https://via.placeholder.com/1280x720?text=Forrest+Gump"),
        Movie(title="Inception", description="A thief who steals corporate secrets through dreams.", genre="Action, Sci-Fi, Thriller", release_year=2010, director="Christopher Nolan", cast="Leonardo DiCaprio, Marion Cotillard", rating=8.8, runtime=148, poster_url="https://via.placeholder.com/300x450?text=Inception", backdrop_url="https://via.placeholder.com/1280x720?text=Inception"),
        Movie(title="The Matrix", description="A computer hacker learns about the true nature.", genre="Action, Sci-Fi", release_year=1999, director="Wachowski", cast="Keanu Reeves, Laurence Fishburne", rating=8.7, runtime=136, poster_url="https://via.placeholder.com/300x450?text=The+Matrix", backdrop_url="https://via.placeholder.com/1280x720?text=The+Matrix"),
        Movie(title="Parasite", description="Greed and class discrimination threaten symbiosis.", genre="Drama, Thriller", release_year=2019, director="Bong Joon Ho", cast="Song Kang-ho, Lee Sun-kyun", rating=8.6, runtime=132, poster_url="https://via.placeholder.com/300x450?text=Parasite", backdrop_url="https://via.placeholder.com/1280x720?text=Parasite"),
        Movie(title="Interstellar", description="A team of explorers travel through a wormhole.", genre="Adventure, Drama, Sci-Fi", release_year=2014, director="Christopher Nolan", cast="Matthew McConaughey, Anne Hathaway", rating=8.6, runtime=169, poster_url="https://via.placeholder.com/300x450?text=Interstellar", backdrop_url="https://via.placeholder.com/1280x720?text=Interstellar"),
        Movie(title="The Avengers", description="Earth's mightiest heroes must come together.", genre="Action, Adventure, Sci-Fi", release_year=2012, director="Joss Whedon", cast="Robert Downey Jr., Chris Evans", rating=8.0, runtime=143, poster_url="https://via.placeholder.com/300x450?text=Avengers", backdrop_url="https://via.placeholder.com/1280x720?text=Avengers"),
    ]
    
    for movie in sample_movies:
        db.session.add(movie)
    db.session.commit()
    print(f"Seeded database with {len(sample_movies)} movies.")

if __name__ == '__main__':
    with app.app_context():
        seed_database()
    app.run(debug=True, port=5000)
