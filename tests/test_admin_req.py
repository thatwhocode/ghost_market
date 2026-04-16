import pytest
from fastapi.testclient import TestClient

def test_admin_router_is_globally_protected(client: TestClient, regular_user_token_headers: dict):


    response = client.get("/admin/users", headers=regular_user_token_headers)
    
    assert response.status_code in [401, 403]

def test_admin_router_allows_admin(client: TestClient, admin_token_headers: dict):
    response = client.get("/admin/users", headers=admin_token_headers)
    assert response.status_code == 200