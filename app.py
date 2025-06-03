import os
from dotenv import load_dotenv
from flask import Flask, render_template
from tree_utils import get_tree

from database.models import db

load_dotenv() # ładuje plik .env
# w pliku .env należy wpisać:
# DATABASE_URL=sqlite:///database.db

# PRZED URUCHAMIANIEM APLIKACJI
# uruchomcie init_db.py (stworzy tabele)

app = Flask(__name__)

url = os.getenv("DATABASE_URL") # pobiera url bazy danych z .env
app.config['SQLALCHEMY_DATABASE_URI'] = url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app) # inicjalizuje aplikację dla bazy danych

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tree')
def tree():
    return render_template('tree.html')

# uruchamia się przez tree.js
@app.route("/tree/cytoscape")
def get_cytoscape_tree():
    return get_tree('data/drzewko.json')
# zapytania dla użytkowników
from database.queries.users import *

@app.route('/users')
def users():
    #return get_all_users()
    #return get_user_by_id(1)
    #add_user('some@email.meow', 'nepeta')
    return users_ranking()


if __name__ == '__main__':
    app.run(debug=True)
