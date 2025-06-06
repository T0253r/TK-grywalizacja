from grywalizacja_app.database.models import db, User_Task, Task, User
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
    Gets one user task by task and user id.
    '''
    user_task = User_Task.query.filter_by(user_id=user_id, task_id=task_id).one_or_404()
    return _prettify_user_task(user_task)

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
    users = User.query.all()

    user_tasks = [User_Task(task_id=task_id, user_id=user.id) for user in users]
    db.session.add_all(user_tasks)
    db.session.commit()

def delete_user_task(task_id, user_id):
    '''
    Deletes a user task from database.
    '''
    user_task = get_user_task(task_id, user_id)
    db.session.delete(user_task)
    db.session.commit()