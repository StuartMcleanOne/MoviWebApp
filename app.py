"""
This module contains the Flask application routes and logic for the MoviWeb App.
It handles user and movie management, including CRUD operations and error handling.
"""
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db
from data_manager import DataManager

# Create a Flask application instance
app = Flask(__name__)

# A secret key is required for flashing messages and session management
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moviweb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy object
db.init_app(app)

# Create an instance of the DataManager
data_manager = DataManager()


@app.route('/')
def index():
    """
    Renders the home page, displaying a list of all users.

    Returns:
        str: The rendered index.html template.
    """
    users = data_manager.get_users()
    return render_template('index.html', users=users)


@app.route('/users', methods=['POST'])
def create_user():
    """
    Handles the POST request to create a new user.

    Redirects:
        The user to the home page after adding the new user.
    """
    user_name = request.form.get('user_name')
    if user_name:
        success, message = data_manager.add_user(user_name)
        flash(message, 'success' if success else 'error')
    return redirect(url_for('index'))


@app.route('/users/<int:user_id>/movies', methods=['GET'])
def get_movies(user_id):
    """
    Renders the page displaying all movies for a specific user.

    Args:
        user_id (int): The ID of the user.

    Returns:
        str: The rendered user_movies.html template.
    """
    user = data_manager.get_user_by_id(user_id)
    if not user:
        # Returns a 404 error if the user does not exist
        return "User not found", 404
    movies = data_manager.get_movies_by_user(user_id)
    return render_template('user_movies.html', user=user, movies=movies)


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie_to_user(user_id):
    """
    Handles the POST request to add a new movie for a specific user.

    Args:
        user_id (int): The ID of the user.

    Redirects:
        The user back to their movies page after adding the movie.
    """
    movie_title = request.form.get('movie_title')
    if movie_title:
        success, message = data_manager.add_movie(user_id, movie_title)
        flash(message, 'success' if success else 'error')
    return redirect(url_for('get_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update',
           methods=['POST'])
def update_movie(user_id, movie_id):
    """
    Handles the POST request to update a movie's name.

    Args:
        user_id (int): The ID of the user.
        movie_id (int): The ID of the movie to update.

    Redirects:
        The user back to their movies page after updating the movie.
    """
    new_movie_name = request.form.get('new_movie_name')
    if new_movie_name:
        success, message = data_manager.update_movie(movie_id, new_movie_name)
        flash(message, 'success' if success else 'error')
    return redirect(url_for('get_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete',
           methods=['POST'])
def delete_movie(user_id, movie_id):
    """
    Handles the POST request to delete a movie.

    Args:
        user_id (int): The ID of the user.
        movie_id (int): The ID of the movie to delete.

    Redirects:
        The user back to their movies page after deleting the movie.
    """
    success, message = data_manager.delete_movie(movie_id)
    flash(message, 'success' if success else 'error')
    return redirect(url_for('get_movies', user_id=user_id))


@app.errorhandler(404)
def page_not_found(e):
    """
    Handles 404 Not Found errors by rendering a custom page.

    Args:
        e: The exception object.

    Returns:
        A tuple containing the rendered 404.html template and the 404 status code.
    """
    return render_template('404.html'), 404


if __name__ == '__main__':
    with app.app_context():


        app.run(debug=True, host='127.0.0.1', port=5000)