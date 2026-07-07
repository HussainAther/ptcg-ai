import os
import random

from cg.api import Observation, to_observation_class

import json

from agent_core.board import parse_board
from agent_core.action_scoring import choose_indices
from agent_core.debug_logger import log_turn



def read_deck_csv() -> list[int]:
    """Read deck.csv.
    
    Returns:
        list[int]: A list of card IDs in the deck.
    """
    file_path = "deck.csv"
    if not os.path.exists(file_path):
        file_path = "/kaggle_simulations/agent/" + file_path
    with open(file_path, "r") as file:
        csv = file.read().split("\n")
    deck = []
    for i in range(60):
        deck.append(int(csv[i]))
    return deck

def agent(obs_dict: dict) -> list[int]:
    """Implement Your Pokémon Trading Card Game Agent.

    Each element in the returned list must be >= 0 and < len(obs.select.option).
    The list length must be between obs.select.minCount and obs.select.maxCount (inclusive), with no duplicate elements.
    
    Returns:
        list[int]: A list of option index.
    """
    obs: Observation = to_observation_class(obs_dict)
    try:
        with open("debug_obs.json", "w", encoding="utf-8") as f:
            json.dump(obs_dict, f, indent=2)
    except Exception:
        pass
    if obs.select == None:
        # In the initial selection, the obs.select is None, and it is necessary to return the deck.
        # The deck is a list of 60 card IDs.
        # The deck must comply with the Pokémon Trading Card Game rules.
        return read_deck_csv()
    
    scores = []

    for i, option in enumerate(obs.select.option):
        text = str(option).lower()
        score = 0

        if "attack" in text:
            score += 100
        if "knock" in text or "damage" in text:
            score += 50
        if "energy" in text or "attach" in text:
            score += 40
        if "draw" in text or "search" in text:
            score += 35
        if "ability" in text:
            score += 25
        if "evolve" in text:
            score += 30
        if "retreat" in text:
            score += 10
        if "pass" in text or "end" in text:
            score -= 20

        scores.append((score, i))

    scores.sort(reverse=True)

    count = obs.select.maxCount
    board = parse_board(obs_dict)
    selected = choose_indices(
        board=board,
        options=list(obs.select.option),
        min_count=obs.select.minCount,
        max_count=obs.select.maxCount,
    )

    log_turn(obs_dict, selected)
    return selected
