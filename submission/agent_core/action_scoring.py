from typing import Any

from agent_core.board import BoardState
from agent_core.evaluator import choose_best_indices


def choose_indices(
    board: BoardState,
    options: list[Any],
    min_count: int,
    max_count: int,
) -> list[int]:
    return choose_best_indices(board, options, min_count, max_count)