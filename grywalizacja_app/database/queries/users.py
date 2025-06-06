from grywalizacja_app.database.models import db, User


def _prettify_user(user: User):
    '''
    Makes a user into a dictionary.
    '''
    return {
        'discord_id': user.discord_id,
        'name': user.name,
        'email': user.email,
        'points': user.points
    }

def _prettify_users(users: list[User]):
    '''
    Makes a list of users as dictionaries.
    '''
    return [_prettify_user(user) for user in users]

def get_all_users():
    '''
    Gets all users, both admins and non-admins.
    '''
    users = User.query.all()
    return _prettify_users(users)

def get_non_admin_users():
    '''
    Gets all non-admin users.
    '''
    users = User.query.filter_by(is_admin=False).all()
    return _prettify_users(users)

def users_ranking():
    '''
    Gets the top 3 users with the most points.
    '''
    users = User.query.filter_by(is_admin=False)\
                      .order_by(User.points.desc())\
                      .limit(3)\
                      .all()
    return _prettify_users(users)

def get_admins():
    '''
    Gets all admin users.
    '''
    admins = User.query.filter_by(is_admin=True).all()
    return _prettify_users(admins)

def get_user_by_discord_id(discord_id):
    '''
    Gets a user by discord_id.
    '''
    user = User.query.filter_by(discord_id=discord_id).first_or_404()
    return _prettify_user(user)

def _add_any_user(discord_id, email, name, is_admin=False):
    '''
    Adds a user to database.
    '''
    user = User(discord_id=discord_id, email=email, name=name, is_admin=is_admin)
    db.session.add(user)
    db.session.commit()

def add_non_admin_user(discord_id, email, name):
    '''
    Adds a non-admin user to database.
    '''
    _add_any_user(discord_id, email, name)

def add_admin(discord_id, email, name):
    '''
    Adds an admin user to database.
    '''
    _add_any_user(discord_id, email, name, True)

def delete_user_by_discord_id(discord_id):
    '''
    Deletes user by discord_id.
    '''
    user = User.query.filter_by(discord_id=discord_id).first_or_404()
    db.session.delete(user)
    db.session.commit()