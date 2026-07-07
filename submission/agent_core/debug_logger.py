import json
from pathlib import Path


def log_turn(obs_dict, selected):
    try:
        path = Path("debug_turns.jsonl")
        record = {
            "step": obs_dict.get("step"),
            "selected": selected,
            "select": obs_dict.get("select"),
            "current": obs_dict.get("current"),
        }
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
    except Exception:
        pass