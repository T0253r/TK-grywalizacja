from app import app
from database.models import db, User

# to powinno utworzyć tabele i dodać 2 użytkowników
with app.app_context():
    db.create_all()
    
    if not User.query.first():
        admin = User(email="admin@test.com", name="Admin", is_admin=True)
        user1 = User(email="user1@test.com", name="User1", points=100)
        user2 = User(email="user2@test.com", name="user_efgh", points=100)
        user3 = User(email="user3@test.com", name="systematic_chaos", points=500)
        db.session.add_all([admin, user1, user2, user3])
        db.session.commit()