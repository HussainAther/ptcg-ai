from typing import Any, Dict, List


class ActionGenerator:
    def legal_actions(self, state: Dict[str, Any]) -> List[str]:
        actions = ['pass']

        if state.get('can_attack', True):
            actions.append('attack')

        if state.get('can_attach_energy', True):
            actions.append('attach_energy')

        if state.get('can_play_supporter', True):
            actions.append('play_supporter')

        if state.get('can_retreat', False):
            actions.append('retreat')

        if state.get('hand'):
            actions.append('play_item')

        return actions
