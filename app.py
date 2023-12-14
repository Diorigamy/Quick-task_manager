# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session, g
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash 
from flask.cli import with_appcontext
from datetime import datetime
#from flask_talisman import Talisman
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from sqlalchemy.exc import IntegrityError

# Create a Flask application instance
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'  # Configure SQLite database URI
app.config['SECRET_KEY'] = 't6rtuuvccPaveho$surziflqlmer$dbtxemcxlvekyfmtM3h'  # Secret key for session
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy and set up login manager
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Define User and Task models
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    full_name = db.Column(db.String(150))
    age = db.Column(db.Integer)
    tasks = db.relationship('Task', backref='user', lazy=True)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    alert_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    details = db.Column(db.Text)
    priority = db.Column(db.String(20), nullable=False)

# SQLite Database Configuration
DATABASE = 'tasks.db'

# Initialize the database
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# CLI command to initialize the database
@app.cli.command('init-db')
@with_appcontext
def init_db_command():
    """Initialize the database."""
    init_db()
    print('Initialized the database.')

# Function to get a SQLite database connection
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

# Teardown function to close the database connection
@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# Example user_loader callback
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Unauthorized handler for login manager
@login_manager.unauthorized_handler
def unauthorized():
    flash('You must be logged in to access this page.', 'error')
    return redirect(url_for('login', next=request.url))

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Retrieve user registration form data
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Additional fields for user registration
        full_name = request.form['full_name']
        age = request.form['age']

        # Hash the password for security
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Create a new User instance
        new_user = User(username=username, email=email, password=hashed_password, full_name=full_name, age=age)

        try:
            # Add the new user to the database
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! You can now log in.', 'success')
            print("Registration successful!")
            return redirect(url_for('login'))

        except IntegrityError as e:
            # Handle case where email address is already in use
            db.session.rollback()
            flash('Error: Email address already in use. Please choose a different email.', 'error')

    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Retrieve login form data
        username = request.form['username']
        password = request.form['password']

        # Find the user by username
        user = User.find_by_username(username)
        
        if user is None or not check_password_hash(user.password, password):
            # Display error message for incorrect credentials
            flash('Incorrect username or password.', 'error')
        else:
            # Log in the user and set session variables
            login_user(user)
            session['user_id'] = user.id
            flash('Login successful!', 'success')

            # Get the next URL or redirect to the index if it doesn't exist
            next_url = request.args.get('next') or url_for('index')
            return redirect(next_url)

    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    # Clear session variables for user logout
    session.clear()
    return redirect(url_for('index'))

# Index (Tasks) route
@app.route('/')
@login_required
def index():
    if 'user_id' in session:
        # Retrieve user tasks for display on the index page
        user_id = session['user_id']
        db = get_db()
        cur = db.execute('SELECT * FROM tasks WHERE user_id = ? ORDER BY id DESC', (user_id,))
        tasks = cur.fetchall()
        return render_template('index.html', tasks=tasks)
    return redirect(url_for('login'))

# Task routes
# Create Task route
@app.route('/tasks/create', methods=['GET', 'POST'])
def create_task():
    if request.method == 'POST':
        # Retrieve task creation form data
        user_id = session.get('user_id')
        due_datetime = request.form['due_date']
        alert_datetime = request.form['alert_date']
        description = request.form['description']
        details = request.form['details']
        priority = request.form['priority']

        try:
            # Convert date and time strings to datetime objects
            due_date = datetime.strptime(due_datetime, '%m/%d/%Y %H:%M')
            alert_date = datetime.strptime(alert_datetime, '%m/%d/%Y %H:%M')

            # Check if alert date is before due date
            if alert_date > due_date:
                raise ValueError("Alert date should not be after due date")

            # Insert the new task into the database
            db = get_db()
            db.execute(
                'INSERT INTO tasks (user_id, due_date, alert_date, description, details, priority) VALUES (?, ?, ?, ?, ?, ?)',
                (user_id, due_date, alert_date, description, details, priority)
            )
            db.commit()
            flash('Task created successfully.')
            return redirect(url_for('index'))

        except ValueError as e:
            # Display error message for invalid date or time format
            flash(f'Error creating task: {str(e)}')

    return render_template('create_task.html')

# Edit Task route
@app.route('/tasks/<int:task_id>/edit', methods=['GET', 'POST'])
def edit_task(task_id):
    db = get_db()
    task = db.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()

    if task is None:
        # Display error message if task is not found
        flash('Task not found.')
        return redirect(url_for('index'))

    if request.method == 'POST':
        # Retrieve edited task data from form
        due_date = request.form['due_date']
        alert_datetime = request.form['alert_date']
        description = request.form['description']
        details = request.form['details']
        priority = request.form['priority']

        # Convert date and time strings to datetime objects
        due_date = datetime.strptime(due_date, '%Y-%m-%d %H:%M:%S')
        alert_datetime = datetime.strptime(alert_datetime, '%Y-%m-%d %H:%M:%S')

        # Update the task in the database
        db.execute(
            'UPDATE tasks SET due_date=?, alert_date=?, description=?, details=?, priority=? WHERE id=?',
            (due_date, alert_datetime, description, details, priority, task_id)
        )
        db.commit()
        flash('Task updated successfully.')
        return redirect(url_for('index'))

    return render_template('edit_task.html', task=task)

# Delete Task route
@app.route('/tasks/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    db = get_db()
    db.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    db.commit()
    flash('Task deleted successfully.')
    return redirect(url_for('index'))

# View Task route
@app.route('/tasks/<int:task_id>')
def view_task(task_id):
    db = get_db()
    task = db.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()

    if task is None:
        # Display error message if task is not found
        flash('Task not found.')
        return redirect(url_for('index'))

    return render_template('view_task.html', task=task)

# Run the application if executed as the main module
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

