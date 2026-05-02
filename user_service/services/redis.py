from redis.asyncio import ConnectionPool, Redis
from shared_packages.core.config import RedisSettings



class RedisService():
    def __init__(self, redis_url : str):
        self.pool = ConnectionPool.from_url(f"{redis_url}", decode_responses = True)
        self._client= Redis(connection_pool=self.pool)
    async def close(self):
        await self._client.close()
    async def add_to_blacklist(self, jti : str, ttl: int):
        key = f"jwt_blacklist:{jti}"
        await self._client.setex(key, ttl, 1)
    async def is_in_blacklist(self, jti:str):
        result = await self._client.exists(f"jwt_blacklist:{jti}")
        return result > 0 
