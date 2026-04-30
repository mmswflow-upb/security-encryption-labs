from pathlib import Path
import os

from flask import Flask, jsonify


def create_app() -> Flask:
    app = Flask(__name__)

    @app.route("/")
    def home():
        return jsonify(
            {
                "message": "HW4 Flask HTTPS app is running",
                "hint": "Open this URL with https://localhost:5000",
            }
        )

    return app


def build_ssl_context(cert_path: str | Path, key_path: str | Path) -> tuple[str, str]:
    cert = Path(cert_path)
    key = Path(key_path)

    if not cert.exists():
        raise FileNotFoundError(f"SSL certificate not found: {cert}")
    if not key.exists():
        raise FileNotFoundError(f"SSL private key not found: {key}")

    return str(cert), str(key)


if __name__ == "__main__":
    cert_file = os.getenv("SSL_CERT_FILE", "certs/localhost.crt")
    key_file = os.getenv("SSL_KEY_FILE", "certs/localhost.key")

    ssl_context = build_ssl_context(cert_file, key_file)
    app = create_app()
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=os.getenv("FLASK_DEBUG", "0") == "1",
        ssl_context=ssl_context,
    )
