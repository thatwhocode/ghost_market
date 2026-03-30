from user_service.api.deps import Dependencies
from shared_packages.core.config import admin_settings
from user_service.db.database import AsyncSessionLocal
from shared_packages.db.user import User
from user_service.core.security import get_password_hash
from sqlalchemy import select, update
import asyncio

async def create_first_admin():
    if admin_settings.ADMIN_PASSWORD == "missing_secret":
        print("❌ Error: ADMIN_PASSWORD not found in secrets or env!")
        return
    async with AsyncSessionLocal() as session :
        try:
        # Шукаємо існуючого адміна
            query  = select(User).where(User.is_superuser == True)
            result = await session.execute(query)
            admin = result.scalar_one_or_none()
            if admin:
                print(f"ℹ️ Admin already exists: {admin.username}")
                return

            new_admin = User(
                email=admin_settings.ADMIN_EMAIL,
                username=admin_settings.ADMIN_USERNAME,
                hashed_password=get_password_hash(admin_settings.ADMIN_PASSWORD),
                is_superuser=True
            )
            session.add(new_admin)
            await session.commit()
            print(f"✅ Admin created!")
        except Exception as e:
            await session.rollback()
            print(f"❌ Failed: {e}")

if __name__ == "__main__":
    asyncio.run(create_first_admin())