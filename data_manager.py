"""
This module provides a DataManager class for all database interactions and 
external API calls for the MoviWeb App.
"""
import os
import requests
from models import db, User, Movie
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()


class DataManager:
    """
    Handles all data management logic, including database and API operations.
    """

    def add_user(self, name):
        """
        Adds a new user to the database.

        Args:
            name (str): The name of the user.

        Returns:
            tuple: A tuple (success_boolean, message_string).
        """
        try:
            new_user = User(name=name)
            db.session.add(new_user)
            db.session.commit()
            return True, f"User '{name}' added successfully!"
        except Exception as e:
            db.session.rollback()
            return False, f"Error adding user: {str(e)}"

    def get_users(self):
        """
        Retrieves all users from the database.

        Returns:
            list: A list of User objects.
        """
        return db.session.query(User).all()

    def get_user_by_id(self, user_id):
        """
        Retrieves a user by their ID.

        Args:
            user_id (int): The ID of the user.

        Returns:
            User: The User object, or None if not found.
        """
        return db.session.get(User, user_id)

    def _fetch_movie_data(self, title):
        """
        Fetches movie data from the OMDb API.

        Args:
            title (str): The title of the movie to search for.

        Returns:
            dict: The movie data, or None if not found or an error occurs.
        """
        omdb_api_key = os.getenv("OMDB_API_KEY")
        if not omdb_api_key:
            print("OMDB_API_KEY environment variable not set.")
            return None

        # Make a GET request to the OMDb API
        response = requests.get(
            f"http://www.omdbapi.com/?apikey={omdb_api_key}&t={title}"
        )

        if response.status_code == 200:
            movie_data = response.json()
            # Check if the API returned a valid movie response
            if movie_data.get("Response") == "True":
                return movie_data

        return None

    def add_movie(self, user_id, title):
        """
        Fetches movie data and adds a new movie for a specific user.

        Args:
            user_id (int): The ID of the user.
            title (str): The title of the movie.

        Returns:
            tuple: A tuple (success_boolean, message_string).
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
            return False, f"Error adding movie to database: {str(e)}"

    def get_movies_by_user(self, user_id):
        """
        Retrieves all movies for a specific user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            list: A list of Movie objects.
        """
        user = self.get_user_by_id(user_id)
        return user.movies if user else []

    def update_movie(self, movie_id, new_name):
        """
        Updates the name of a specific movie.

        Args:
            movie_id (int): The ID of the movie.
            new_name (str): The new name for the movie.

        Returns:
            tuple: A tuple (success_boolean, message_string).
        """
        movie = db.session.get(Movie, movie_id)
        if not movie:
            return False, "Movie not found."

        try:
            movie.name = new_name
            db.session.commit()
            return True, f"Movie updated to '{new_name}' successfully!"
        except Exception as e:
            db.session.rollback()
            return False, f"Error updating movie: {str(e)}"

    def delete_movie(self, movie_id):
        """
        Deletes a specific movie from the database.

        Args:
            movie_id (int): The ID of the movie to delete.

        Returns:
            tuple: A tuple (success_boolean, message_string).
        """
        movie = db.session.get(Movie, movie_id)
        if not movie:
            return False, "Movie not found."

        try:
            db.session.delete(movie)
            db.session.commit()
            return True, "Movie deleted successfully!"
        except Exception as e:
            db.session.rollback()
            return False, f"Error deleting movie: {str(e)}"