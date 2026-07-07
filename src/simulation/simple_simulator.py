from copy import deepcopy
from typing import Dict, Any


class SimpleSimulator:
    def step(self, state: Dict[str, Any], action: str) -> Dict[str, Any]:
        next_state = deepcopy(state)
        action = str(action).lower()

        if action == 'attack':
            damage = next_state.get('attack_damage', 60)
            next_state['opp_active_hp'] = max(
                0,
                next_state.get('opp_active_hp', 0) - damage,
            )

            if next_state['opp_active_hp'] == 0:
                next_state['opp_prizes_left'] = max(
                    0,
                    next_state.get('opp_prizes_left', 6) - 1,
                )

        elif action == 'attach_energy':
            next_state['energy_attached_this_turn'] = True

        elif action == 'play_supporter':
            hand = next_state.get('my_hand', [])
            next_state['my_hand'] = hand + ['drawn_card_1', 'drawn_card_2']

        elif action == 'retreat':
            next_state['retreated_this_turn'] = True

        elif action == 'play_item':
            next_state['played_item_this_turn'] = True

        next_state['turn_number'] = next_state.get('turn_number', 1) + 1
        return next_state
