from flask import Flask, session, render_template, flash, redirect, url_for, request
import psycopg2
import os
from argon2 import PasswordHasher
from functools import wraps

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "changemelater")
ph = PasswordHasher()

def get_db_connection():
	return psycopg2.connect(
		host=os.getenv("DB_HOST", "localhost"),
		port="5432",
		dbname="users",
		user="postgres",
		password=os.getenv("DB_PASSWORD", "postgres")
	)

def login_required(view_func):
	@wraps(view_func)
	def wrapper(*args, **kwargs):
		if "user_id" not in session:
			flash("You are not logged in")
			return redirect(url_for("login"))
		return view_func(*args, **kwargs)
	return wrapper

@app.route("/")
def home():
	if "user_id" in session:
		return redirect(url_for("dashboard"))
	return redirect(url_for("login"))

@app.route("/dashboard")
@login_required
def dashboard():
	return render_template(
		"dashboard.html",
		email=session.get("username"),
		role=session.get("role", "user")
	)

@app.route("/register", methods=["GET", "POST"])
def register():
	if request.method == "GET":
		return render_template("register.html")
	elif request.method == "POST":
		email = request.form.get("email").strip().lower()
		password = request.form.get("password")		
		confirm_password = request.form.get("confirm_password")
		role = request.form.get("role", "student")
		if not email or not password or not confirm_password:
			flash("Email and password are required")
			return render_template("register.html")

		if password != confirm_password:
			flash("Passwords don't match")
			return render_template("register.html")			

		conn = None
		cur = None

		hashed_password = ph.hash(password)

		conn = get_db_connection()
		cur = conn.cursor()
		cur.execute(
			"""
			INSERT into users (username, password, role)
			VALUES(%s, %s, %s)
			RETURNING id, username, role
			""",
			(email, hashed_password, role)
		)
		new_user = cur.fetchone()
		conn.commit()

		print(new_user)
		session["user_id"] = new_user[0] # id
		session["username"] = new_user[1] # username
		session["role"] = new_user[2] # role

		cur.close()
		conn.close()

		flash("User created.")
		return redirect(url_for("dashboard"))

@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		email = request.form.get("email").strip().lower()
		password = request.form.get("password")

		if not email or not password:
			flash("Email and password are required")
			return render_template("login.html")

		conn = None
		cur = None
		conn = get_db_connection()
		cur = conn.cursor()
		cur.execute(
			"""
			SELECT id, username, password, role FROM users WHERE username = %s
			""",
			(email,)
		)
		user = cur.fetchone()
		if user is None:
			flash("Invalid email or password.")
			return render_template("login.html")
		
		# user is a tuple: (id, username, password, role)
		stored_hash = user[2]
		try:
			ph.verify(stored_hash, password)
		except Exception as ex:
			flash("Invalid email or password")
			return render_template("login.html")
		
		session["user_id"] = user[0]
		session["username"] = user[1]
		session["role"] = user[3]

		cur.close()
		conn.close()

		flash("Login ok")
		return redirect(url_for("dashboard"))

	elif request.method == "GET":
		return render_template("login.html")

@app.route("/logout")
def logout():
	session.clear()
	flash("You have been logged out.")
	return redirect(url_for("login"))

@app.route("/admin")
@login_required
def admin():
	if session.get("role") != "admin":
		flash("Access denied. Admin only.")
		return redirect(url_for("dashboard"))
	return render_template("admin.html")

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000, debug=True)