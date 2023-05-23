from functools import wraps
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import uuid
import jwt
# Initialize Flask app
app = Flask(__name__)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:karimbkh@localhost/bank'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy database
db = SQLAlchemy(app)

# Configure JWT secret key
app.config['SECRET_KEY'] = 'AOSPROJECTAUTHSERVICESECRETKEY'


# User model
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def __init__(self, id, username, password, email):
        self.id = id
        self.username = username
        self.password = password
        self.email = email


# Register route
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(id=str(uuid.uuid4()), username=data['username'], password=hashed_password, email=data['email'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully.'}), 201


# Login route
@app.route('/login', methods=['POST'])
def login():
    auth = request.authorization
    print(auth)

    if not auth or not auth.username or not auth.password:
        print("hereeee")
        return jsonify({'message': 'Invalid credentials.'}), 401

    user = User.query.filter_by(username=auth.username).first()

    if not user:
        print(user)
        return jsonify({'message': 'Invalid credentials.'}), 401

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'id': user.id, 'exp': datetime.utcnow() + timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token': token}), 200

    return jsonify({'message': 'Invalid credentials.'}), 401


def authenticate(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.get('token')

        if not token:
            return jsonify({'message': 'Missing token.'}), 401

        try:
            data =jwt.decode(token, app.config['SECRET_KEY'])

            kwargs['user_id'] = data['id']  # Pass the user ID to the decorated function
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired.'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token.1'}), 401

        return func(*args, **kwargs)

    return decorated


# Verify route
@app.route('/verify', methods=['POST'])
def verify_token():
    data = request.get_json()

    token = data.get("token")         


    if not token:
        return jsonify({'message': 'Missing token.'}), 401

    try:
        jwt.decode(token, app.config['SECRET_KEY'])
        print(jwt.decode(token, app.config['SECRET_KEY']))
        return jsonify({'message': 'Token is valid.'}), 200
    except jwt.ExpiredSignatureError:
        print(jwt.ExpiredSignatureError)
        return jsonify({'message': 'Token has expired.'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token2.'}), 401


# Run the application
if __name__ == '__main__':
    app.run()
