import os
import mysql.connector
from flask import Flask, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


def get_db_connection():
    """Create and return a MySQL connection."""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "mysql"),
        port=int(os.getenv("DB_PORT", 3306)),
        database=os.getenv("DB_NAME", "lab_db"),
        user=os.getenv("DB_USER", "lab_user"),
        password=os.getenv("DB_PASSWORD", "lab_password"),
    )


@app.route("/")
def index():
    return jsonify({"message": "Flask + MySQL container is running!", "status": "ok"})


@app.route("/health")
def health():
    """Check DB connectivity."""
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify({"status": "healthy", "database": "connected"})
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500


@app.route("/users")
def get_users():
    """Fetch all users from the DB."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify({"users": users})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=os.getenv("FLASK_DEBUG", "0") == "1")
