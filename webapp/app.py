# webapp/app.py
from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import requests
import os

app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://gameuser:gamepass@db:5432/gamedb')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar SQLAlchemy
db = SQLAlchemy(app)

# Modelos
class Player(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

class Challenge(db.Model):
    __tablename__ = 'challenges'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    points = db.Column(db.Integer, default=10)

class PlayerProgress(db.Model):
    __tablename__ = 'player_progress'
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'))
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenges.id'))
    completed_at = db.Column(db.DateTime, server_default=db.func.now())
    attempts = db.Column(db.Integer, default=1)

# Rutas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register_player():
    data = request.get_json()
    username = data.get('username')
    
    if not username:
        return jsonify({'status': 'error', 'message': 'Username is required'}), 400
    
    try:
        player = Player(username=username)
        db.session.add(player)
        db.session.commit()
        return jsonify({'status': 'success', 'player_id': player.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': 'Username already exists'}), 400

@app.route('/check_service1')
def check_service1():
    player_id = request.args.get('player_id')
    try:
        response = requests.get('http://service1:5001/status')
        if response.status_code == 200 and player_id:
            record_progress(player_id, 1)
        return jsonify(response.json())
    except:
        return jsonify({'status': 'error', 'message': 'No se pudo conectar con el Servicio 1'})

@app.route('/check_service2')
def check_service2():
    player_id = request.args.get('player_id')
    try:
        response = requests.get('http://service2:5002/status')
        if response.status_code == 200 and player_id:
            record_progress(player_id, 2)
        return jsonify(response.json())
    except:
        return jsonify({'status': 'error', 'message': 'No se pudo conectar con el Servicio 2'})

def record_progress(player_id, challenge_id):
    try:
        progress = PlayerProgress.query.filter_by(
            player_id=player_id,
            challenge_id=challenge_id
        ).first()
        
        if progress:
            progress.attempts += 1
        else:
            progress = PlayerProgress(
                player_id=player_id,
                challenge_id=challenge_id
            )
            db.session.add(progress)
        
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error recording progress: {e}")

@app.route('/leaderboard')
def get_leaderboard():
    try:
        leaderboard = db.session.query(
            Player.username,
            db.func.count(PlayerProgress.id).label('challenges_completed'),
            db.func.sum(Challenge.points).label('total_points')
        ).join(
            PlayerProgress, Player.id == PlayerProgress.player_id
        ).join(
            Challenge, PlayerProgress.challenge_id == Challenge.id
        ).group_by(Player.username).order_by(
            db.text('total_points DESC')
        ).limit(10).all()
        
        return jsonify([{
            'username': row[0],
            'challenges_completed': row[1],
            'total_points': row[2] or 0
        } for row in leaderboard])
    except Exception as e:
        print(f"Error getting leaderboard: {e}")
        return jsonify([])

# Inicialización de la base de datos
with app.app_context():
    try:
        db.create_all()
        
        # Verificar si ya existen desafíos
        if Challenge.query.count() == 0:
            challenges = [
                Challenge(name='Servicio Básico', description='Conectar con el primer servicio de la red', points=10),
                Challenge(name='Servicio Avanzado', description='Establecer conexión con el segundo servicio', points=20)
            ]
            db.session.bulk_save_objects(challenges)
            db.session.commit()
    except Exception as e:
        print(f"Error initializing database: {e}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)