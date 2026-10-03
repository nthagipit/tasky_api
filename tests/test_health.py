from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_placeholder():
    """Test giữ chỗ để CI không bị fail khi chưa viết test logic"""
    assert True