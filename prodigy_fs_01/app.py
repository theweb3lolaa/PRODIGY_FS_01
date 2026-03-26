from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app=Flask(__name__)
app.secret_key = "your_secret_key_here"

# --- Database setup ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- User model ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password_hash = db.Column(db.String(200), nullable=False)

# --- Initialize database ---
with app.app_context():
    db.create_all()  # Creates users.db and the table if it doesn't exist

# --- Routes ---
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash("Passwords do not match", "error")
            return redirect(url_for('register'))

        # Check if user/email exists
        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            flash("Username or email already exists", "error")
            return redirect(url_for('register'))

        # Hash the password before storing
        password_hash = generate_password_hash(password)

        # Create new user and add to DB
        new_user = User(username=username, email=email, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully!", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            session['user'] = user.username
            flash(f"Welcome, {user.username}!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password", "error")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        flash("Please log in first", "error")
        return redirect(url_for('login'))

    # Get all registered users from the database
    users = User.query.all()
    return render_template('dashboard.html', username=session['user'], users=users)

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Logged out successfully", "success")
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()