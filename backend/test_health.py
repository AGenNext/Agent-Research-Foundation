from fastapi.testclient import TestClient

from main import app


def test_health_endpoint():
    client = TestClient(app)
    response = client.get('/health')

    assert response.status_code == 200
    assert response.json()['status'] == 'healthy'


def test_demo_endpoint():
    client = TestClient(app)
    response = client.get('/api/demo')

    assert response.status_code == 200
    data = response.json()
    assert 'agentNodes' in data
    assert 'executionLogs' in data
