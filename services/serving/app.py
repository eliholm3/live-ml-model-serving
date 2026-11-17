import os

import mlflow
import mlflow.sklearn
import pandas as pd
from mlflow.tracking import MlflowClient

MODEL_NAME = "titanic-logistic-regression"
FEATURE_COLS = ["Sex", "Age", "Fare"]  # Sex: 0 = male, 1 = female

# A few hand-built passengers to score (same feature encoding as panda_clean).
EXAMPLES = pd.DataFrame(
    [
        {"label": "First-class woman", "Sex": 1, "Age": 28, "Fare": 80.0},
        {"label": "Third-class man", "Sex": 0, "Age": 40, "Fare": 8.0},
        {"label": "Young girl", "Sex": 1, "Age": 6, "Fare": 20.0},
        {"label": "Young man, cheap fare", "Sex": 0, "Age": 22, "Fare": 7.25},
        {"label": "Older woman, mid fare", "Sex": 1, "Age": 55, "Fare": 30.0},
    ]
)


def load_latest_model():
    mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI", "http://mlflow:5000"))
    client = MlflowClient()
    versions = client.search_model_versions(f"name='{MODEL_NAME}'")
    if not versions:
        raise RuntimeError(f"No registered versions for model '{MODEL_NAME}'. Run training first.")
    latest = max(versions, key=lambda v: int(v.version))
    model = mlflow.sklearn.load_model(f"models:/{MODEL_NAME}/{latest.version}")
    return model, latest.version


def main():
    model, version = load_latest_model()

    X = EXAMPLES[FEATURE_COLS]
    out = EXAMPLES.copy()
    out["survival_probability"] = model.predict_proba(X)[:, 1].round(4)
    out["predicted_survived"] = model.predict(X)

    print(f"Model: {MODEL_NAME} v{version}\n")
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
