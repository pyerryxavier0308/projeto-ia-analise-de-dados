FROM python:3.13-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY app_core/ ./app_core/
COPY dashboard/ ./dashboard/
COPY data/ ./data/
RUN mkdir /app/artifacts
EXPOSE 8000
CMD ["python","-m","uvicorn","app_core.api:app","--host","0.0.0.0","--port","8000"]
