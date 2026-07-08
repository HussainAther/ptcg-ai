import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "submission"))

from agent_core.board import BoardState, PlayerBoard
from agent_core.evaluator import ActionEvaluator
from agent_core.structured_actions import parse_action


def test_setup_active_prefers_snover_over_energy():
    board = BoardState(
        select_context="SetupActivePokemon",
        me=PlayerBoard(
            hand=[
                {"name": "Basic {W} Energy"},
                {"name": "Snover"},
            ]
        ),
    )

    evaluator = ActionEvaluator()

    energy = parse_action(0, {"type": "Card", "area": 2, "index": 0})
    snover = parse_action(1, {"type": "Card", "area": 2, "index": 1})

    assert evaluator.score(board, snover) > evaluator.score(board, energy)


def test_draw_count_prefers_larger_number():
    board = BoardState(select_context="DrawCount", select_type="Count")
    evaluator = ActionEvaluator()

    zero = parse_action(0, {"type": "Number", "number": 0})
    one = parse_action(1, {"type": "Number", "number": 1})

    assert evaluator.score(board, one) > evaluator.score(board, zero)


def test_is_first_prefers_no():
    board = BoardState(select_context="IsFirst")
    evaluator = ActionEvaluator()

    yes = parse_action(0, {"type": "Yes"})
    no = parse_action(1, {"type": "No"})

    assert evaluator.score(board, no) > evaluator.score(board, yes)