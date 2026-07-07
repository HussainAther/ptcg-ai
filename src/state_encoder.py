from dataclasses import dataclass
from typing import Dict, Any
import numpy as np


@dataclass
class EncodedState:
    vector: np.ndarray
    feature_names: list


class StateEncoder:
    def encode(self, state: Dict[str, Any]) -> EncodedState:
        features = {
            'my_prizes_left': state.get('my_prizes_left', 6),
            'opp_prizes_left': state.get('opp_prizes_left', 6),
            'my_hand_size': len(state.get('my_hand', [])),
            'opp_hand_size_est': state.get('opp_hand_size', 0),
            'my_active_hp': state.get('my_active_hp', 0),
            'opp_active_hp': state.get('opp_active_hp', 0),
            'my_bench_size': len(state.get('my_bench', [])),
            'opp_bench_size': len(state.get('opp_bench', [])),
            'turn_number': state.get('turn_number', 1),
        }

        names = list(features.keys())
        vector = np.array([features[name] for name in names], dtype=float)
        return EncodedState(vector=vector, feature_names=names)
