from flask import Blueprint, request, jsonify, session

from grywalizacja_app.database.queries.user_tasks import get_user_task, change_status
from grywalizacja_app.database.queries.tasks import get_task
from .auth import login_required

api = Blueprint('api', __name__)

def update_own_task(new_status):
    user_id = session['user']['id']
    node_id = request.json.get('task_id')
    tree_id = request.json.get('tree_id')

    task = get_task(tree_id, node_id)

    change_status(user_id, task['id'], new_status)
    return jsonify({'success': True, 'status': new_status})

@api.route('/api/user_mark', methods=['POST'])
def user_mark():
    return update_own_task(1)

@api.route('/api/user_unmark', methods=['POST'])
def user_unmark():
    return update_own_task(0)