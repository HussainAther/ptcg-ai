from src.simulation.game_state import GameState


class Rules:
    @staticmethod
    def can_attach_energy(state: GameState) -> bool:
        return not state.current().energy_attached_this_turn

    @staticmethod
    def can_play_supporter(state: GameState) -> bool:
        return not state.current().supporter_played_this_turn

    @staticmethod
    def can_retreat(state: GameState) -> bool:
        player = state.current()
        return player.active is not None and len(player.bench) > 0

    @staticmethod
    def check_game_over(state: GameState) -> None:
        if state.player.prizes_left <= 0:
            state.game_over = True
            state.winner = "player"
        elif state.opponent.prizes_left <= 0:
            state.game_over = True
            state.winner = "opponent"
