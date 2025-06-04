from database.models import db, User


def prettify_users(users):
    '''
    Makes it into a json so it looks nice on the site.
    '''
    result = [{
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'points': user.points
    } for user in users]
    
    return result

def get_users():
    '''
    Gets all non-admin users.
    '''
    users = User.query.filter_by(is_admin=False).all()
    return users

def users_ranking():
    '''
    Gets the top 3 users with the most points.
    '''
    users = User.query.filter_by(is_admin=False)\
                      .order_by(User.points.desc())\
                      .limit(3)\
                      .all()
    return users

def get_admins():
    '''
    Gets all admin users.
    '''
    admins = User.query.filter_by(is_admin=True).all()
    return admins

def get_user_by_id(id):
    '''
    Gets a user by id.
    '''
    user = db.get_or_404(User, id)
    return user

def _add_any_user(email, name, is_admin=False):
    '''
    Adds a user to database.
    '''
    user = User(email=email, name=name, is_admin=is_admin)
    db.session.add(user)
    db.session.commit()

def add_user(email, name):
    '''
    Adds a non-admin user to database.
    '''
    _add_any_user(email, name)

def add_admin(email, name):
    '''
    Adds an admin user to database.
    '''
    _add_any_user(email, name, True)

def delete_user(id):
    '''
    Deletes user by id.
    '''
    user = get_user_by_id(id)
    db.session.delete(user)
    db.session.commit()