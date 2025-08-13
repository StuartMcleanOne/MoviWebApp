import os
import requests
from dotenv import load_dotenv
from .models import db, User, Movie


class DataManager():

    def __init__(self):
        # Loads environment variables from a .env file
        load_dotenv()
        self.OMDB_API_KEY = os.getenv("OMDB_API_KEY")
        if not self.OMDB_API_KEY:
            raise ValueError("OMDB_API_KEY not found. Please set it in a .env file.")

    def get_users(self):
        """Returns a list of all users in the database."""
        return User.query.all()


    def _fetch_movie_data(self, title):
        """Fetches movie data from the OMDb API."""
        url = f"http://www.omdbapi.com/?apikey={self.OMDB_API_KEY}&t={title}"
        response = requests.get(url)
        data = response.json()

        if data.get("Response") == "True":
            return data
        return None

    def add_user(self, name):
        """Adds a new user to the database."""
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
        """Retrieves a user by their ID."""
        return User.query.filter_by(id=user_id).first()

    def add_movie(self, user_id, title):
        """
        Adds a movie for a specific user after fetching its data from OMDb.
        Returns a tuple: (success, message)
        """
        movie_data = self._fetch_movie_data(title)

        if not movie_data:
            return False, f"Movie '{title}' not found in OMDb."

        try:
            new_movie = Movie(
                user_id=user_id,
                name=movie_data.get("Title"),
                director=movie_data.get("Director"),
                year=movie_data.get("Year"),
                poster_url=movie_data.get("Poster")
            )
            db.session.add(new_movie)
            db.session.commit()
            return True, f"Movie '{new_movie.name}' added successfully!"
        except Exception as e:
            db.session.rollback()
            return False, f"Error adding movie to database: {e}"

    def delete_movie(self, movie_id):
        """Deletes a movie by its ID."""
        movie_to_delete = Movie.query.filter_by(id=movie_id).first()
        if movie_to_delete:
            db.session.delete(movie_to_delete)
            db.session.commit()
            return True
        return False

    def update_movie(self, movie_id, new_data):
        """Updates a movie's information."""
        movie_to_update = Movie.query.filter_by(id=movie_id).first()
        if movie_to_update:
            movie_to_update.name = new_data.get('name', movie_to_update.name)
            movie_to_update.director = new_data.get('director', movie_to_update.director)
            movie_to_update.year = new_data.get('year', movie_to_update.year)
            movie_to_update.poster_url = new_data.get('poster_url', movie_to_update.poster_url)
            db.session.commit()
            return True
        return False

    def get_movies_by_user(self, user_id):
        """Gets all movies for a specific user."""
        return Movie.query.filter_by(user_id=user_id).all()