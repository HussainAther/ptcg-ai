import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.cabt.replay_db import ReplayDB


def test_replay_db_ingests_decisions(tmp_path):
    replay = {
        "id": "game-1",
        "rewards": [-1, 1],
        "statuses": ["DONE", "DONE"],
        "steps": [
            [
                {
                    "action": [0],
                    "observation": {
                        "select": {
                            "context": "DrawCount",
                            "type": "Count",
                            "minCount": 1,
                            "maxCount": 1,
                            "option": [{"type": "Number", "number": 0}],
                        }
                    },
                    "selected": [0],
                },
                {},
            ]
        ],
    }

    replay_path = tmp_path / "replay.json"
    replay_path.write_text(json.dumps(replay), encoding="utf-8")

    db = ReplayDB(str(tmp_path / "replays.sqlite3"))
    db.ingest_replay(str(replay_path))

    summary = db.summarize()
    db.close()

    assert summary[0]["context"] == "DrawCount"
    assert summary[0]["count"] == 1