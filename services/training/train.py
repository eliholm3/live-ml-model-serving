import os

import mlflow
import mlflow.sklearn
import pandas as pd
from feast import FeatureStore
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split

# Every feature except Name (passenger_id is the entity key, Survived is the target).
FEATURE_REFS = [
    "titanic_passenger_features:Sex",
    "titanic_passenger_features:Age",
    "titanic_passenger_features:Fare",
    "titanic_passenger_features:Survived",
]
FEATURE_COLS = ["Sex", "Age", "Fare"]
TARGET = "Survived"


def load_training_data():
    store = FeatureStore(repo_path="/repo/features")
    source = pd.read_parquet("/repo/data/titanic_features.parquet")
    entity_df = source[["passenger_id", "event_timestamp"]]
    return store.get_historical_features(
        entity_df=entity_df,
        features=FEATURE_REFS,
    ).to_df()


def main():
    df = load_training_data()
    X = df[FEATURE_COLS]
    y = df[TARGET]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI", "http://mlflow:5000"))
    mlflow.set_experiment("titanic-survival")

    with mlflow.start_run():
        model = LogisticRegression(max_iter=1000)
        model.fit(X_train, y_train)

        preds = model.predict(X_test)
        proba = model.predict_proba(X_test)[:, 1]
        accuracy = accuracy_score(y_test, preds)
        roc_auc = roc_auc_score(y_test, proba)

        mlflow.log_param("features", FEATURE_COLS)
        mlflow.log_param("target", TARGET)
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("roc_auc", roc_auc)
        mlflow.sklearn.log_model(
            model,
            artifact_path="model",
            registered_model_name="titanic-logistic-regression",
        )
        print(f"Logged run: accuracy={accuracy:.4f} roc_auc={roc_auc:.4f}")


if __name__ == "__main__":
    main()
