from starlette.middleware.base import BaseHTTPMiddleware
from uuid import uuid4
import structlog

class TraceIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        trace_id = request.headers.get("X-Request-ID", str(uuid4()))
        # Прив'язуємо trace_id до контексту structlog
        structlog.contextvars.bind_contextvars(trace_id=trace_id)
        try:
            response = await call_next(request)
            response.headers["X-Request-ID"] = trace_id
            return response
        finally:
            structlog.contextvars.unbind_contextvars("trace_id")