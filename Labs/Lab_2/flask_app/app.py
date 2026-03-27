import os
import bcrypt
import psycopg2
import psycopg2.extras
from flask import Flask, request, session, redirect, url_for, render_template
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "change-me")


def get_db():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "postgres"),
        port=int(os.getenv("DB_PORT", 5432)),
        dbname=os.getenv("DB_NAME", "lab_db"),
        user=os.getenv("DB_USER", "lab_user"),
        password=os.getenv("DB_PASSWORD", "lab_password"),
    )


@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    username = request.form["username"].strip()
    password = request.form["password"].encode()

    # hash the password with bcrypt (salt is generated automatically)
    hashed = bcrypt.hashpw(password, bcrypt.gensalt()).decode()

    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
            (username, hashed),
        )
        conn.commit()
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        return render_template("register.html", error="Username already taken.")
    finally:
        cur.close()
        conn.close()

    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form["username"].strip()
    password = request.form["password"].encode()

    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user is None or not bcrypt.checkpw(password, user["password_hash"].encode()):
        return render_template("login.html", error="Invalid username or password.")

    # store user in session (Flask signs the cookie with SECRET_KEY)
    session["user_id"] = user["id"]
    session["username"] = user["username"]
    return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html", username=session["username"])


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=os.getenv("FLASK_DEBUG", "0") == "1")
