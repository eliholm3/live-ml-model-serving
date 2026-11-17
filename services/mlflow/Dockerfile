FROM python:3.12-slim

# SQLAlchemy 2.1 dropped FallbackAsyncAdaptedQueuePool, which mlflow 2.x still imports.
RUN pip install --no-cache-dir "mlflow>=2.17,<3" "sqlalchemy<2.1"

EXPOSE 5000

CMD ["mlflow", "server", "--host", "0.0.0.0", "--port", "5000", "--backend-store-uri", "sqlite:////mlflow/mlflow.db", "--artifacts-destination", "/mlflow/artifacts"]
