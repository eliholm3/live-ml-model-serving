FROM python:3.12-slim

WORKDIR /repo

COPY services/serving/requirements.txt services/serving/requirements.txt
RUN pip install --no-cache-dir -r services/serving/requirements.txt

COPY services/ services/

CMD ["python", "services/serving/app.py"]
