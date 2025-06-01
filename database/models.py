from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(127), unique=True, nullable=False)
    name = db.Column(db.String(63), nullable=False)
    points = db.Column(db.Integer, default=0)
    is_admin = db.Column(db.Boolean, default=False)

class Tree(db.Model):
    __tablename__ = 'trees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(127))
    json_structure = db.Column(db.JSON, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    is_public = db.Column(db.Boolean, default=False)

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    tree_id = db.Column(db.Integer, db.ForeignKey('trees.id'))
    name = db.Column(db.String(127))
    description = db.Column(db.String(511))
    points = db.Column(db.Integer)

class User_Task(db.Model):
    __tablename__ = 'user_tasks'

    id = db.Column(db.Integer, primary_key=True)
    task_id =  db.Column(db.Integer, db.ForeignKey('tasks.id'))
    user_id =  db.Column(db.Integer, db.ForeignKey('users.id'))
    status = db.Column(db.String)
    is_visible = db.Column(db.Boolean, default=False)