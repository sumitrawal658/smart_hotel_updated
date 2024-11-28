from functools import wraps
from flask import current_app, request, jsonify
from .permissions import ROLE_PERMISSIONS
from .utils import get_current_user

def require_permission(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get current user from session/token
            current_user = get_current_user()
            
            if not current_user:
                return jsonify({'error': 'Authentication required'}), 401
                
            if permission not in ROLE_PERMISSIONS[current_user.role]:
                return jsonify({'error': 'Permission denied'}), 403
                
            return f(*args, **kwargs)
        return decorated_function
    return decorator 