from grywalizacja_app import create_app
from grywalizacja_app.extensions import db
from grywalizacja_app.database.queries.trees import add_tree
import json

if __name__ == '__main__':
    app = create_app()

    with app.app_context():
        db.create_all()

        for file_name, name in [
            ('data/tree1.json', 'Tree 1'),
            ('data/tree2.json', 'Tree 2'),
        ]:
            with open(file_name, encoding='utf-8') as f:
                json_structure = json.load(f)
            add_tree(name, json_structure, None, True)

        print("Showcase config completed")