from dataclasses import dataclass
from src.simulation.player import PlayerState


@dataclass
class GameState:
    player: PlayerState
    opponent: PlayerState
    turn_number: int = 1
    current_player: str = "player"
    game_over: bool = False
    winner: str = ""

    def current(self) -> PlayerState:
        return self.player if self.current_player == "player" else self.opponent

    def opposing(self) -> PlayerState:
        return self.opponent if self.current_player == "player" else self.player

    def switch_turn(self) -> None:
        self.current_player = "opponent" if self.current_player == "player" else "player"
        self.turn_number += 1
        self.current().reset_turn_flags()
