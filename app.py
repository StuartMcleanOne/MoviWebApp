from flask import Flask, render_template, request, redirect, url_for
from models import db
from data_manager import DataManager

# Create a Flask application instance
app = Flask(__name__)

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moviweb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy object
db.init_app(app)

# Create an instance of the DataManager
data_manager = DataManager()

@app.route('/')
def home():
    users = data_manager.get_users()
    return render_template('index.html', users=users)

@app.route('/users', methods=['POST'])
def add_user():
    user_name = request.form.get('user_name')
    if user_name:
        data_manager.add_user(user_name)
    return redirect(url_for('home'))

@app.route('/users/<int:user_id>/movies', methods=['GET'])
def list_movies(user_id)
    user = data_manager.get_user_by_id(user_id)
    if not user:
        return "User not found", 404
    movies = data_manager.get_movies_by_user(user_id)
    return render_template('user_movies.html', user=user, movies=movies)

@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie_for_user(user_id):
    movie_title = request.form.get('movie_title')
    if movie_title:
        data_manager.add_movie(user_id, movie_title)
    return redirect(url_for('list_movies', user_id=user_id))


if __name__ == '__main__':
    # Create the database tables before running the app
    # with app.app_context():
    #     db.create_all()

    app.run(debug=True, host='127.0.0.1', port=5000)