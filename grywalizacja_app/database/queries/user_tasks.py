from grywalizacja_app.extensions import db
from grywalizacja_app.database.models import User_Task, Task, User
from sqlalchemy.orm import joinedload
from typing import overload


def _prettify_user_task(user_task: User_Task):
    '''
    Makes user_task into a dictionary.
    '''
    return {
        'user_id': user_task.user_id,
        'task_id': user_task.task_id,
        'status': user_task.status,
        'is_visible': user_task.is_visible
    }

def _prettify_user_tasks(user_tasks: list[User_Task]):
    '''
    Makes list of user_tasks as dictionaries.
    '''
    return [_prettify_user_task(user_task) for user_task in user_tasks]

@overload
def get_user_tasks(task_id):
    '''
    Gets tasks by task id.
    '''
    ...

@overload
def get_user_tasks(user_id):
    '''
    Get tasks by user id.
    '''
    ...

    from typing import overload

def get_user_tasks(*, task_id = None, user_id = None):
    '''
    Implementation of:
    - get_user_tasks(task_id)
    - get_user_tasks(user_id)
    '''
    if task_id is not None:
        user_tasks = User_Task.query.filter_by(task_id=task_id).all()
    elif user_id is not None:
        user_tasks = User_Task.query.filter_by(user_id=user_id).all()
    else:
        raise ValueError("Musisz podać albo task_id, albo user_id")
    
    return _prettify_user_tasks(user_tasks)

def get_user_task(task_id, user_id):
    '''
    Gets one user task by task and user id. Throws NoResultFound and MultipleResultsFound.
    '''
    try:
        user_task = User_Task.query.filter_by(user_id=user_id, task_id=task_id).one()
        return _prettify_user_task(user_task)
    except Exception as e:
        print(f'Error getting user_task: {str(e)}')
        raise

def add_user_task(task_id, user_id, status=None, is_visible=None):
    '''
    Adds a user task to database.
    '''
    user_task = User_Task(task_id=task_id, user_id=user_id, status=status, is_visible=is_visible)
    db.session.add(user_task)
    db.session.commit()

def add_user_tasks_by_user(user_id):
    '''
    Adds user tasks for one user.
    '''
    tasks = Task.query.all()

    user_tasks = [User_Task(task_id=task.id, user_id=user_id) for task in tasks]
    db.session.add_all(user_tasks)
    db.session.commit()

def add_user_tasks_by_task(task_id):
    '''
    Adds user tasks for one task.
    '''
    users : list[User] = User.query.all()

    user_tasks = [User_Task(task_id=task_id, user_id=user.discord_id) for user in users]
    db.session.add_all(user_tasks)
    db.session.commit()

def delete_user_task(task_id, user_id):
    '''
    Deletes a user task from database.
    '''
    try:
        user_task = User_Task.query.filter_by(user_id=user_id, task_id=task_id).one()
        db.session.delete(user_task)
        db.session.commit()
    except Exception as e:
        print(f'Error deleting user_task: {str(e)}')
        raise

def change_status(user_id, task_id, new_status):
    '''
    Changes status of a user_task. Throws NoResultFound and MultipleResultsFound.
    '''
    try:
        user_task : User_Task = User_Task.query.filter_by(user_id=user_id, task_id=task_id).one()
        user_task.change_status(new_status)
    except Exception as e:
        print(user_id, task_id)
        print(f'Error changing status: {str(e)}')
        raise

def change_visibility(user_id, task_id, is_visible):
    '''
    Changes visibility of a user_task. Throws NoResultFound and MultipleResultsFound.
    '''
    try:
        user_task : User_Task = User_Task.query.filter_by(user_id=user_id, task_id=task_id).one()
        user_task.change_visibility(is_visible)
    except Exception as e:
        print(f'Error changing visibility: {str(e)}')
        raise
    user_task = get_user_task(task_id, user_id)
    db.session.delete(user_task)
    db.session.commit()

def _get_foreign_names(user_task):
    user = (db.session.query(User.name).filter(User.discord_id==user_task.user_id).first())[0]
    task = (db.session.query(Task.name).filter(Task.id == user_task.task_id).first())[0]
    return user, task

def _prettify_user_task_with_related(user_task: User_Task):
    '''
    Makes user_task into a dictionary. Includes names of joined user and tree.
    '''
    user, task = _get_foreign_names(user_task)
    return {
        'user_id': str(user_task.user_id),
        'task_id': user_task.task_id,
        'status': user_task.status,
        'is_visible': user_task.is_visible,
        'user': user,
        'task': task
    }

def _prettify_user_tasks_with_related(user_tasks: list[User_Task]):
    '''
    Makes list of user_tasks as dictionaries.
    '''
    return [_prettify_user_task_with_related(user_task) for user_task in user_tasks]

def get_user_tasks_by_status(status=0):
    '''
    Gets all user tasks with given status.
    '''
    user_tasks = User_Task.query.filter_by(status=status).all()
    return _prettify_user_tasks_with_related(user_tasks)