from database.models import db, Task
from database.queries.user_tasks import add_user_tasks_by_task
from typing import overload


def _prettify_task(task: Task):
    '''
    Makes task into a dictionary.
    '''
    return {
        'id': task.id,
        'tree_id': task.tree_id,
        'node_id':task.node_id,
        'name': task.name,
        'description': task.description,
        'points': task.points
    }

def _prettify_tasks(tasks: list[Task]):
    '''
    Makes list of tasks as dictionaries.
    '''
    return [_prettify_task(task) for task in tasks]

def get_tasks_by_tree_id(tree_id):
    '''
    Gets all tasks of a tree.
    '''
    tasks = Task.query.filter_by(tree_id=tree_id).all()
    return _prettify_tasks(tasks)

@overload
def get_task(tree_id, node_id):
    '''
    Gets a task of a tree by task id defined in that tree.
    '''
    ...

@overload
def get_task(id):
    '''
    Gets a task by id.
    '''
    ...

def get_task(*args):
    '''
    Implementation of:
    - get_task(id) 
    - get_task(tree_id, node_id)
    '''
    if len(args) == 1:
        task = Task.query.get_or_404(args[0])
    elif len(args) == 2:
        tree_id, node_id = args
        task = Task.query.filter_by(tree_id=tree_id, node_id=node_id).first_or_404()
    else:
        raise TypeError('Invalid arguments - expected either get_task(id) or get_task(tree_id, node_id)')
    
    return task

def add_task(tree_id, node_id, name, description, points):
    task = Task(tree_id= tree_id, node_id=node_id, name=name, description=description, points=points)
    db.session.add(task)
    db.session.commit()
    add_user_tasks_by_task(task.id)

def add_all_tasks(tree_id, json_structure):
    for node in json_structure['nodes']:
        add_task(tree_id=tree_id,
                 node_id=node['id'],
                 name=node['name'],
                 description=node['description'],
                 points=node['points'])

@overload
def delete_task(tree_id, node_id):
    '''
    Deletes a task of a tree by task id defined in that tree.
    '''
    ...

@overload
def delete_task(id):
    '''
    Deletes a task by id.
    '''
    ...

def delete_task(*args):
    '''
    Implementation of:
    - delete_task(id) 
    - delete_task(tree_id, node_id)
    '''
    if len(args) == 1 or len(args) == 2:
        task = get_task(args)
    else:
        raise TypeError('Invalid arguments - expected either get_task(id) or get_task(tree_id, node_id)')
    
    db.session.delete(task)
    db.session.commit()
