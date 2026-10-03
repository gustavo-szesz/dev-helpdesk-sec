import pytest
import requests

@pytest.fixture(scope="session", autouse=True)
def verify_test_health_check():
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code != 200:
            pytest.exit("Offline target", returncode=1)

        data = response.json()
        if data.get("status") != "ok":
            pytest.exit(f"Offline target (Invalid status code): {data}", returncode=1)
        
    except requests.RequestException:
        pytest.exit("Not possible connect to the server")
    except ValueError:
        pytest.exit("The server not returne a valid JSON", returncode=1)

def test_exemple_control_access():
    assert True