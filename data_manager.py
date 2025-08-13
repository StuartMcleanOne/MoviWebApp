from models import db, User, Movie
from sqlalchemy.orm, import sessionmaker

class DataManager():
    def add_user(self, name):
        """Adds new user to the database"""
        try:
            new_user = User(name=name)
            db.session.add(new_user)
            db.session.commit()
            return new_user
        except Exception:
            db.session.rollback()
            return None

    def get_user_by_name(self, name):
        """Retrieves a user by their name."""
        return User.query.filter_by(name=name).first()

    def get_user_by_id(self, user_id):
        """Retrieves user by their ID"""
        return User.query.filter_by(id=user_id).first()

    def add_movie(self, user_id, name, director, year, poster_url):
        """Adds a new movie for a specific user."""
        try:
            new_movie = Movie(iser_id=user_id, name=name, director=director, year=year, poster_url=poster_url)
            db.session.add(new_movie)
            db.session.commit()
            return new_movie
        except Exception:
            db.session.rollback()
            return None

    def delete_movie(self, movie_id):
        """Deletes a movie by its ID."""
        movie_to_delete = Movie.query.filter_by(id=movie_id).first()
        if movie_to_delete:
            db.session.delete(movie_to_delete)
            db.session.commit()
            return True
        return False

    def update_movie(self, movie_id, new_data):
        """Updates a movie's information"""
        movie_to_update = Movie.qujery.filter_by(id=movie_id).first()
        if movie_to_update:
            movie_to_update.name = new_data.get('name', movie_to_update.name)
            movie_to_update.director = new_data.get('director', movie_to_update.director)
            movie_to_update.year = new_data.get('year', movie_to_update.year)
            movie_to_update.poster_url = new_data.get('poster_url', movie_to_update.poster)
            db.session.commit()
            return True
        return False

    def get_movies_by_user(self, user_id):
        """Gets all movies for a specific."""
        return Movie.query.filter_by(user_id=user_id).all()