FROM python:3.12-bookworm
WORKDIR /app

COPY user_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHONPATH=/app
COPY user_service/scripts/entrypoint.sh /app/entrypoint.sh
RUN chmod +x user_service/scripts/entrypoint.sh


ENTRYPOINT ["/bin/bash", "/app/user_service/scripts/entrypoint.sh"]

