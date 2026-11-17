from datetime import timedelta
from pathlib import Path

from feast import Entity, FeatureService, FeatureView, Field, FileSource, ValueType
from feast.types import Float32, Int64, String

# Written by services/ingestion/main.py into the shared data volume.
DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "titanic_features.parquet"

passenger = Entity(
    name="passenger",
    join_keys=["passenger_id"],
    value_type=ValueType.INT64,
)

titanic_source = FileSource(
    name="titanic_source",
    path=str(DATA_PATH),
    timestamp_field="event_timestamp",
)

titanic_passenger_features = FeatureView(
    name="titanic_passenger_features",
    entities=[passenger],
    ttl=timedelta(days=3650),
    schema=[
        Field(name="Name", dtype=String),
        Field(name="Sex", dtype=Int64),
        Field(name="Age", dtype=Float32),
        Field(name="Survived", dtype=Int64),
        Field(name="Fare", dtype=Float32),
    ],
    source=titanic_source,
    online=True,
)

titanic_serving = FeatureService(
    name="titanic_serving",
    features=[titanic_passenger_features],
)
