from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///squash4all.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- MODELS ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    points = db.Column(db.Integer, default=0)
    last_golden_match = db.Column(db.DateTime, nullable=True)

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    challenger_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    opponent_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.String(20), default='pending') # pending, confirmed
    is_golden = db.Column(db.Boolean, default=False)
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow)

# --- ROUTES ---
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data.get('username')).first()
    if user and check_password_hash(user.password_hash, data.get('password')):
        return jsonify({"id": user.id, "username": user.username, "points": user.points, "last_golden_match": user.last_golden_match})
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    users = User.query.order_by(User.points.desc(), User.id.asc()).all()
    return jsonify([{"id": u.id, "username": u.username, "points": u.points} for u in users])

@app.route('/submit_result', methods=['POST'])
def submit_result():
    data = request.json
    match = Match(
        challenger_id=data['challenger_id'],
        opponent_id=data['opponent_id'],
        is_golden=data.get('is_golden', False)
    )
    db.session.add(match)
    db.session.commit()
    return jsonify({"message": "Result submitted for confirmation!"})

@app.route('/confirm_result/<int:match_id>', methods=['POST'])
def confirm_result(match_id):
    match = Match.query.get_or_404(match_id)
    if match.status == 'confirmed':
        return jsonify({"error": "Already confirmed"}), 400
        
    match.status = 'confirmed'
    challenger = User.query.get(match.challenger_id)
    opponent = User.query.get(match.opponent_id)
    
    # Ranked players to determine point reward based on opponent's rank
    leaderboard = User.query.order_by(User.points.desc()).all()
    opponent_rank = leaderboard.index(opponent) + 1

    if match.is_golden:
        challenger.points = opponent.points + 1
        challenger.last_golden_match = datetime.utcnow()
    else:
        # Calculate points based on opponent's rank
        if opponent_rank == 1: challenger.points += 100
        elif opponent_rank == 2: challenger.points += 90
        elif 3 <= opponent_rank <= 4: challenger.points += 85
        elif 5 <= opponent_rank <= 8: challenger.points += 80
        elif 9 <= opponent_rank <= 16: challenger.points += 70
        else: challenger.points += 50 # Default for lower ranks

    db.session.commit()
    return jsonify({"message": "Match confirmed and points updated!"})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
