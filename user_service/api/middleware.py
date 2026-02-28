from fastapi import Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
import asyncpg

async def db_exception_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except IntegrityError as exc:
        orig_exc = exc.orig
        
        if hasattr(orig_exc, "__cause__") and isinstance(orig_exc.__cause__, asyncpg.exceptions.UniqueViolationError):
            detail = orig_exc.__cause__.detail 
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "error": "Conflict",
                    "message": "Дані вже існують",
                    "detail": detail
                }
            )
        
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Integrity Error", "message": "Помилка цілісності даних в БД"}
        )
    except Exception as exc:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "Internal Server Error", "message": str(exc)}
        )