import json
from pathlib import Path

from src.cabt.replay_db import ReplayDB


def summarize_replay(path: str, limit: int = 120) -> None:
    data = json.loads(Path(path).read_text(encoding="utf-8-sig"))

    print("game_id:", data.get("id"))
    print("rewards:", data.get("rewards"))
    print("statuses:", data.get("statuses"))
    print()

    for step_index, step in enumerate(data.get("steps", [])[:limit]):
        if not step:
            continue

        for player_index, record in enumerate(step):
            obs = record.get("observation") or record.get("obs") or {}
            select = record.get("select") or obs.get("select")
            action = record.get("action")
            selected = record.get("selected")

            if not select:
                continue

            print("=" * 80)
            print("step:", step_index, "player:", player_index)
            print("context:", select.get("context"))
            print("type:", select.get("type"))
            print("min/max:", select.get("minCount"), select.get("maxCount"))
            print("action:", action)
            print("selected:", selected)

            for i, option in enumerate(select.get("option", [])):
                print(f"  {i}: {option}")


def ingest(path: str, db_path: str = "data/replays/replays.sqlite3") -> None:
    db = ReplayDB(db_path)
    db.ingest_replay(path)

    print("Ingested:", path)
    print()
    print("Decision contexts:")
    for row in db.summarize():
        print(row)

    db.close()


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("--db", default="data/replays/replays.sqlite3")
    parser.add_argument("--ingest", action="store_true")
    parser.add_argument("--limit", type=int, default=120)
    args = parser.parse_args()

    if args.ingest:
        ingest(args.path, args.db)
    else:
        summarize_replay(args.path, args.limit)


if __name__ == "__main__":
    main()