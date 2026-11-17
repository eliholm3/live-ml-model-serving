FROM python:3.12-slim

WORKDIR /repo/features

RUN pip install --no-cache-dir "feast==0.68.0" redis pandas pyarrow

COPY features/ /repo/features/

# Kept alive so `docker compose exec feast feast <cmd>` can run apply/materialize/ui.
CMD ["sleep", "infinity"]
