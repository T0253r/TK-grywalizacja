import os
from werkzeug.exceptions import NotFound
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, session, url_for

from .auth import login_required
from .tree_utils import get_tree
from .database.queries.users import *
from .database.queries.user_tasks import *
from .database.models import db

# w pliku .env należy wpisać:
# DATABASE_URL=sqlite:///database.db

# PRZED URUCHAMIANIEM APLIKACJI
# uruchomcie init_db.py (stworzy tabele)

def create_app(test_config=None):
    load_dotenv()
    app = Flask(__name__, instance_relative_config=True)

    # przerzucic do config.py
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

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app) # inicjalizuje aplikację dla bazy danych

    @app.context_processor
    def inject_admin():
        if 'user' not in session:
            return {}
        else:
            return dict(is_admin=session['is_admin'])

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/tree')
    @login_required
    def tree():
        return render_template('tree.html')

    # uruchamia się przez tree.js
    @app.route("/tree/cytoscape")
    @login_required
    def get_cytoscape_tree():
        return get_tree('data/drzewko.json')

    @app.route('/users')
    def users():
        return users_ranking()


    @app.route('/dashboard')
    @login_required
    def dashboard():
        if 'user' not in session or 'id' not in session['user']:
            return redirect(url_for('auth.login'))
        try:
            user_data = get_user_by_discord_id(session['user']['id'])
        except NotFound:
            add_non_admin_user(session['user']['id'], session['user']['email'], session['user']['global_name'])
        finally:
            if session['is_admin'] is None:
                session['is_admin'] = get_admin_by_discord_id(session['user']['id']) is not None
            return render_template('dashboard.html', user=session['user'], is_member=session['is_member'],
                                   guild=session['guild'])


    @app.route('/ranking')
    @login_required
    def ranking():
        return render_template('ranking.html')

    @app.route('/admin')
    @login_required
    def admin():
        return render_template('admin.html')

    from . import auth
    from . import admin_options
    app.register_blueprint(auth.bp)
    app.register_blueprint(admin_options.admin)

    return app