from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import json
import os
import re

# --- App and DB Setup ---
app = Flask(__name__, template_folder='templates')
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'submissions.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- Helper for Dynamic Form ---
def get_roles_data():
    """Scans the TeamWork directory to build a dict of roles and their report items."""
    roles_data = {}
    teamwork_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'TeamWork')
    
    try:
        dir_contents = os.listdir(teamwork_path)
    except FileNotFoundError:
        print(f"Error: The '{teamwork_path}' directory was not found.")
        return {}

    role_pattern = re.compile(r'^\d_PRID_(\w+)')

    for item in sorted(dir_contents):
        match = role_pattern.match(item)
        if match:
            role_name = match.group(1).replace("_", " ") # Make name pretty
            role_dir_path = os.path.join(teamwork_path, item)
            
            if os.path.isdir(role_dir_path):
                try:
                    # Filter for relevant files, ignore hidden/system files
                    role_files = [f for f in os.listdir(role_dir_path) if os.path.isfile(os.path.join(role_dir_path, f)) and not f.startswith('.')]
                    roles_data[role_name] = sorted(role_files)
                except OSError:
                    roles_data[role_name] = [] # Handle cases where dir is not readable
    
    # Exclude the 'Supervisor' role from the selection
    if 'Supervisor' in roles_data:
        del roles_data['Supervisor']
    
    return roles_data

# --- Route to Serve the Dynamic Form ---
@app.route('/')
def form():
    """Renders the dynamic form based on the directory structure."""
    roles_data = get_roles_data()
    return render_template('dynamic_form.html', roles_data=roles_data)

# --- Database Model ---
class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    role_specific_data = db.Column(db.Text, nullable=True) # Storing as JSON string
    submitted_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f'<Submission {self.id} - {self.full_name}>'

# --- Excel Export Function ---
def export_to_excel():
    """Queries all submissions and saves them to an Excel file."""
    with app.app_context():
        try:
            submissions = Submission.query.all()
            if not submissions:
                print("No submissions to export.")
                return

            data = []
            for sub in submissions:
                sub_data = {
                    'ID': sub.id,
                    'FullName': sub.full_name,
                    'Email': sub.email,
                    'Role': sub.role,
                    'SubmittedAt': sub.submitted_at.strftime("%Y-%m-%d %H:%M:%S") if sub.submitted_at else None
                }
                if sub.role_specific_data:
                    try:
                        role_data = json.loads(sub.role_specific_data)
                        sub_data.update(role_data) # Directly use keys from form
                    except json.JSONDecodeError:
                        sub_data['RoleSpecificData_Error'] = "Invalid JSON"
                
                data.append(sub_data)

            df = pd.DataFrame(data)
            excel_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'submissions.xlsx')
            df.to_excel(excel_path, index=False)
            print(f"Successfully exported {len(submissions)} submissions to {excel_path}")

        except Exception as e:
            print(f"An error occurred during Excel export: {e}")

# --- API Route ---
@app.route('/submit', methods=['POST'])
def handle_submission():
    """Receives form data, saves to DB, and triggers Excel export."""
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()

    if not all(k in data for k in ['fullName', 'email', 'role']):
        return jsonify({"error": "Missing required fields: fullName, email, role"}), 400

    new_submission = Submission(
        full_name=data['fullName'],
        email=data['email'],
        role=data['role'],
        role_specific_data=json.dumps(data.get('roleData', {}))
    )

    try:
        db.session.add(new_submission)
        db.session.commit()
        export_to_excel()
        return jsonify({"message": "Submission successful!"}), 201
    
    except Exception as e:
        db.session.rollback()
        print(f"Database or export error: {e}")
        return jsonify({"error": "An internal error occurred."}), 500

# --- Main Runner ---
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Database tables created.")
    
    print("Starting Flask server...")
    print("Access the dynamic form at: http://127.0.0.1:5001/")
    app.run(debug=True, port=5001)
