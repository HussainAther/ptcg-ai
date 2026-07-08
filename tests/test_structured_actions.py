import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "submission"))

from agent_core.structured_actions import parse_action


def test_parse_attack_text():
    action = parse_action(0, {"type": "Attack", "name": "Water Shuriken"})
    assert action.kind == "attack"


def test_parse_number_option():
    action = parse_action(1, {"type": "Number", "number": 1})
    assert action.kind == "number"
    assert action.number == 1