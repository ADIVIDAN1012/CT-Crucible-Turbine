from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import requests

# Initialize extensions
db = SQLAlchemy()

# Create Flask app
app = Flask(__name__,
            template_folder='TeamWork',
            static_folder='TeamWork/3_PRID_Designer/static')

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-12345')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///./orbit.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize with app
db.init_app(app)

# Setup LoginManager
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# Define models
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(256))
    prid_role = db.Column(db.String(32), default='PRID_UNASSIGNED')
    
    tasks = db.relationship('Task', backref='assignee', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(32), default='Pending')
    progress = db.Column(db.Integer, default=0)
    assigned_to_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def update_status_from_progress(self):
        if self.progress >= 100:
            self.status = 'Completed'
        elif self.progress >= 75:
            self.status = 'Review'
        elif self.progress >= 25:
            self.status = 'In Progress'
        else:
            self.status = 'Pending'

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    action = db.Column(db.String(255), nullable=False)
    target = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Webhook(db.Model):
    __tablename__ = 'webhooks'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    event_type = db.Column(db.String(64), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

def trigger_webhooks(event_type, data):
    """Send POST requests to all active webhooks for event_type"""
    webhooks = Webhook.query.filter_by(event_type=event_type, is_active=True).all()
    for webhook in webhooks:
        try:
            requests.post(webhook.url, json=data, timeout=5)
        except:
            pass  # Silently fail to not break main app flow

def record_system_action(action, target):
    """Log an action to audit logs"""
    try:
        if current_user.is_authenticated:
            uid = current_user.id
        else:
            uid = None
        new_log = AuditLog(user_id=uid, action=action, target=target)
        db.session.add(new_log)
        db.session.commit()
    except:
        pass  # Silently fail to not break main app flow

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create tables
with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        u = User(username='admin', prid_role='PRID_1')
        u.set_password('admin')
        db.session.add(u)
        db.session.commit()

# Routes
@app.route("/")
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
        remember = request.form.get('remember') == '1'
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user, remember=remember)
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
            flash("Username already exists.")
            return redirect(url_for('register'))
        
        new_user = User(username=username, prid_role=prid_role)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user)
        flash("Registration successful!")
        return redirect(url_for('dashboard'))
    return render_template('3_PRID_Designer/register.html')

@app.route("/dashboard")
@login_required
def dashboard():
    tasks = Task.query.order_by(Task.id.desc()).all()
    users = User.query.all()
    audit_logs = AuditLog.query.order_by(AuditLog.id.desc()).limit(5).all()
    
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

@app.route("/api/update_task_progress/<int:task_id>", methods=["POST"])
@login_required
def api_update_task_progress(task_id):
    task = Task.query.get_or_404(task_id)
    progress = request.form.get("progress", type=int)
    if progress is not None and 0 <= progress <= 100:
        task.progress = progress
        task.update_status_from_progress()
        db.session.commit()
        flash(f"Task progress updated to {progress}%!")
        trigger_webhooks("task_updated", {"task_id": task.id, "title": task.title, "progress": progress, "status": task.status})
    return redirect(url_for('dashboard'))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/team")
@login_required
def team_view():
    users = User.query.all()
    return render_template('3_PRID_Designer/team.html', users=users)

@app.route("/logs")
@login_required
def logs_view():
    if current_user.prid_role != 'PRID_1':
        return redirect(url_for('dashboard'))
    all_logs = AuditLog.query.order_by(AuditLog.id.desc()).all()
    return render_template('2_PRID_Auditor/full_logs.html', logs=all_logs)

@app.route("/api/create_task", methods=["POST"])
@login_required
def api_create_task():
    if current_user.prid_role != 'PRID_1':
        return redirect(url_for('dashboard'))
    title = request.form.get("title")
    description = request.form.get("description")
    new_task = Task(title=title, description=description)
    db.session.add(new_task)
    db.session.commit()
    flash("Task created!")
    trigger_webhooks("task_created", {"task_id": new_task.id, "title": title, "description": description})
    return redirect(url_for('dashboard'))

@app.route("/api/delete_task/<int:task_id>", methods=["POST"])
@login_required
def api_delete_task(task_id):
    if current_user.prid_role != 'PRID_1':
        return redirect(url_for('dashboard'))
    task = Task.query.get_or_404(task_id)
    task_title = task.title
    db.session.delete(task)
    db.session.commit()
    flash("Task deleted!")
    trigger_webhooks("task_deleted", {"task_title": task_title})
    return redirect(url_for('dashboard'))

@app.route("/api/add_webhook", methods=["POST"])
@login_required
def api_add_webhook():
    if current_user.prid_role not in ['PRID_1', 'PRID_4']:
        return redirect(url_for('dashboard'))
    webhook_url = request.form.get("webhook_url")
    if webhook_url:
        new_hook = Webhook(url=webhook_url, event_type="task_update")
        db.session.add(new_hook)
        db.session.commit()
        flash(f"Webhook added: {webhook_url}")
    return redirect(url_for('dashboard'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
