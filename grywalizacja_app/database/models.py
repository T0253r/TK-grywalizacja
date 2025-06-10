from datetime import datetime, timezone
from sqlalchemy import select, func
from sqlalchemy.ext.hybrid import hybrid_property
from grywalizacja_app.extensions import db

class User(db.Model):
    __tablename__ = 'users'

    discord_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(127), unique=True, nullable=False)
    name = db.Column(db.String(63), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    @hybrid_property
    def points(self):
        return sum(
            user_task.task.points
            for user_task in self.user_tasks
            if user_task.status == 2
        )

    @points.expression
    def points(cls):
        return (
            select(func.coalesce(func.sum(Task.points), 0))
            .select_from(cls)
            .join(User_Task, User_Task.user_id == cls.discord_id)
            .join(Task, User_Task.task_id == Task.id)
            .where(User_Task.status == 2)
            .label('user_points')
        )

    def make_admin(self):
        self.is_admin = True
        db.session.commit()
    
    def revoke_admin(self):
        self.is_admin = False
        db.session.commit()
    
    def change_name(self, new_name):
        self.name = new_name
        db.session.commit()

class Tree(db.Model):
    __tablename__ = 'trees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(127))
    json_structure = db.Column(db.JSON, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.discord_id'))
    is_public = db.Column(db.Boolean, default=False)

    def make_public(self):
        self.is_public = True
        db.session.commit()
    
    def change_name(self, new_name):
        self.name = new_name
        db.session.commit()
    
    def update_json_structure(self, json_structure):
        self.json_structure = json_structure
        # updating all the tasks
        db.session.commit()

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    tree_id = db.Column(db.Integer, db.ForeignKey('trees.id'))
    node_id = db.Column(db.Integer)
    name = db.Column(db.String(127))
    description = db.Column(db.String(511))
    points = db.Column(db.Integer)

    def change_name(self, new_name):
        self.name = new_name
        db.session.commit()
    
    def change_description(self, new_description):
        self.description = new_description
        db.session.commit()
    
    def change_points(self, new_points):
        self.points = new_points
        db.session.commit()

class User_Task(db.Model):
    __tablename__ = 'user_tasks'

    task_id =  db.Column(db.Integer, db.ForeignKey('tasks.id'), primary_key=True)
    user_id =  db.Column(db.Integer, db.ForeignKey('users.discord_id'), primary_key=True)
    status = db.Column(db.Integer, default=0) # 0 - not done, 1 - pending, 2 - accepted
    is_visible = db.Column(db.Boolean, default=False)

    user = db.relationship('User', backref=db.backref('user_tasks', lazy='dynamic'))
    task = db.relationship('Task', backref=db.backref('user_tasks', lazy='dynamic'))

    def change_status(self, new_status):
        self.status = new_status
        db.session.commit()

    def change_visibility(self, visibility):
        self.is_visible = visibility
        db.session.commit()