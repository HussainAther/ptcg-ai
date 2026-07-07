from abc import ABC, abstractmethod
from typing import Any, Dict, List

from src.interfaces.game_state import NeutralGameState
from src.interfaces.legal_action import LegalAction


class EngineAdapter(ABC):
    @abstractmethod
    def parse_state(self, raw_state: Dict[str, Any]) -> NeutralGameState:
        pass

    @abstractmethod
    def parse_actions(self, raw_actions: List[Dict[str, Any]]) -> List[LegalAction]:
        pass

    @abstractmethod
    def to_engine_action(self, action: LegalAction) -> Dict[str, Any]:
        pass