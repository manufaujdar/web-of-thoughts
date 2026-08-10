FROM node:24-alpine AS frontend
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

FROM python:3.13-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY pyproject.toml README.md LICENSE ./
COPY tools ./tools
COPY wot_app ./wot_app
RUN pip install --no-cache-dir .
COPY --from=frontend /app/frontend/dist ./frontend/dist
RUN useradd --create-home --uid 10001 wot && mkdir -p /app/data && chown -R wot:wot /app
USER wot
EXPOSE 8000
CMD ["uvicorn", "wot_app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
