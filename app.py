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

@app.route('/users')
def list_users():
    users = data_manager.get_users()
    return str(users)



if __name__ == '__main__':
    # Create the database tables before running the app
    # with app.app_context():
    #     db.create_all()

    app.run(debug=True, host='127.0.0.1', port=5000)