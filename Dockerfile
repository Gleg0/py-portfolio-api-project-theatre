FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt /app/
RUN apt-get update && apt-get install -y gcc libpq-dev bash
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s \
  CMD curl -f http://localhost:8000/health/ || exit 1

ENTRYPOINT ["/app/entrypoint.sh"]
