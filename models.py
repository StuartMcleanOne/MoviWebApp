"""
This module defines the SQLAlchemy database models for the MoviWeb App.
It includes models for User and Movie, and their relationship.
"""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class User(db.Model):
    """
    User model to store user information.

    Attributes:
        id (int): Primary key for the user.
        name (str): Unique name of the user.
        movies (list): Relationship to the Movie model.
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    movies = relationship('Movie',
                          back_populates='user',
                          cascade='all, delete-orphan')


class Movie(db.Model):
    """
    Movie model to store movie information for each user.

    Attributes:
        id (int): Primary key for the movie.
        user_id (int): Foreign key linking the movie to a user.
        name (str): The title of the movie.
        director (str): The director of the movie.
        year (str): The year the movie was released.
        poster_url (str): The URL to the movie's poster image.
        user (object): Relationship to the User model.
    """
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(100), nullable=False)
    director = db.Column(db.String(100))
    year = db.Column(db.String(4))
    poster_url = db.Column(db.String(255))
    user = relationship('User', back_populates='movies')