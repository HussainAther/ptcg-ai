from dataclasses import dataclass, field
from typing import Any


@dataclass
class PokemonState:
    name: str = ""
    hp: int = 0
    max_hp: int = 0
    energies: int = 0


@dataclass
class PlayerBoard:
    active: PokemonState | None = None
    bench_count: int = 0
    hand_count: int = 0
    deck_count: int = 0
    prize_count: int = 0
    discard_count: int = 0
    hand: list[dict] = field(default_factory=list)
    bench: list[dict] = field(default_factory=list)


@dataclass
class BoardState:
    current_player_index: int = 0
    me: PlayerBoard = field(default_factory=PlayerBoard)
    opponent: PlayerBoard = field(default_factory=PlayerBoard)
    turn: int = 0
    energy_attached: bool = False
    supporter_played: bool = False
    select_context: str = ""
    select_type: str = ""


def _parse_active(player: dict[str, Any]) -> PokemonState | None:
    active = player.get("active") or []
    if not active or active[0] is None:
        return None

    card = active[0]
    return PokemonState(
        name=str(card.get("name", "")),
        hp=int(card.get("hp", 0) or 0),
        max_hp=int(card.get("maxHp", 0) or 0),
        energies=len(card.get("energies", []) or []) + len(card.get("energyCards", []) or []),
    )


def _parse_player(player: dict[str, Any]) -> PlayerBoard:
    return PlayerBoard(
        active=_parse_active(player),
        bench_count=len(player.get("bench") or []),
        hand_count=int(player.get("handCount", 0) or 0),
        deck_count=int(player.get("deckCount", 0) or 0),
        prize_count=len(player.get("prize") or []),
        discard_count=len(player.get("discard") or []),
        hand=list(player.get("hand") or []),
        bench=list(player.get("bench") or []),
    )


def parse_board(obs_dict: dict[str, Any]) -> BoardState:
    current = obs_dict.get("current") or {}
    select = obs_dict.get("select") or {}

    players = current.get("players") or []

    your_index = int(current.get("yourIndex", 0) or 0)
    opp_index = 1 - your_index if len(players) > 1 else 0

    me_raw = players[your_index] if len(players) > your_index else {}
    opp_raw = players[opp_index] if len(players) > opp_index else {}

    return BoardState(
        current_player_index=your_index,
        me=_parse_player(me_raw),
        opponent=_parse_player(opp_raw),
        turn=int(current.get("turn", 0) or 0),
        energy_attached=bool(current.get("energyAttached", False)),
        supporter_played=bool(current.get("supporterPlayed", False)),
        select_context=str(select.get("context", "")),
        select_type=str(select.get("type", "")),
    )