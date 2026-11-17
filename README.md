# live-ml-model-serving

An end-to-end example that takes the Titanic dataset, serves its features through
[Feast](https://feast.dev/), trains a model tracked in
[MLflow](https://mlflow.org/), and scores example passengers — all wired together
with Docker Compose.

## Architecture

```
ingestion ──▶ data (parquet) ──▶ Feast (registry + Redis online store)
                                     │
                                     ▼
                                  training ──▶ MLflow (tracking + model registry)
                                                   │
                                                   ▼
                                                serving (example predictions)
```

| Service | Role |
|---------|------|
| `redis` | Feast online store |
| `feast` | Runs `feast apply` / `materialize` against the feature repo in `features/` |
| `ingestion` | `extract()` → `panda_clean()` → writes `titanic_features.parquet` |
| `mlflow` | Tracking server + model registry (http://localhost:5000) |
| `training` | Pulls features from Feast, trains a logistic regression, registers a model version |
| `serving` | Loads the latest registered model and prints survival probabilities for example passengers |

Data moves between the `ingestion`, `feast`, and `training` containers through the
shared `feature-data` named volume (no bind mounts — code is copied into the images).

## Features

`panda_clean()` keeps `passenger_id`, `Name`, `Sex`, `Age`, `Survived`, `Fare`,
drops rows with missing values, and maps `Sex` to `male=0 / female=1`.

The model (`titanic-logistic-regression`) predicts `Survived` from `Sex`, `Age`,
and `Fare` (every feature except `Name`; `passenger_id` is the entity key).

## Usage

```bash
make build        # build all images
make up           # start redis, feast, mlflow
make ingest       # produce the feature parquet
make apply        # register entity / feature view / feature service
make materialize  # load features into the Redis online store
make train        # train + register the logistic regression in MLflow
make examples     # score sample passengers and print survival probabilities
```

Then browse runs and model versions at http://localhost:5000.

> **Note:** Docker is driven from the host (`docker.exe` / Docker Desktop). If `make`
> is run from a WSL shell without Docker integration, call the `docker compose`
> commands directly instead.

## Teardown

```bash
make down       # stop containers
make teardown   # stop and remove the named volumes
```
