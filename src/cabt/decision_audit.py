import json
from pathlib import Path


def main():
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m src.cabt.decision_audit data/replays/84693265-0.json")
        return

    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8-sig"))

    for step_index, step in enumerate(data.get("steps", [])[:120]):
        for player_index, record in enumerate(step or []):
            obs = record.get("observation") or {}
            select = obs.get("select") or record.get("select")
            action = record.get("action")

            if not select:
                continue

            options = select.get("option", [])
            print("=" * 80)
            print("step:", step_index, "player:", player_index)
            print("context:", select.get("context"), "type:", select.get("type"))
            print("chosen:", action)
            for i, option in enumerate(options):
                marker = "<-- chosen" if action and i in action else ""
                print(f"{i}: {option} {marker}")


if __name__ == "__main__":
    main()