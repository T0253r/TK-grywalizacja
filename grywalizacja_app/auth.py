"""Set of endpoints and helper function related to authorization"""
import functools

import requests
from flask import (
    Blueprint, redirect, render_template, request, session, url_for, current_app
)
from requests import HTTPError

from .helpers import parse_scope, check_for_guild

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login')
def login():
    """Endpoint that shows log-in terms and button."""
    return render_template('login.html')


@bp.route('/login-with-discord')
def login_with_discord():
    """Endpoint that redirects to the discord authorization URL."""
    app = current_app
    c_id = app.config.get('DISCORD_CLIENT_ID')
    redirect_url = app.config.get('BASE_URL') + url_for('auth.callback')
    oauth_scope_raw = app.config.get('OAUTH_SCOPE')
    oauth_scope = parse_scope(oauth_scope_raw)

    return redirect(
        f"https://discord.com/api/oauth2/authorize?client_id={c_id}&redirect_uri={redirect_url}&response_type=code&scope={oauth_scope}")


@bp.route('/logout')
def logout():
    """Endpoint to log out the user and clear the session."""
    session.clear()
    return redirect(url_for('index'))


@bp.route('/callback')
def callback():
    """Endpoint that gets the authorization token from the discord auth server
    fetches the user data and guilds
    and puts it into the current session."""
    app = current_app
    code = request.args.get('code')
    # Data for request that gets the user info
    data = {
        'client_id': app.config.get('DISCORD_CLIENT_ID'),
        'client_secret': app.config.get('DISCORD_CLIENT_SECRET'),
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': app.config.get('BASE_URL') + url_for('auth.callback'),
        'scope': parse_scope(app.config.get('OAUTH_SCOPE')),
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    try:
        r = requests.post(f"{app.config.get('DISCORD_API_BASE_URL')}/oauth2/token", data=data, headers=headers,
                          timeout=5)
        r.raise_for_status()
    except HTTPError as e:
        return redirect(url_for('auth.login_invalid', code=e.response.status_code))
    credentials = r.json()
    access_token = credentials['access_token']

    fetch_user_info(access_token)

    if not session.get('is_member'):
        session.pop('user', None)
        session.pop('guild', None)
        session.pop('is_member', None)
        return redirect(url_for('auth.login_invalid', code=403))

    guilds = requests.get(
        f"{app.config.get('DISCORD_API_BASE_URL')}/users/@me/guilds",
        headers={'Authorization': f'Bearer {access_token}'}
    ).json()

    #session['is_member'], session['guild'] = check_for_guild(guilds, int(app.config.get('ALLOWED_GUILD_ID')))
    session['is_admin'] = None # nie wiem czy bedzie sprawiac problemow
    return redirect(url_for('dashboard'))


@bp.route('/login-invalid')
def login_invalid():
    """Endpoint to inform user that the log-in failed."""
    error_code = request.args.get('code', default=400, type=int)
    return render_template('login_invalid.html', membership_required=current_app.config.get('KICK_NON_MEMBERS'),
                           error_code=error_code)


def login_required(view):
    """Wrapper for all the views that require the user to be logged in."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not session.get('user'):
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


def fetch_user_info(access_token: str) -> None:
    """Gets user data from discord and stores it in current browser session."""
    app = current_app
    user_info = requests.get(
        f"{app.config.get('DISCORD_API_BASE_URL')}/users/@me",
        headers={'Authorization': f'Bearer {access_token}'},
        timeout=5
    ).json()

    session['user'] = user_info

    guilds = requests.get(
        f"{app.config.get('DISCORD_API_BASE_URL')}/users/@me/guilds",
        headers={'Authorization': f'Bearer {access_token}'},
        timeout=5
    ).json()

    session['is_member'], session['guild'] = check_for_guild(guilds, int(app.config.get('ALLOWED_GUILD_ID')))
