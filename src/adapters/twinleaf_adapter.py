from typing import Any, Dict, List

from src.interfaces.game_state import NeutralGameState, PlayerView, PokemonView
from src.interfaces.legal_action import LegalAction, ActionType
from src.interfaces.engine import EngineAdapter


class TwinleafAdapter(EngineAdapter):
    '''
    Adapter boundary between Twinleaf's TypeScript rules engine and this
    Python planning framework.

    Twinleaf should remain the rules authority. This adapter converts
    serialized Twinleaf state/actions into neutral Python objects that
    planners can evaluate.
    '''
    def parse_state(self, raw_state):
        return self.from_twinleaf_state(raw_state)

    def parse_actions(self, raw_actions):
        return self.from_twinleaf_actions(raw_actions)

    def to_engine_action(self, action):
        return self.to_twinleaf_action(action)


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

        if 'play_card_action' in text:
            return ActionType.PLAY_CARD
        if 'attack_action' in text or 'attack' in text:
            return ActionType.ATTACK
        if 'retreat_action' in text or 'retreat_start_action' in text or 'retreat' in text:
            return ActionType.RETREAT
        if 'pass_turn' in text or 'end' in text:
            return ActionType.END_TURN
        if 'use_ability_action' in text or 'ability' in text:
            return ActionType.USE_ABILITY
        if 'energy' in text or 'attach' in text:
            return ActionType.ATTACH_ENERGY
        if 'evolve' in text:
            return ActionType.EVOLVE
        if 'play' in text:
            return ActionType.PLAY_CARD

        return ActionType.PASS
    def test_twinleaf_adapter_maps_play_card_action():
        adapter = TwinleafAdapter()
        actions = adapter.from_twinleaf_actions([
            {
                "type": "PLAY_CARD_ACTION",
                "id": 1,
                "handIndex": 2,
                "target": {"player": 1, "slot": 3, "index": 0},
            }
        ])

        assert actions[0].action_type == ActionType.PLAY_CARD
        assert actions[0].payload["handIndex"] == 2
        assert actions[0].payload["target"]["slot"] == 3