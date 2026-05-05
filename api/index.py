import os
import sys
import importlib
from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

# Append the current directory so modules in TeamWork/ can be resolved
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Dynamic imports
dba_module = importlib.import_module("TeamWork.5_PRID_DBA.core.database")
db = dba_module.db
init_db = dba_module.init_db
User = dba_module.User
Task = dba_module.Task
AuditLog = dba_module.AuditLog
Webhook = dba_module.Webhook

supervisor_module = importlib.import_module("TeamWork.1_PRID_Supervisor.turbine")
require_prid = supervisor_module.require_prid

auditor_module = importlib.import_module("TeamWork.2_PRID_Auditor.Guidelines_Breakdown.integrity_log")
record_system_action = auditor_module.record_system_action

integrator_module = importlib.import_module("TeamWork.4_PRID_Integrator.modules.api_ext")
process_webhook = integrator_module.process_webhook

# Setup Flask
app = Flask(__name__, 
            template_folder="../TeamWork", 
            static_folder="../TeamWork/3_PRID_Designer/static")

# Setup DB
init_db(app)

# Setup LoginManager
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# --- AUTHENTICATION ROUTES ---

@app.route("/", methods=["GET"])
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            remember = request.form.get('remember') == '1'
            login_user(user, remember=remember)
            # Log action
            record_system_action("User authenticated successfully.", target="Login")
            return redirect(url_for('dashboard'))
        flash("Invalid credentials.")
    return render_template('3_PRID_Designer/login.html')

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == "POST":
        username = request.form.get("username")
        prid_role = request.form.get("prid_role")
        password = request.form.get("password")
        
        if User.query.filter_by(username=username).first():
            flash("Username ID already onboarded.")
            return redirect(url_for('register'))
            
        new_user = User(username=username, prid_role=prid_role)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        # Auditor track
        record_system_action(f"Registered new PRID profile: {username} ({prid_role})", target="System Reg")
        
        # Auto-login the new user so they don't have to enter their password twice
        login_user(new_user)
        flash("Registration successful. PRID linked to main orchestrator.")
        return redirect(url_for('dashboard'))
    return render_template('3_PRID_Designer/register.html')

@app.route("/logout")
@login_required
def logout():
    record_system_action("Terminated user session.", target="System Logout")
    logout_user()
    return redirect(url_for('login'))


# --- DASHBOARD & CORE ROUTES ---

@app.route("/dashboard")
@login_required
def dashboard():
    tasks = Task.query.order_by(Task.id.desc()).all()
    users = User.query.all()
    audit_logs = AuditLog.query.order_by(AuditLog.id.desc()).limit(5).all()
    
    # Calculate Completion Metrics
    total_tasks = len(tasks)
    if total_tasks > 0:
        completion_pc = int(sum(t.progress for t in tasks) / total_tasks)
    else:
        completion_pc = 0
    
    return render_template('1_PRID_Supervisor/dashboard.html', 
                           tasks=tasks, 
                           users=users, 
                           audit_logs=audit_logs,
                           completion_pc=completion_pc)

@app.route("/team")
@login_required
def team_view():
    users = User.query.all()
    return render_template('3_PRID_Designer/team.html', users=users)

@app.route("/logs")
@login_required
@require_prid("PRID_1") # Full logs for Supervisor
def logs_view():
    all_logs = AuditLog.query.order_by(AuditLog.id.desc()).all()
    return render_template('2_PRID_Auditor/full_logs.html', logs=all_logs)

@app.route("/api/create_task", methods=["POST"])
@login_required
@require_prid("PRID_1")  # Only supervisors can generate assignments
def api_create_task():
    title = request.form.get("title")
    description = request.form.get("description")
    
    new_task = Task(title=title, description=description)
    db.session.add(new_task)
    db.session.commit()
    
    record_system_action(f"Generated new task: {title}", target="Task Management")
    flash("Successfully initialized new task protocol.")
    return redirect(url_for('dashboard'))

@app.route("/api/update_task_status/<int:task_id>", methods=["POST"])
@login_required
def api_update_task_status(task_id):
    task = Task.query.get_or_404(task_id)
    task.status = "Completed"
    task.progress = 100
    db.session.commit()
    
    record_system_action(f"Marked task Completed: {task.title}", target="Tasks")
    flash(f"Task marked complete!")
    return redirect(url_for('dashboard'))

@app.route("/api/update_task_progress/<int:task_id>", methods=["POST"])
@login_required
def api_update_task_progress(task_id):
    task = Task.query.get_or_404(task_id)
    progress = request.form.get("progress", type=int)
    if progress is not None and 0 <= progress <= 100:
        task.progress = progress
        if progress == 100:
            task.status = "Completed"
        elif progress > 0:
            task.status = "In Progress"
        db.session.commit()
        record_system_action(f"Updated task progress to {progress}%: {task.title}", target="Tasks")
        flash(f"Task progress updated to {progress}%!")
    return redirect(url_for('dashboard'))

@app.route("/api/delete_task/<int:task_id>", methods=["POST"])
@login_required
@require_prid("PRID_1")
def api_delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    
    record_system_action(f"Deleted task: {task.title}", target="Tasks")
    flash("Task successfully removed.")
    return redirect(url_for('dashboard'))

@app.route("/api/add_webhook", methods=["POST"])
@login_required
@require_prid("PRID_4")  # Only integrator or supervisor can add webhooks
def api_add_webhook():
    webhook_url = request.form.get("webhook_url")
    if webhook_url:
        new_hook = Webhook(url=webhook_url, event_type="general.event")
        db.session.add(new_hook)
        db.session.commit()
        
        record_system_action(f"Mounted webhook: {webhook_url}", target="API Ext")
        flash(f"External Integrator mounted at {webhook_url}.")
    return redirect(url_for('dashboard'))


if __name__ == "__main__":
    app.run(debug=True, port=5001)
