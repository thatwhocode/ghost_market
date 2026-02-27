FROM python:3.12-bookworm
WORKDIR /app

COPY user_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHONPATH=/app
CMD ["uvicorn", "user_service.main:app", "--host", "0.0.0.0", "--port", "8002", "--reload"]