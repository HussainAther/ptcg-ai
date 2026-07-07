import json
from pathlib import Path

from src.adapters.twinleaf_adapter import TwinleafAdapter
from src.interfaces.legal_action import ActionType


def choose_simple_action(actions):
    priority = [
        ActionType.ATTACK,
        ActionType.PLAY_CARD,
        ActionType.ATTACH_ENERGY,
        ActionType.RETREAT,
        ActionType.END_TURN,
        ActionType.PASS,
    ]

    for action_type in priority:
        for action in actions:
            if action.action_type == action_type:
                return action

    return actions[0] if actions else None


def main():
    fixture_path = Path("fixtures/twinleaf_sample_state.json")
    raw_state = json.loads(fixture_path.read_text(encoding="utf-8"))

    adapter = TwinleafAdapter()
    neutral_state = adapter.parse_state(raw_state)

    print("Parsed neutral state")
    print("Turn:", neutral_state.turn_number)
    print("Phase:", neutral_state.phase)
    print("Player active:", neutral_state.player.active.name)
    print("Opponent active:", neutral_state.opponent.active.name)

    print()
    print("Legal actions:")
    for action in neutral_state.legal_actions:
        print("-", action.action_type.value, "|", action.label)

    chosen = choose_simple_action(neutral_state.legal_actions)
    engine_payload = adapter.to_engine_action(chosen)

    print()
    print("Chosen neutral action:", chosen.action_type.value)
    print("Twinleaf payload:")
    print(json.dumps(engine_payload, indent=2))


if __name__ == "__main__":
    main()s