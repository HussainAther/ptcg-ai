from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from src.interfaces.legal_action import LegalAction


@dataclass
class PokemonView:
    name: str
    hp_remaining: Optional[int] = None
    hp_max: Optional[int] = None
    attached_energy: List[str] = field(default_factory=list)
    tools: List[str] = field(default_factory=list)
    status: List[str] = field(default_factory=list)


@dataclass
class PlayerView:
    name: str
    prizes_left: int
    hand_count: int
    deck_count: int
    discard_count: int
    active: Optional[PokemonView] = None
    bench: List[PokemonView] = field(default_factory=list)


@dataclass
class NeutralGameState:
    player: PlayerView
    opponent: PlayerView
    turn_number: int
    phase: str = ''
    legal_actions: List[LegalAction] = field(default_factory=list)
    raw_engine_state: Dict[str, Any] = field(default_factory=dict)
