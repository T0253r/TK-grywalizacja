from flask import Flask, render_template
from tree_utils import get_tree

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tree')
def tree():
    return render_template('tree.html')

# uruchamia się przez tree.js
@app.route("/tree/cytoscape")
def get_cytoscape_tree():
    return get_tree('data/drzewko.json')

if __name__ == '__main__':
    app.run(debug=True)
