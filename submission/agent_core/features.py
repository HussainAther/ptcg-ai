from dataclasses import dataclass
from agent_core.board import BoardState


@dataclass
class BoardFeatures:
    my_active_hp: int = 0
    my_active_max_hp: int = 0
    opp_active_hp: int = 0
    opp_active_max_hp: int = 0
    my_energy: int = 0
    opp_energy: int = 0
    my_bench_count: int = 0
    opp_bench_count: int = 0
    my_hand_count: int = 0
    opp_hand_count: int = 0
    my_prize_count: int = 0
    opp_prize_count: int = 0
    energy_attached: bool = False
    supporter_played: bool = False


def extract_features(board: BoardState) -> BoardFeatures:
    my_active = board.me.active
    opp_active = board.opponent.active

    return BoardFeatures(
        my_active_hp=my_active.hp if my_active else 0,
        my_active_max_hp=my_active.max_hp if my_active else 0,
        opp_active_hp=opp_active.hp if opp_active else 0,
        opp_active_max_hp=opp_active.max_hp if opp_active else 0,
        my_energy=my_active.energies if my_active else 0,
        opp_energy=opp_active.energies if opp_active else 0,
        my_bench_count=board.me.bench_count,
        opp_bench_count=board.opponent.bench_count,
        my_hand_count=board.me.hand_count,
        opp_hand_count=board.opponent.hand_count,
        my_prize_count=board.me.prize_count,
        opp_prize_count=board.opponent.prize_count,
        energy_attached=board.energy_attached,
        supporter_played=board.supporter_played,
    )


def evaluate_board(features: BoardFeatures) -> int:
    score = 0

    score += (features.opp_prize_count - features.my_prize_count) * 120
    score += (features.my_active_hp - features.opp_active_hp)
    score += (features.my_energy - features.opp_energy) * 35
    score += features.my_bench_count * 30
    score -= features.opp_bench_count * 15
    score += features.my_hand_count * 8
    score -= features.opp_hand_count * 4

    return score