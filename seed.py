from app import app, db, User
from werkzeug.security import generate_password_hash

# Initial points structure based on your rules
initial_players = [
    {"name": "Player One (Rank 1)", "points": 100},
    {"name": "Player Two (Rank 2)", "points": 90},
    {"name": "Player Three (Rank 3)", "points": 85},
    {"name": "Player Four (Rank 4)", "points": 85},
    {"name": "Player Five (Rank 5)", "points": 80}, # You are placed 5th here as an example
    {"name": "Matei Ignat", "points": 80},
    {"name": "Player Seven (Rank 7)", "points": 80},
    {"name": "Player Eight (Rank 8)", "points": 80},
    {"name": "Player Nine (Rank 9)", "points": 70},
    {"name": "Player Ten (Rank 10)", "points": 70},
]

with app.app_context():
    db.create_all()
    
    # Clear existing to prevent duplicates during testing
    User.query.delete()
    
    for player in initial_players:
        # Default password is 'password' for everyone except Matei
        pwd = "mateiignat" if player["name"] == "Matei Ignat" else "password"
        u = User(
            username=player["name"], 
            password_hash=generate_password_hash(pwd),
            points=player["points"]
        )
        db.session.add(u)
    
    db.session.commit()
    print("Database seeded successfully! Matei Ignat account created.")
