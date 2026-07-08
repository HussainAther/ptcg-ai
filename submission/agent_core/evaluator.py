from agent_core.board import BoardState
from agent_core.features import extract_features, evaluate_board
from agent_core.structured_actions import StructuredAction


class ActionEvaluator:
    def score(self, board: BoardState, action: StructuredAction) -> int:
        features = extract_features(board)
        score = evaluate_board(features)
        context = board.select_context.lower()

        if "setupactivepokemon" in context:
            return self._score_setup_active(board, action)

        if "setupbenchpokemon" in context:
            return self._score_card_choice(board, action)

        if "drawcount" in context and action.number is not None:
            return action.number * 10000

        if "count" in board.select_type.lower() and action.number is not None:
            return action.number * 1000

        if action.kind == "attack":
            score += 100
            if 0 < features.opp_active_hp <= 90:
                score += 500
            elif 0 < features.opp_active_hp <= 120:
                score += 300
            elif 0 < features.opp_active_hp <= 180:
                score += 150

        elif action.kind == "attach_energy":
            if not features.energy_attached:
                score += 180 if features.my_energy < 2 else 80
            else:
                score -= 100

        elif action.kind == "evolve":
            score += 160

        elif action.kind == "ability":
            score += 80

        elif action.kind == "retreat":
            if 0 < features.my_active_hp <= 40:
                score += 90
            else:
                score += 5

        elif action.kind == "pass":
            score -= 300

        elif action.kind == "card":
            score += self._score_card_choice(board, action)

        elif action.kind == "number":
            score += (action.number or 0) * 100

        elif action.kind == "yes":
            if "isfirst" in context:
                score -= 50
            else:
                score += 100

        elif action.kind == "no":
            if "isfirst" in context:
                score += 50
            else:
                score -= 20

        return score

    def _score_setup_active(self, board: BoardState, action: StructuredAction) -> int:
        name = self._card_name_from_action(board, action)

        if "kyogre" in name:
            return 1200
        if "snover" in name:
            return 900
        if "mega abomasnow" in name:
            return -1000
        if "energy" in name:
            return -500

        return 100

    def _score_card_choice(self, board: BoardState, action: StructuredAction) -> int:
        context = board.select_context.lower()
        name = self._card_name_from_action(board, action)

        if "setupbenchpokemon" in context:
            if "kyogre" in name:
                return 1000
            if "snover" in name:
                return 900
            if "energy" in name:
                return -500
            if "mega abomasnow" in name:
                return -800
            return 300

        if "kyogre" in name:
            return 300
        if "snover" in name:
            return 200
        if "mega abomasnow" in name:
            return 120
        if "energy" in name:
            return 80

        if board.me.bench_count < 3:
            return 80

        return 20

    def _card_name_from_action(
        self, board: BoardState, action: StructuredAction
    ) -> str:
        if action.card_name:
            return action.card_name

        if action.area == 2 and action.target_index is not None:
            hand = board.me.hand
            if 0 <= action.target_index < len(hand):
                return str(hand[action.target_index].get("name", "")).lower()

        return action.text


def choose_best_indices(
    board: BoardState, options, min_count: int, max_count: int
) -> list[int]:
    from agent_core.structured_actions import parse_actions

    actions = parse_actions(list(options))
    evaluator = ActionEvaluator()

    scored = [(evaluator.score(board, action), action.index) for action in actions]
    scored.sort(reverse=True)

    count = max(min_count, max_count)
    count = min(count, len(scored))

    return [index for _, index in scored[:count]]