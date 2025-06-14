import os
from werkzeug.exceptions import NotFound
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, session, url_for, request, jsonify

from .auth import login_required
from .admin_options import admin_only
from .tree_utils import get_tree, to_cytoscape_format
from .database.queries.users import *
from .database.queries.user_tasks import *
from .database.queries.trees import get_public_trees, get_tree_json_by_user, get_tree as get_tree_db
from grywalizacja_app.extensions import db

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
        KICK_NON_MEMBERS = True,
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
    def tree():
        trees = get_public_trees()
        tree_id = request.args.get('tree_id', type=int)
        if not tree_id and trees:
            tree_id = trees[0]['id']  # domyslnie wczytuje sie pierwsze drzewko
        return render_template('tree.html', trees=trees, selected_tree_id=tree_id)

    # uruchamia się przez tree.js
    @app.route("/tree/cytoscape")
    def get_cytoscape_tree():
        tree_id = request.args.get('tree_id', type=int)
        if not tree_id:
            trees = get_public_trees()
            if not trees:
                return jsonify({'nodes': [], 'edges': []})
            tree_id = trees[0]['id'] #  ponownie, domyslnie wczytuje sie pierwsze

        if not 'user' in session:
            tree_json = get_tree_db(tree_id)['json_structure']
        else:
            tree_json = get_tree_json_by_user(tree_id, session['user']['id'])

        return jsonify(to_cytoscape_format(tree_json))

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
            add_user_tasks_by_user(session['user']['id'])
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
    @admin_only
    def admin():
        return render_template('admin.html')

    from . import auth
    from . import admin_options
    app.register_blueprint(auth.bp)
    app.register_blueprint(admin_options.admin)

    from . import api
    app.register_blueprint(api.api)

    return app