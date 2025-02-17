from functools import wraps
from flask import request, jsonify, make_response
import jwt
import datetime
from config.app_config import AppConfig
import json
from utils.factory import createGetPlayerService

def generate_token(username):
    """Generate a JWT token for the given username."""
    return jwt.encode({
        'username': username,
        'exp': datetime.datetime.now(datetime.timezone.utc) + 
               datetime.timedelta(hours=AppConfig.JWT_EXPIRATION_HOURS)
    }, AppConfig.SECRET_KEY, algorithm='HS256')

def decode_token(token):
    """Decode and validate a JWT token."""
    try:
        payload = jwt.decode(token, AppConfig.SECRET_KEY, algorithms=['HS256'])
        return make_response(payload, 200)
    except jwt.ExpiredSignatureError:
        return make_response('Token has expired', 401)
    except jwt.InvalidTokenError:
        return make_response('Invalid token', 401)

def token_required(f):
    """Decorator to protect routes with JWT authentication."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('auth_token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, AppConfig.SECRET_KEY, algorithms=['HS256'])
            request.user = data
            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 401
    return decorated

def get_player_id_by_token(token):
    token = request.cookies.get('auth_token')
    res = decode_token(token)
    if res.status_code != 200:
        return make_response('Invalid token', 401)
    
    json_string = res.data.decode('utf-8')
    token_dict = json.loads(json_string)
    email = token_dict['username']

    get_player_service = createGetPlayerService()
    return get_player_service.get_id_by_email(email)