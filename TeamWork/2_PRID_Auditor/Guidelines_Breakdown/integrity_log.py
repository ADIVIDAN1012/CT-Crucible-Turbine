from flask_login import current_user
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import importlib
dba_module = importlib.import_module("TeamWork.5_PRID_DBA.core.database")
AuditLog = dba_module.AuditLog
db = dba_module.db

def record_system_action(action, target="Dashboard"):
    try:
        try:
            user_id = current_user.id if current_user.is_authenticated else None
        except RuntimeError:
            user_id = None
        new_log = AuditLog(user_id=user_id, action=action, target=target)
        db.session.add(new_log)
        db.session.commit()
    except Exception as e:
        import traceback
        print(f"[AUDIT ERROR] Log insertion failed: {e}")
        traceback.print_exc()
