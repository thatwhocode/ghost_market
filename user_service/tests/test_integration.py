import httpx
import pytest
import time 

BASE_URL = "https://localhost:443"

@pytest.mark.asyncio
async def test_health_check_ssl():
    async with httpx.AsyncClient(base_url=BASE_URL, verify=False) as client:
        response = await client.get("/docs")
        assert response.status_code == 200

@pytest.mark.asyncio
async def test_register_user_ssl_flow():
    unique_id = int(time.time())
    payload = {
        "email": f"integration_ssl_{unique_id}@example.com",
        "username": f"ssl_user_{unique_id}",
        "password": "secure_password123"
    }
    async with httpx.AsyncClient(base_url=BASE_URL, verify=False) as client:
        response = await client.post("/v1/auth/register", json=payload)
        assert response.status_code in [200, 201]