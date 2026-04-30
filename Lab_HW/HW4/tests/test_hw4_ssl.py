from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from main import create_app, build_ssl_context


def test_home_returns_expected_message():
    app = create_app()
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["message"] == "HW4 Flask HTTPS app is running"


def test_build_ssl_context_uses_existing_files(tmp_path: Path):
    cert = tmp_path / "localhost.crt"
    key = tmp_path / "localhost.key"
    cert.write_text("cert")
    key.write_text("key")

    cert_path, key_path = build_ssl_context(cert, key)

    assert cert_path == str(cert)
    assert key_path == str(key)


def test_build_ssl_context_raises_for_missing_files(tmp_path: Path):
    cert = tmp_path / "missing.crt"
    key = tmp_path / "missing.key"

    with pytest.raises(FileNotFoundError):
        build_ssl_context(cert, key)
