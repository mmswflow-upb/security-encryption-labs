from flask import Flask, render_template, request, jsonify
import psycopg2
import psycopg2.extras
import os
import bcrypt
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "change-me-in-production")

jwt = JWTManager(app)

revoked_jtis = set()

@jwt.token_in_blocklist_loader
def is_token_revoked(jwt_header, jwt_payload):
    return jwt_payload["jti"] in revoked_jtis

def get_db_connection():
	return psycopg2.connect(
		host=os.getenv("DB_HOST", "postgres"),
		port=os.getenv("DB_PORT", "5432"),
		dbname=os.getenv("POSTGRES_DB", "users"),
		user=os.getenv("POSTGRES_USER", "postgres"),
		password=os.getenv("POSTGRES_PASSWORD", "postgres")
	)

@app.route("/")
def home():
	return render_template("login.html")

@app.route("/register")
def register_page():
	return render_template("register.html")

@app.route("/dashboard")
def dashboard():
	return render_template("dashboard.html")

@app.route("/api/register", methods=["POST"])
def register():
	data = request.get_json()
	email = data.get("email", "").strip().lower()
	password = data.get("password", "")
	confirm_password = data.get("confirm_password", "")
	role = data.get("role", "student")

	if not email or not password or not confirm_password:
		return jsonify({"error": "Email and password are required"}), 400

	if password != confirm_password:
		return jsonify({"error": "Passwords don't match"}), 400

	if len(password) < 6:
		return jsonify({"error": "Password must be at least 6 characters"}), 400

	hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

	conn = get_db_connection()
	cur = conn.cursor()
	try:
		cur.execute(
			"INSERT INTO users (email, password, role) VALUES (%s, %s, %s) RETURNING id, email, role",
			(email, hashed_password, role)
		)
		new_user = cur.fetchone()
		conn.commit()

		access_token = create_access_token(identity=str(new_user[0]), additional_claims={"role": role})
		refresh_token = create_refresh_token(identity=str(new_user[0]))

		return jsonify({
			"message": "User created successfully",
			"access_token": access_token,
			"refresh_token": refresh_token
		}), 201

	except psycopg2.errors.UniqueViolation:
		conn.rollback()
		return jsonify({"error": "Email already registered"}), 409
	finally:
		cur.close()
		conn.close()

@app.route("/api/login", methods=["POST"])
def login():
	data = request.get_json()
	email = data.get("email", "").strip().lower()
	password = data.get("password", "")

	if not email or not password:
		return jsonify({"error": "Email and password are required"}), 400

	conn = get_db_connection()
	cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
	cur.execute("SELECT id, email, password, role FROM users WHERE email = %s", (email,))
	user = cur.fetchone()
	cur.close()
	conn.close()

	if user is None:
		return jsonify({"error": "Invalid email or password"}), 401

	if not bcrypt.checkpw(password.encode(), user["password"].encode()):
		return jsonify({"error": "Invalid email or password"}), 401

	access_token = create_access_token(identity=str(user["id"]), additional_claims={"role": user["role"]})
	refresh_token = create_refresh_token(identity=str(user["id"]))

	return jsonify({
		"message": "Login successful",
		"access_token": access_token,
		"refresh_token": refresh_token
	}), 200

@app.route("/api/me", methods=["GET"])
@jwt_required()
def get_profile():
	user_id = get_jwt_identity()
	conn = get_db_connection()
	cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
	cur.execute("SELECT id, email, role FROM users WHERE id = %s", (int(user_id),))
	user = cur.fetchone()
	cur.close()
	conn.close()

	if user is None:
		return jsonify({"error": "User not found"}), 404

	return jsonify({
		"id": user["id"],
		"email": user["email"],
		"role": user["role"]
	}), 200

@app.route("/api/admin", methods=["GET"])
@jwt_required()
def admin_only():
	user_id = get_jwt_identity()
	conn = get_db_connection()
	cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
	cur.execute("SELECT role FROM users WHERE id = %s", (int(user_id),))
	user = cur.fetchone()
	cur.close()
	conn.close()

	if user is None:
		return jsonify({"error": "User not found"}), 404

	if user["role"] != "admin":
		return jsonify({"error": "Admin access required"}), 403

	return jsonify({"message": "Welcome to the admin area!"}), 200

@app.route("/api/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
	user_id = get_jwt_identity()
	conn = get_db_connection()
	cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
	cur.execute("SELECT role FROM users WHERE id = %s", (int(user_id),))
	user = cur.fetchone()
	cur.close()
	conn.close()

	role = user["role"] if user else "student"
	access_token = create_access_token(identity=user_id, additional_claims={"role": role})
	return jsonify({"access_token": access_token}), 200

@app.route("/api/logout", methods=["POST"])
@jwt_required()
def logout():
	jti = get_jwt()["jti"]
	revoked_jtis.add(jti)
	return jsonify({"message": "Logged out successfully"}), 200

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000, debug=os.getenv("FLASK_DEBUG", "0") == "1")
