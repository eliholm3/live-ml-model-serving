FROM python:3.12-slim

WORKDIR /repo

COPY services/ingestion/requirements.txt services/ingestion/requirements.txt
RUN pip install --no-cache-dir -r services/ingestion/requirements.txt

COPY features/ features/
COPY services/ services/

CMD ["python", "services/ingestion/main.py"]
