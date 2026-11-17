FROM python:3.12-slim

WORKDIR /repo

COPY services/training/requirements.txt services/training/requirements.txt
RUN pip install --no-cache-dir -r services/training/requirements.txt

COPY features/ features/
COPY services/ services/

CMD ["python", "services/training/train.py"]
