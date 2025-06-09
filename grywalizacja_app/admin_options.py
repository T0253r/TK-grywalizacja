from flask import Blueprint, request, jsonify

from grywalizacja_app.database.queries.user_tasks import get_user_tasks_by_status, change_status

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/accept', methods=['POST'])
def accept_task():
    data = request.get_json()
    user_id = int(data.get('user_id'))
    task_id = data.get('task_id')
    change_status(user_id, task_id, 2)

    return jsonify({'status': 'success', 'message': f'Task {task_id} accepted'})

@admin.route('/reject', methods=['POST'])
def reject_task():
    data = request.get_json()
    user_id = data.get('user_id')
    task_id = data.get('task_id')
    change_status(user_id, task_id, 0)
    return jsonify({"status": "rejected", "message": "Task has been rejected."})

@admin.route('/tasks')
def unfinished_tasks():
    return get_user_tasks_by_status(1)