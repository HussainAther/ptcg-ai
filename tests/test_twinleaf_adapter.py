import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.adapters.twinleaf_adapter import TwinleafAdapter
from src.interfaces.legal_action import ActionType


def test_twinleaf_adapter_parses_neutral_state():
    raw = {
        'turn': 3,
        'phase': 'attack',
        'player': {
            'name': 'me',
            'prizesLeft': 5,
            'hand': ['A', 'B'],
            'deck': ['C'],
            'discard': [],
            'active': {'name': 'Pikachu', 'hpRemaining': 70, 'hpMax': 100},
            'bench': [{'name': 'Bulbasaur', 'hpRemaining': 90, 'hpMax': 90}],
        },
        'opponent': {
            'name': 'opp',
            'prizesLeft': 6,
            'hand': [],
            'deck': ['X', 'Y'],
            'discard': ['Z'],
            'active': {'name': 'Charmander', 'hpRemaining': 40, 'hpMax': 70},
            'bench': [],
        },
        'legal_actions': [
            {'type': 'attack', 'label': 'Attack with Thunder Shock'},
            {'type': 'retreat', 'label': 'Retreat'},
        ],
    }

    state = TwinleafAdapter().from_twinleaf_state(raw)

    assert state.turn_number == 3
    assert state.player.name == 'me'
    assert state.player.active.name == 'Pikachu'
    assert state.opponent.active.name == 'Charmander'
    assert len(state.legal_actions) == 2
    assert state.legal_actions[0].action_type == ActionType.ATTACK

def test_twinleaf_adapter_maps_real_action_types():
    adapter = TwinleafAdapter()
    actions = adapter.from_twinleaf_actions([
        {"type": "ATTACK_ACTION", "name": "Thunder Shock", "clientId": 1},
        {"type": "RETREAT_ACTION", "benchIndex": 0, "clientId": 1},
        {"type": "PASS_TURN", "clientId": 1},
    ])

    assert actions[0].action_type == ActionType.ATTACK
    assert actions[1].action_type == ActionType.RETREAT
    assert actions[2].action_type == ActionType.END_TURN