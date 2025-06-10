from grywalizacja_app import create_app
from grywalizacja_app.database.models import db
from grywalizacja_app.database.queries.trees import add_tree
import json

if __name__ == '__main__':
    app = create_app()
    with app.app_context():

        for fname, name in [
            ('data/tree1.json', 'Tree 1'),
            ('data/tree2.json', 'Tree 2'),
        ]:
            with open(fname, encoding='utf-8') as f:
                json_structure = json.load(f)
            add_tree(name, json_structure, None)
        print("Trees added!")