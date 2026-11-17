import sys
from datetime import timezone
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "features"))

from features import extract, panda_clean  # noqa: E402

OUTPUT = REPO_ROOT / "data" / "titanic_features.parquet"


def ingest():
    cleaned = panda_clean(extract())
    cleaned["event_timestamp"] = pd.Timestamp.now(tz=timezone.utc)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_parquet(OUTPUT, index=False)
    print(f"Wrote {len(cleaned)} rows to {OUTPUT}")
    return cleaned


if __name__ == "__main__":
    ingest()
