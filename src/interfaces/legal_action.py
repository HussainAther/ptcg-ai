from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict


class ActionType(str, Enum):
    ATTACK = 'attack'
    RETREAT = 'retreat'
    PLAY_CARD = 'play_card'
    ATTACH_ENERGY = 'attach_energy'
    EVOLVE = 'evolve'
    USE_ABILITY = 'use_ability'
    END_TURN = 'end_turn'
    PASS = 'pass'


@dataclass
class LegalAction:
    action_type: ActionType
    label: str
    payload: Dict[str, Any]
