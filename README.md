#  MoviWeb

### Website hosted on pythonanywhere until 15 November 2025


A simple web application done as part of my Software Engineering /Ai Engineering course 
at Masterschool. 



##  Description

MoviWeb is a Flask-based web app that lets friends create and manage their own movie catalogues as recommendations for groups of friends. Just enter a movie title, and MoviWeb fetches details like the poster, release year, and director using the OMDb API. With a clean, responsive design and a SQLite backend. 

A implementation of notes or a direct link to a trailer or to imdb would be the next logical iteration here. That and probably not allowing just anyone to delete other peoples profiles. Lol

##  Features

-  **User Management**: Create and view individual user profiles.
-  **Movie Collection**: Each user can build and manage their own movie list.
-  **Automated Data Fetching**: Enter a title, and details are pulled from the OMDb API.
-  **Responsive Design**: Works seamlessly on desktop and mobile.
-  **CRUD Operations**: Add, view, edit, and delete movies and users.

##  Dependancies Used

| Technology         | Purpose                          |
|--------------------|----------------------------------|
| Flask              | Core web framework               |
| Flask-SQLAlchemy   | ORM for SQLite database          |
| Requests           | API calls to OMDb                |
| Jinja              | Front-end templating             |
| HTML & CSS         | Structure and styling            |

## ⚙️ Setup and Installation

Follow these steps to get MoviWeb running locally:

### 1. Clone the repository

```bash
git clone [your-repository-url]
cd moviweb-project 
````

### 2. Create a virtual environment 

````bash
python -m venv venv
````

### 3. Activate the virtual environment
 
```bash
venv\Scripts\activate
source venv/bin/activate
````

### 4. Install dependencies

````bash
pip install -r requirements.txt
````

### 5. Set up environment variables

````bash
OMDB_API_KEY=your_omdb_api_key
SECRET_KEY=a_long_random_string
````
Get your OMDb API key from omdbapi.com

### 6. Run the application

````bash
python app.py

````
Visit http://127.0.0.1:5000/ in your browser.

### 7. Author
Stuart McLean
