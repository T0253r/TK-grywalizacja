from grywalizacja_app.database.models import db, Tree

# tutaj są operacje SELECT, INSERT i DELETE
# w models.py są metody do modyfikacji (UPDATE)

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
    Gets tree by id.
    '''
    tree = db.get_or_404(Tree, id)
    return _prettify_tree(tree)

def add_tree(name, json_structure, created_by):
    '''
    Adds a tree to database.
    '''
    tree = Tree(name=name, json_structure=json_structure, created_by=created_by)
    # add all tasks
    db.session.add(tree)
    db.session.commit()

def delete_tree(id):
    '''
    Deletes a tree from database.
    '''
    tree = get_tree(id)
    db.session.delete(tree)
    db.session.commit()