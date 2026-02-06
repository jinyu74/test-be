from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app


def test_health_ready_skipped_when_disabled() -> None:
    client = TestClient(app)
    original = settings.enable_health_checks

    try:
        object.__setattr__(settings, "enable_health_checks", False)
        response = client.get("/health/ready")

        assert response.status_code == 200
        assert response.json() == {"status": "skipped"}
    finally:
        object.__setattr__(settings, "enable_health_checks", original)
