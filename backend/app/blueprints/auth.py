from datetime import datetime
from functools import wraps
from flask import Blueprint, jsonify, request, session, current_app
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token

from app import db
from app.models import User, UserRole

auth_bp = Blueprint('auth', __name__)


def get_current_user_from_session():
    user_id = session.get('user_id')
    if not user_id:
        return None
    return User.query.get(user_id)


@auth_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'service': 'auth'}), 200


@auth_bp.route('/login', methods=['POST'])
def login():
    """Google OAuth login endpoint."""
    payload = request.get_json() or {}
    id_token_value = payload.get('id_token')

    if not id_token_value:
        return jsonify({'error': 'Missing id_token'}), 400

    try:
        client_id = current_app.config.get('GOOGLE_CLIENT_ID')
        id_info = id_token.verify_oauth2_token(id_token_value, google_requests.Request(), client_id)
    except ValueError as exc:
        return jsonify({'error': 'Invalid id_token', 'details': str(exc)}), 401

    google_id = id_info.get('sub')
    email = id_info.get('email')
    name = id_info.get('name') or email
    picture = id_info.get('picture')

    if not google_id or not email:
        return jsonify({'error': 'Invalid Google token payload'}), 400

    user = User.query.filter_by(google_id=google_id).first()
    if not user:
        user = User(
            google_id=google_id,
            email=email,
            name=name,
            profile_picture=picture,
            role=UserRole.GENERAL_USER.value,
        )
        db.session.add(user)
        db.session.commit()
    else:
        user.email = email
        user.name = name
        user.profile_picture = picture
        db.session.commit()

    session.clear()
    session['user_id'] = user.id
    session.permanent = True

    return jsonify({'user': user.to_dict()}), 200


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Clear user session."""
    session.clear()
    return jsonify({'message': 'Logged out'}), 200


@auth_bp.route('/user', methods=['GET'])
def get_current_user():
    """Return current logged-in user profile."""
    user = get_current_user_from_session()
    if not user:
        return jsonify({'user': None}), 200
    return jsonify({'user': user.to_dict()}), 200


def login_required(f):
    """Decorator to require authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not get_current_user_from_session():
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function


def role_required(*roles):
    """Decorator to require specific user roles."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = get_current_user_from_session()
            if not user or user.role not in roles:
                return jsonify({'error': 'Forbidden'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator
