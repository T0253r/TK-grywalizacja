import json
from flask import jsonify

def load_tree(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

# jeszcze nigdzie nie użyte
def save_tree(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# formatuje do cytoscape, czyli robi listy nodes i edges
def to_cytoscape_format(tree_data):
    nodes = [
        {
            "data": {
                "id": node["id"],
                "label": node["name"],
                "status": node["status"]
            }
        }
        for node in tree_data["nodes"]
    ]

    edges = []

    for node in tree_data["nodes"]:
        for child_id in node["children"]:
            edges.append({
                "data": {"source": node["id"], "target": child_id}
            })

    return {
        "nodes": nodes,
        "edges": edges
    }

# pobiera dane drzewka i zwraca Response
def get_tree(filename):
    data = load_tree(filename)
    return jsonify(to_cytoscape_format(data))