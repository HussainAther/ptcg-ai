from dataclasses import dataclass, field
from typing import List, Optional
from src.simulation.pokemon import PokemonInPlay


@dataclass
class PlayerState:
    name: str
    deck: List[str] = field(default_factory=list)
    hand: List[str] = field(default_factory=list)
    discard: List[str] = field(default_factory=list)
    prizes_left: int = 6
    active: Optional[PokemonInPlay] = None
    bench: List[PokemonInPlay] = field(default_factory=list)
    supporter_played_this_turn: bool = False
    energy_attached_this_turn: bool = False

    def draw(self, n: int = 1) -> None:
        for _ in range(n):
            if self.deck:
                self.hand.append(self.deck.pop(0))

    def can_bench(self) -> bool:
        return len(self.bench) < 5

    def take_prize(self, n: int = 1) -> None:
        self.prizes_left = max(0, self.prizes_left - n)

    def reset_turn_flags(self) -> None:
        self.supporter_played_this_turn = False
        self.energy_attached_this_turn = False
        if self.active:
            self.active.evolved_this_turn = False
        for pokemon in self.bench:
            pokemon.evolved_this_turn = False
