import os

import requests
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, request, session

from src.helpers import parse_scope, check_for_guild
from tree_utils import get_tree
# zapytania dla użytkowników
from database.queries.users import *

from database.models import db

load_dotenv() # ładuje plik .env
# w pliku .env należy wpisać:
# DATABASE_URL=sqlite:///database.db

# PRZED URUCHAMIANIEM APLIKACJI
# uruchomcie init_db.py (stworzy tabele)

app = Flask(__name__)

app.config.from_mapping(
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL"),
    SQLALCHEMY_TRACK_MODIFICATIONS = False,
    DISCORD_CLIENT_SECRET=os.getenv('DISCORD_CLIENT_SECRET'),
    DISCORD_CLIENT_ID=os.getenv('DISCORD_CLIENT_ID'),
    OAUTH_SCOPE='identify guilds email',
    BASE_URL='http://localhost:5000',
    PORT=5000,
    DISCORD_API_BASE_URL='https://discord.com/api',
    DISCORD_TOKEN=os.getenv('DISCORD_TOKEN'),
    ALLOWED_GUILD_ID=os.getenv('ALLOWED_GUILD_ID'),
    SECRET_KEY=os.getenv('SECRET_KEY'),
)

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

@app.route('/users')
def users():
    #return get_all_users()
    #return get_user_by_id(1)
    #add_user('some@email.meow', 'nepeta')
    return users_ranking()

@app.route('/login')
def login():
    c_id = app.config.get('DISCORD_CLIENT_ID')
    redirect_url = app.config.get('BASE_URL') + url_for('callback')
    oauth_scope_raw = app.config.get('OAUTH_SCOPE')
    oauth_scope = parse_scope(oauth_scope_raw)

    return redirect(
        f"https://discord.com/api/oauth2/authorize?client_id={c_id}&redirect_uri={redirect_url}&response_type=code&scope={oauth_scope}")


@app.route('/callback')
def callback():
    code = request.args.get('code')
    data = {
        'client_id': app.config.get('DISCORD_CLIENT_ID'),
        'client_secret': app.config.get('DISCORD_CLIENT_SECRET'),
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': app.config.get('BASE_URL') + url_for('callback'),
        'scope': parse_scope(app.config.get('OAUTH_SCOPE')),
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    r = requests.post(f"{app.config.get('DISCORD_API_BASE_URL')}/oauth2/token", data=data, headers=headers)
    r.raise_for_status()
    credentials = r.json()
    access_token = credentials['access_token']

    # Fetch user info
    user_info = requests.get(
        f"{app.config.get('DISCORD_API_BASE_URL')}/users/@me",
        headers={'Authorization': f'Bearer {access_token}'}
    ).json()

    session['user'] = user_info

    guilds = requests.get(
        f"{app.config.get('DISCORD_API_BASE_URL')}/users/@me/guilds",
        headers={'Authorization': f'Bearer {access_token}'}
    ).json()

    session['is_member'], session['guild'] = check_for_guild(guilds, int(app.config.get('ALLOWED_GUILD_ID')))
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', user=session['user'], is_member=session['is_member'],
                           guild=session['guild'])

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/ranking')
def ranking():
    return render_template('ranking.html')


if __name__ == '__main__':
    app.run(debug=True)
