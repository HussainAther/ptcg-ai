from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class PokemonInPlay:
    name: str
    max_hp: int
    current_hp: int
    card_type: str = ""
    stage: str = "Basic Pokemon"
    energy_attached: List[str] = field(default_factory=list)
    status_conditions: List[str] = field(default_factory=list)
    evolved_this_turn: bool = False

    @property
    def is_knocked_out(self) -> bool:
        return self.current_hp <= 0

    def attach_energy(self, energy_name: str) -> None:
        self.energy_attached.append(energy_name)

    def take_damage(self, amount: int) -> None:
        self.current_hp = max(0, self.current_hp - amount)

    def heal(self, amount: int) -> None:
        self.current_hp = min(self.max_hp, self.current_hp + amount)
