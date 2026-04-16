from fastapi import FastAPI
from user_service.db.database import get_db
from contextlib import asynccontextmanager
from user_service.api import auth
from user_service.api import admin
from fastapi.middleware.cors import CORSMiddleware
from user_service.api.middleware import db_exception_middleware
from user_service.middleware import TraceIDMiddleware
from user_service.logging_config import configure_logging
from shared_packages.core.config import SharedBaseSettings
stgs = SharedBaseSettings()
configure_logging(env="development")
@asynccontextmanager

async def lifespan(app: FastAPI):
    try:
        yield
    except Exception as e:
        print(e)
    finally:
        pass
app = FastAPI(title="Ghost market game backend", description="Api for game backend managment", version="0.0.0.1", contact={"name":"thatwhocode", "email":"thatwhocode@gmail.com"},lifespan=lifespan)
app.middleware("http")(db_exception_middleware)
app.add_middleware(TraceIDMiddleware)
app.include_router(auth.router, prefix=f"/{stgs.APP_VERSION}/auth", tags=["Auth"])
app.include_router(admin.router, prefix=f"/{stgs.APP_VERSION}", tags=["Admin"])
@app.get("/version")
def version_getter():
    return {"version" : f"{stgs.APP_VERSION}"}
import structlog    
logger = structlog.get_logger()