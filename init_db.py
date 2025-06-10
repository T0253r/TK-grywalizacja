from grywalizacja_app import create_app
from grywalizacja_app.extensions import db

if __name__ == '__main__':
    app = create_app()

    with app.app_context():
        db.create_all()
