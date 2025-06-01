from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(127), unique=True, nullable=False)
    name = db.Column(db.String(63), nullable=False)
    points = db.Column(db.Integer, default=0)
    is_admin = db.Column(db.Boolean, default=False)

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
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    is_public = db.Column(db.Boolean, default=False)

    def make_public(self):
        self.is_public = True
        db.session.commit()
    
    def change_name(self, new_name):
        self.name = new_name
        db.session.commit()
    
    def update_json_structure(self, json_file):
        self.json_structure = json_file
        # updating all the tasks
        db.session.commit()

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