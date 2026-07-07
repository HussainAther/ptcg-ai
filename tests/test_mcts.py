import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.planner.mcts import MCTSPlanner


def test_mcts_prefers_knockout_attack():
    state = {
        "my_prizes_left": 5,
        "opp_prizes_left": 6,
        "my_hand": ["Energy", "Item", "Supporter"],
        "opp_hand_size": 4,
        "my_active_hp": 120,
        "opp_active_hp": 50,
        "my_bench": ["Basic A"],
        "opp_bench": ["Basic C"],
        "turn_number": 4,
        "attack_damage": 60,
        "can_attack": True,
        "can_attach_energy": True,
        "can_play_supporter": True,
        "can_retreat": True,
    }

    decision = MCTSPlanner(simulations=100, rollout_depth=3).choose_action(state)

    assert decision["action"] == "attack"
