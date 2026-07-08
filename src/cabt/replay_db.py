import json
import sqlite3
from pathlib import Path
from typing import Any


SCHEMA = """
CREATE TABLE IF NOT EXISTS games (
    game_id TEXT PRIMARY KEY,
    path TEXT,
    reward_player0 REAL,
    reward_player1 REAL,
    status_player0 TEXT,
    status_player1 TEXT,
    raw_json TEXT
);

CREATE TABLE IF NOT EXISTS decisions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id TEXT,
    step_index INTEGER,
    player_index INTEGER,
    context TEXT,
    select_type TEXT,
    min_count INTEGER,
    max_count INTEGER,
    options_json TEXT,
    action_json TEXT,
    selected_json TEXT
);
"""


class ReplayDB:
    def __init__(self, path: str = "data/replays/replays.sqlite3"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.path)
        self.conn.executescript(SCHEMA)
        self.conn.commit()

    def close(self) -> None:
        self.conn.close()

    def ingest_replay(self, replay_path: str) -> None:
        path = Path(replay_path)
        data = json.loads(path.read_text(encoding="utf-8-sig"))

        game_id = str(data.get("id", path.stem))
        rewards = data.get("rewards") or [None, None]
        statuses = data.get("statuses") or [None, None]

        self.conn.execute(
            """
            INSERT OR REPLACE INTO games
            (game_id, path, reward_player0, reward_player1, status_player0, status_player1, raw_json)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                game_id,
                str(path),
                rewards[0] if len(rewards) > 0 else None,
                rewards[1] if len(rewards) > 1 else None,
                statuses[0] if len(statuses) > 0 else None,
                statuses[1] if len(statuses) > 1 else None,
                json.dumps(data),
            ),
        )

        self.conn.execute("DELETE FROM decisions WHERE game_id = ?", (game_id,))

        for step_index, step in enumerate(data.get("steps", [])):
            if not step:
                continue

            for player_index, record in enumerate(step):
                select = self._get_select(record)
                if not select:
                    continue

                self.conn.execute(
                    """
                    INSERT INTO decisions
                    (game_id, step_index, player_index, context, select_type,
                     min_count, max_count, options_json, action_json, selected_json)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        game_id,
                        step_index,
                        player_index,
                        str(select.get("context", "")),
                        str(select.get("type", "")),
                        select.get("minCount"),
                        select.get("maxCount"),
                        json.dumps(select.get("option", [])),
                        json.dumps(record.get("action")),
                        json.dumps(record.get("selected")),
                    ),
                )

        self.conn.commit()

    def summarize(self) -> list[dict[str, Any]]:
        rows = self.conn.execute(
            """
            SELECT context, select_type, COUNT(*) AS n
            FROM decisions
            GROUP BY context, select_type
            ORDER BY n DESC
            """
        ).fetchall()

        return [
            {"context": context, "select_type": select_type, "count": count}
            for context, select_type, count in rows
        ]

    def _get_select(self, record: dict[str, Any]) -> dict[str, Any] | None:
        obs = record.get("observation") or record.get("obs") or {}
        return record.get("select") or obs.get("select")