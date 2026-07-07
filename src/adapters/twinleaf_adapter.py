from typing import Any, Dict, List

from src.interfaces.game_state import NeutralGameState, PlayerView, PokemonView
from src.interfaces.legal_action import LegalAction, ActionType


class TwinleafAdapter:
    '''
    Adapter boundary between Twinleaf's TypeScript rules engine and this
    Python planning framework.

    Twinleaf should remain the rules authority. This adapter converts
    serialized Twinleaf state/actions into neutral Python objects that
    planners can evaluate.
    '''

    def from_twinleaf_state(self, raw_state: Dict[str, Any]) -> NeutralGameState:
        player_raw = raw_state.get('player', {})
        opponent_raw = raw_state.get('opponent', {})

        player = self._parse_player(player_raw, fallback_name='player')
        opponent = self._parse_player(opponent_raw, fallback_name='opponent')

        return NeutralGameState(
            player=player,
            opponent=opponent,
            turn_number=raw_state.get('turn', raw_state.get('turn_number', 0)),
            phase=str(raw_state.get('phase', '')),
            legal_actions=self.from_twinleaf_actions(raw_state.get('legal_actions', [])),
            raw_engine_state=raw_state,
        )

    def from_twinleaf_actions(self, raw_actions: List[Dict[str, Any]]) -> List[LegalAction]:
        actions = []

        for raw in raw_actions:
            label = str(raw.get('label', raw.get('type', 'unknown')))
            action_type = self._map_action_type(label)

            actions.append(
                LegalAction(
                    action_type=action_type,
                    label=label,
                    payload=raw,
                )
            )

        return actions

    def to_twinleaf_action(self, action: LegalAction) -> Dict[str, Any]:
        return action.payload

    def _parse_player(self, raw: Dict[str, Any], fallback_name: str) -> PlayerView:
        active = self._parse_pokemon(raw.get('active'))

        bench = []
        for item in raw.get('bench', []) or []:
            pokemon = self._parse_pokemon(item)
            if pokemon is not None:
                bench.append(pokemon)

        return PlayerView(
            name=str(raw.get('name', fallback_name)),
            prizes_left=int(raw.get('prizes_left', raw.get('prizesLeft', 6))),
            hand_count=int(raw.get('hand_count', raw.get('handCount', len(raw.get('hand', []))))),
            deck_count=int(raw.get('deck_count', raw.get('deckCount', len(raw.get('deck', []))))),
            discard_count=int(raw.get('discard_count', raw.get('discardCount', len(raw.get('discard', []))))),
            active=active,
            bench=bench,
        )

    def _parse_pokemon(self, raw: Any):
        if not raw:
            return None

        return PokemonView(
            name=str(raw.get('name', raw.get('cardName', 'Unknown'))),
            hp_remaining=raw.get('hp_remaining', raw.get('hpRemaining')),
            hp_max=raw.get('hp_max', raw.get('hpMax')),
            attached_energy=list(raw.get('attached_energy', raw.get('attachedEnergy', [])) or []),
            tools=list(raw.get('tools', []) or []),
            status=list(raw.get('status', raw.get('status_conditions', [])) or []),
        )

    def _map_action_type(self, label: str) -> ActionType:
        text = label.lower()

        if 'attack' in text:
            return ActionType.ATTACK
        if 'retreat' in text:
            return ActionType.RETREAT
        if 'energy' in text or 'attach' in text:
            return ActionType.ATTACH_ENERGY
        if 'evolve' in text:
            return ActionType.EVOLVE
        if 'ability' in text:
            return ActionType.USE_ABILITY
        if 'end' in text:
            return ActionType.END_TURN
        if 'play' in text:
            return ActionType.PLAY_CARD

        return ActionType.PASS
