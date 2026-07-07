import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.adapters.twinleaf_adapter import TwinleafAdapter
from src.interfaces.engine import EngineAdapter
from src.interfaces.legal_action import ActionType


def test_twinleaf_adapter_implements_engine_interface():
    adapter: EngineAdapter = TwinleafAdapter()

    raw_state = {
        "turn": 4,
        "phase": "player_turn",
        "player": {
            "name": "me",
            "prizesLeft": 5,
            "hand": ["Card A", "Card B"],
            "deck": ["Card C"],
            "discard": [],
            "active": {"name": "Greninja ex", "hpRemaining": 180, "hpMax": 310},
            "bench": [],
        },
        "opponent": {
            "name": "opp",
            "prizesLeft": 6,
            "hand": [],
            "deck": [],
            "discard": [],
            "active": {"name": "Charmander", "hpRemaining": 50, "hpMax": 70},
            "bench": [],
        },
        "legal_actions": [
            {"type": "ATTACK_ACTION", "clientId": 1, "name": "Water Shuriken"},
            {
                "type": "PLAY_CARD_ACTION",
                "id": 1,
                "handIndex": 0,
                "target": {"player": 1, "slot": 3, "index": 0},
            },
            {"type": "RETREAT_ACTION", "clientId": 1, "benchIndex": 0},
            {"type": "PASS_TURN", "clientId": 1},
        ],
    }

    state = adapter.parse_state(raw_state)

    assert state.player.active.name == "Greninja ex"
    assert state.opponent.active.name == "Charmander"

    action_types = [a.action_type for a in state.legal_actions]

    assert ActionType.ATTACK in action_types
    assert ActionType.PLAY_CARD in action_types
    assert ActionType.RETREAT in action_types
    assert ActionType.END_TURN in action_types

    engine_payload = adapter.to_engine_action(state.legal_actions[0])
    assert engine_payload["type"] == "ATTACK_ACTION"