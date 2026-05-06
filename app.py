from flask import Flask, render_template_string, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# Initialize extensions
db = SQLAlchemy()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///./orbit.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions with app
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

@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash("Invalid credentials.")
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head><title>Login | Orbit</title></head>
    <body style="font-family: sans-serif; max-width: 400px; margin: 50px auto;">
        <h1>Orbit Project Manager</h1>
        <form method="POST">
            <div style="margin: 10px 0;">
                <label>Username:</label><br>
                <input type="text" name="username" required style="width: 100%; padding: 8px;">
            </div>
            <div style="margin: 10px 0;">
                <label>Password:</label><br>
                <input type="password" name="password" required style="width: 100%; padding: 8px;">
            </div>
            <button type="submit" style="background: #007bff; color: white; padding: 10px 20px; border: none; cursor: pointer;">Login</button>
        </form>
        <p>Default: admin / admin</p>
    </body>
    </html>
    """)

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head><title>Dashboard | Orbit</title></head>
    <body style="font-family: sans-serif; max-width: 800px; margin: 50px auto;">
        <h1>Welcome, {{ current_user.username }}!</h1>
        <p>Role: {{ current_user.prid_role }}</p>
        <p>Orbit Project Manager is running successfully on Render!</p>
        <a href="/logout">Logout</a>
    </body>
    </html>
    """)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
