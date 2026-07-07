from src.simulation.game_state import GameState
from src.simulation.rules import Rules


class GameEngine:
    def attach_energy(self, state: GameState, energy_name: str = "Basic Energy") -> GameState:
        player = state.current()

        if not Rules.can_attach_energy(state):
            raise ValueError("Energy already attached this turn.")

        if player.active is None:
            raise ValueError("No active Pokemon to attach energy to.")

        player.active.attach_energy(energy_name)
        player.energy_attached_this_turn = True
        return state

    def play_supporter_draw(self, state: GameState, cards: int = 2) -> GameState:
        player = state.current()

        if not Rules.can_play_supporter(state):
            raise ValueError("Supporter already played this turn.")

        player.draw(cards)
        player.supporter_played_this_turn = True
        return state

    def attack(self, state: GameState, damage: int = 60) -> GameState:
        attacker = state.current()
        defender = state.opposing()

        if attacker.active is None:
            raise ValueError("No active attacking Pokemon.")
        if defender.active is None:
            raise ValueError("No defending active Pokemon.")

        defender.active.take_damage(damage)

        if defender.active.is_knocked_out:
            attacker.take_prize(1)
            defender.discard.append(defender.active.name)
            defender.active = defender.bench.pop(0) if defender.bench else None

        Rules.check_game_over(state)
        return state

    def retreat(self, state: GameState, bench_index: int = 0) -> GameState:
        player = state.current()

        if not Rules.can_retreat(state):
            raise ValueError("Cannot retreat.")

        old_active = player.active
        player.active = player.bench.pop(bench_index)
        player.bench.append(old_active)
        return state
