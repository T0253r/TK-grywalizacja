import functools

from flask import Blueprint, request, jsonify, session, redirect, url_for

from grywalizacja_app.database.queries.user_tasks import get_user_tasks_by_status, change_status

admin = Blueprint('admin', __name__, url_prefix='/admin')

def admin_only(view):
    @functools.wraps(view)
    def authorize(**kwargs):
        if not session.get('user'):
            return redirect(url_for('auth.login'))
        if not session.get('is_admin'):
            return redirect(url_for('index'))
        return view(**kwargs)
    return authorize

@admin.route('/accept', methods=['POST'])
@admin_only
def accept_task():
    data = request.get_json()
    user_id = int(data.get('user_id'))
    task_id = data.get('task_id')
    change_status(user_id, task_id, 2)

    return jsonify({'status': 'success', 'message': f'Task {task_id} accepted'})

@admin.route('/reject', methods=['POST'])
@admin_only
def reject_task():
    data = request.get_json()
    user_id = int(data.get('user_id'))
    task_id = data.get('task_id')
    change_status(user_id, task_id, 0)
    return jsonify({"status": "rejected", "message": "Task has been rejected."})

@admin.route('/tasks')
@admin_only
def unfinished_tasks():
    return get_user_tasks_by_status(1)