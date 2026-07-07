import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pytest

from src.simulation.game_engine import GameEngine
from src.simulation.game_state import GameState
from src.simulation.player import PlayerState
from src.simulation.pokemon import PokemonInPlay


def make_state():
    player = PlayerState(
        name="player",
        deck=["A", "B", "C"],
        hand=[],
        prizes_left=6,
        active=PokemonInPlay(name="Pikachu", max_hp=100, current_hp=100),
    )
    opponent = PlayerState(
        name="opponent",
        deck=["X", "Y", "Z"],
        hand=[],
        prizes_left=6,
        active=PokemonInPlay(name="Charmander", max_hp=70, current_hp=70),
        bench=[PokemonInPlay(name="Squirtle", max_hp=80, current_hp=80)],
    )
    return GameState(player=player, opponent=opponent)


def test_attack_deals_damage():
    state = make_state()
    GameEngine().attack(state, damage=30)
    assert state.opponent.active.current_hp == 40


def test_knockout_takes_prize_and_promotes_bench():
    state = make_state()
    GameEngine().attack(state, damage=80)
    assert state.player.prizes_left == 5
    assert state.opponent.active.name == "Squirtle"
    assert "Charmander" in state.opponent.discard


def test_energy_once_per_turn():
    state = make_state()
    engine = GameEngine()

    engine.attach_energy(state, "Water Energy")

    assert state.player.active.energy_attached == ["Water Energy"]

    with pytest.raises(ValueError):
        engine.attach_energy(state, "Fire Energy")


def test_supporter_once_per_turn():
    state = make_state()
    engine = GameEngine()

    engine.play_supporter_draw(state, cards=2)

    assert len(state.player.hand) == 2

    with pytest.raises(ValueError):
        engine.play_supporter_draw(state, cards=1)


def test_retreat_swaps_active_with_bench():
    state = make_state()
    state.player.bench.append(PokemonInPlay(name="Bulbasaur", max_hp=90, current_hp=90))

    GameEngine().retreat(state, bench_index=0)

    assert state.player.active.name == "Bulbasaur"
    assert state.player.bench[-1].name == "Pikachu"
