from functools import wraps
from flask import abort, jsonify
from flask_login import current_user
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import importlib
dba_module = importlib.import_module("TeamWork.5_PRID_DBA.core.database")
UserLog = dba_module.AuditLog
db = dba_module.db

def log_unauthorized_access(prid_role, endpoint):
    try:
        try:
            uid = current_user.id if current_user.is_authenticated else None
        except RuntimeError:
            uid = None
        new_log = UserLog(user_id=uid, action=f"DENIED ACCESS to {endpoint}", target=prid_role)
        db.session.add(new_log)
        db.session.commit()
    except Exception as e:
        print(f"[AUDIT ERROR] Failed to log unauthorized access: {e}")

def require_prid(required_role):
    """
    Flask route decorator.
    Enforces that the current authenticated user has the necessary PRID role.
    PRID_1 (Supervisor) has universal access override.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return jsonify({"error": "Authentication required."}), 401
                
            # PRID_1 is the Supervisor and has override capabilities
            if current_user.prid_role == 'PRID_1':
                return f(*args, **kwargs)
                
            if current_user.prid_role != required_role:
                log_unauthorized_access(required_role, f.__name__)
                return jsonify({
                    "error": "Security Breach Prevented", 
                    "message": f"User role {current_user.prid_role} is DENIED access to {required_role} resources."
                }), 403
                
            return f(*args, **kwargs)
        return decorated_function
    return decorator
