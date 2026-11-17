.PHONY: build up ingest apply materialize train examples logs down teardown

# Build the ingestion + feast images.
build:
	docker compose build

# Start Redis (online store), the Feast container, and the MLflow server.
up:
	docker compose up -d redis feast mlflow

# Run the ingestion job: extract -> panda_clean -> write parquet into the shared volume.
ingest:
	docker compose run --rm ingestion

# Register entity / feature view / feature service in the Feast registry.
apply:
	docker compose exec feast feast apply

# Load the latest feature values from the offline parquet into Redis.
materialize:
	docker compose exec feast sh -c 'feast materialize-incremental $$(date -u +%Y-%m-%dT%H:%M:%S)'

# Train the logistic regression and log/register it in MLflow (http://localhost:5000).
train:
	docker compose run --rm training

# Score example passengers and print their survival probabilities.
examples:
	docker compose run --rm serving

logs:
	docker compose logs -f

down:
	docker compose down

# Also remove the Redis + feature-data volumes.
teardown:
	docker compose down -v
