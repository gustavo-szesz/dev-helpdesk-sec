from __future__ import annotations

import pytest
import requests
from typing import Final

HEALTH_URL: Final[str] = "http://localhost:8000/health"
TIMEOUT: Final[float] = 5.0
EXPECTED_STATUS: Final[str] = "ok"

def _fetch_health() -> dict:
    response = requests.get(HEALTH_URL, timeout=TIMEOUT)
    response.raise_for_status()
    return response.json()


def _is_health(payload: dict) -> bool:
    return payload.get("status") == EXPECTED_STATUS


@pytest.fixture(scope="session", autouse=True)
def verify_test_health_check():
    try:
        data = _fetch_health()
    except requests.Timeout:
        pytest.exit("Health check time out", returncode=1)
    except requests.ConnectionError:
        pytest.exit("Could not connect to the server", returncode=1)
    except requests.HTTPError as exc:
        pytest.exit(f"Health endpoint returned {exc.response.status_code}", returncode=1)
    except ValueError:
        pytest.exit("Health endpoint did not return a valid JSON", returncode=1)
    
    if not _is_health(data):
        pytest.exit(
            f"Servere reported unhealthy status: {data!r}",
            returncode=1
        )


def test_exemple_control_access():
    assert True