from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime

db = SQLAlchemy()

# Use PostgreSQL in production, SQLite locally
DB_PATH = os.environ.get('DATABASE_URL', 'sqlite:///orbit_core.db')
if DB_PATH and DB_PATH.startswith('postgres://'):
    DB_PATH = DB_PATH.replace('postgres://', 'postgresql://', 1)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(256))
    prid_role = db.Column(db.String(32), default='PRID_UNASSIGNED')
    
    # Relationships
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
    status = db.Column(db.String(32), default='Pending') # Pending, In Progress, Completed
    progress = db.Column(db.Integer, default=0) # Progress percentage 0-100
    assigned_to_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    action = db.Column(db.String(255), nullable=False)
    target = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    user_ref = db.relationship('User', backref='audit_logs', lazy=True)

class Webhook(db.Model):
    __tablename__ = 'webhooks'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    event_type = db.Column(db.String(64), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_PATH
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Secret key for Flask-Login
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'super-secret-prid-key-012931')
    
    db.init_app(app)
    
    with app.app_context():
        # Create all tables
        db.create_all()
        # Seed an initial Supervisor if none exists
        if not User.query.filter_by(username='admin').first():
            u = User(username='admin', prid_role='PRID_1')
            u.set_password('admin')
            db.session.add(u)
            
            # Seed auditor
            u2 = User(username='auditor', prid_role='PRID_2')
            u2.set_password('password')
            db.session.add(u2)
            
            # Seed designer
            u3 = User(username='designer', prid_role='PRID_3')
            u3.set_password('password')
            db.session.add(u3)
            
            # Seed integrator
            u4 = User(username='integrator', prid_role='PRID_4')
            u4.set_password('password')
            db.session.add(u4)
            
            # Seed dba
            u5 = User(username='dba', prid_role='PRID_5')
            u5.set_password('password')
            db.session.add(u5)
            
            db.session.commit()
            print("Seeded default test users (admin / password) for each PRID role.")
