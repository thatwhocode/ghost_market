import pytest
from fastapi.testclient import TestClient
@pytest.mark.asyncio
async def test_admin_router_allows_admin(client, admin_token_headers):
    # Тепер client автоматично має доступ до бази контейнера,
    # а admin_token_headers підставляє валідний JWT.
    response = await client.get("/admin/users", headers=admin_token_headers)
    assert response.status_code == 200
@pytest.mark.asyncio
async def test_admin_router_allows_admin(client, admin_token_headers: dict):
    response = await client.get("/0.0.0.1/admin/users", headers=admin_token_headers)
    assert response.status_code == 200