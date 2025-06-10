from grywalizacja_app.extensions import db
from grywalizacja_app.database.models import Tree
from grywalizacja_app.database.queries.tasks import add_all_tasks, get_tasks_by_tree_id
from grywalizacja_app.database.queries.user_tasks import get_user_task


def _prettify_tree(tree: Tree):
    '''
    Makes tree into a dictionary.
    '''
    return {
        'id': tree.id,
        'name': tree.name,
        'json_structure': tree.json_structure,
        'created_by': tree.created_by,
        'is_public': tree.is_public
    }

def _prettify_trees(trees: list[Tree]):
    '''
    Makes list of users as dictionaries.
    '''
    return [_prettify_tree(tree) for tree in trees]

def get_public_trees():
    '''
    Gets all public trees.
    '''
    trees = Tree.query.filter_by(is_public=True).all()
    return _prettify_trees(trees)

def get_trees_by_author(admin_id):
    ''''
    Gets all public trees made by the admin.
    '''
    trees = Tree.query.filter_by(created_by=admin_id, is_public=True).all()
    return _prettify_trees(trees)

def get_unpublished_trees(author_id):
    '''
    Gets all private trees made by the author.
    '''
    trees = Tree.query.filter_by(created_by=author_id, is_public=False).all()
    return _prettify_trees(trees)

def get_tree(id):
    '''
    Gets tree by id. Throws NoResultFound and MultipleResultsFound.
    '''
    try:
        tree = Tree.query.filter_by(id=id).one()
        return _prettify_tree(tree)
    except Exception as e:
        print(f'Exception getting tree: {str(e)}')
        raise

def get_tree_json_by_user(id, discord_id):
    '''
    Gets tree by id and user's discord id. Throws NoResultFound and MultipleResultsFound.
    '''
    try:
        tree : Tree = Tree.query.filter_by(id=id).one()
        json_structure = tree.json_structure
        tasks = get_tasks_by_tree_id(tree.id)
        for task in tasks:
            user_task = get_user_task(task_id=task['id'], user_id=discord_id)
            status = user_task['status']
            is_visible = user_task['is_visible']

            json_structure['nodes'][task['node_id']]['status'] = status
            json_structure['nodes'][task['node_id']]['is_visible'] = is_visible
            
            return json_structure
    except Exception as e:
        print(f"Exception getting tree's json: {str(e)}")
        raise

def add_tree(name, json_structure, created_by):
    '''
    Adds a tree to database.
    '''
    tree = Tree(name=name, json_structure=json_structure, created_by=created_by)
    db.session.add(tree)
    db.session.commit()
    add_all_tasks(tree_id=tree.id, json_structure=json_structure)

def delete_tree(id):
    '''
    Deletes a tree from database. Throws NoResultFound and MultipleResultsFound.
    '''
    try:
        tree = Tree.query.filter_by(id=id).one()
        db.session.delete(tree)
        db.session.commit()
    except Exception as e:
        print(f'Exception deleting tree: {str(e)}')
        raise

def make_public(id):
    '''
    Makes tree public. Throws NoResultFound and MultipleResultsFound.
    '''
    try:
        tree : Tree = Tree.query.filter_by(id=id).one()
        tree.make_public()
        db.session.commit()
    except Exception as e:
        print(f'Exception making tree public: {str(e)}')
        raise

def change_tree_name(id, new_name):
    '''
    Changes name of tree. Throws NoResultFound and MultipleResultsFound.
    '''
    try:
        tree : Tree = Tree.query.filter_by(id=id).one()
        tree.change_name(new_name)
        db.session.commit()
    except Exception as e:
        print(f'Exception changing name of tree: {str(e)}')
        raise

def update_json_structure(id, json_structure):
    '''
    Updates json structure and tasks. Throws NoResultFound and MultipleResultsFound.
    '''
    try:
        tree : Tree = Tree.query.filter_by(id=id).one()
        tree.update_json_structure(json_structure)
        db.session.commit()
    except Exception as e:
        print(f'Exception changing json structure of tree: {str(e)}')
        raise