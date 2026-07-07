from typing import Any
from agent_core.board import BoardState
from agent_core.features import extract_features, evaluate_board

def _option_text(option: Any) -> str:
    return str(option).lower()


def score_option(board: BoardState, option: Any) -> int:
    text = _option_text(option)
    context = board.select_context.lower()
    score = 0
    features = extract_features(board)
    score += evaluate_board(features)
    # Setup: choosing active Pokemon.
    if "setupactivepokemon" in context:
        if "kyogre" in text:
            return 1000
        if "snover" in text:
            return 800
        if "mega" in text:
            return 100
        return 300

    # Setup: bench basics whenever offered.
    if "setupbenchpokemon" in context:
        return 700

    # Draw count: prefer drawing more cards.
    if "drawcount" in context and isinstance(option, dict):
        return int(option.get("number", 0) or 0) * 500

    my_active = board.me.active
    opp_active = board.opponent.active

    # Prefer taking knockouts.
    if "attack" in text and features.opp_active_hp > 0:
        if features.opp_active_hp <= 90:
            score += 500
        elif features.opp_active_hp <= 120:
            score += 300
        elif features.opp_active_hp <= 180:
            score += 150

    # Prefer developing energy early.
    if ("energy" in text or "attach" in text) and not features.energy_attached:
        if features.my_energy < 2:
            score += 180
        else:
            score += 80

    # Avoid passing unless forced.
    if "pass" in text or "end" in text:
        score -= 300

    if "evolve" in text:
        score += 130

    if "bench" in text or "setup" in text:
        if board.me.bench_count < 3:
            score += 80
        else:
            score += 20

    if "draw" in text or "search" in text:
        score += 70

    if "ability" in text:
        score += 60

    if "retreat" in text:
        if my_active and my_active.hp <= 40:
            score += 80
        else:
            score += 5
    return score


def choose_indices(board: BoardState, options: list[Any], min_count: int, max_count: int) -> list[int]:
    if not options:
        return []

    scored = [(score_option(board, option), i) for i, option in enumerate(options)]
    scored.sort(reverse=True)

    count = max(min_count, max_count)
    count = min(count, len(options))

    return [i for _, i in scored[:count]]