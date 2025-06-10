from flask import Blueprint, request, jsonify, session
from grywalizacja_app.database.queries.user_tasks import get_user_task
from .auth import login_required

api = Blueprint('api', __name__)

def update_own_task(new_status):
    user_id = session['user']['id']
    task_id = request.json.get('task_id')

    user_task = get_user_task(task_id, user_id) #dostaje tu 404, nie wiem czy to ja cos popsulem w bazie czy gdzie indziej jest problem
    print(user_task)

    if user_task:
        user_task.change_status(new_status)
        return jsonify({'success': True, 'status': new_status})
    return jsonify({'success': False, 'error': 'Task not found'}), 404

@api.route('/api/user_mark', methods=['POST'])
def user_mark():
    return update_own_task(1)

@api.route('/api/user_unmark', methods=['POST'])
def user_unmark():
    return update_own_task(0)