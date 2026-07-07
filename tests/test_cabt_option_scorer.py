import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.cabt.option_scorer import CABTOptionScorer


def test_option_scorer_prefers_attack_over_pass():
    scorer = CABTOptionScorer()
    options = ["Pass turn", "Attack for 100 damage"]

    assert scorer.choose_indices(options, max_count=1) == [1]