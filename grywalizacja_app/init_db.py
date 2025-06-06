from app import app
from database.models import db, User

# to powinno utworzyć tabele i dodać 2 użytkowników
with app.app_context():
    db.create_all()
    
    # if not User.query.first():
        # admin = User(email="admin@test.com", name="Admin", is_admin=True)
        # user1 = User(email="user1@test.com", name="User1", points=100)
        # db.session.add_all([admin, user1])
        # db.session.commit()