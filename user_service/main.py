from fastapi import FastAPI
from user_service.db.database import get_db
from contextlib import asynccontextmanager
from user_service.api import auth
from fastapi.middleware.cors import CORSMiddleware
from user_service.api.middleware import db_exception_middleware
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        yield
    except Exception as e:
        print(e)
    finally:
        pass

api_version_prefix = "v1"
app = FastAPI(lifespan=lifespan)
app.middleware("http")(db_exception_middleware)
app.include_router(auth.router, prefix=f"/{api_version_prefix}/auth", tags=["Auth"])