import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.simulation.simple_simulator import SimpleSimulator


def test_attack_knockout_reduces_my_prizes_left():
    state = {
        "my_prizes_left": 5,
        "opp_prizes_left": 6,
        "opp_active_hp": 50,
        "attack_damage": 60,
    }

    next_state = SimpleSimulator().step(state, "attack")

    assert next_state["opp_active_hp"] == 0
    assert next_state["my_prizes_left"] == 4
    assert next_state["opp_prizes_left"] == 6
