from agent_core.board import BoardState
from agent_core.features import extract_features, evaluate_board
from agent_core.structured_actions import StructuredAction


class ActionEvaluator:
    def score(self, board: BoardState, action: StructuredAction) -> int:
        features = extract_features(board)
        score = evaluate_board(features)
        context = board.select_context.lower()

        if "setupactivepokemon" in context:
            return self._score_setup_active(action)

        if "setupbenchpokemon" in context:
            return 700

        if "drawcount" in context and action.number is not None:
            return action.number * 500

        if action.kind == "attack":
            score += 100
            if features.opp_active_hp <= 90 and features.opp_active_hp > 0:
                score += 500
            elif features.opp_active_hp <= 120 and features.opp_active_hp > 0:
                score += 300
            elif features.opp_active_hp <= 180 and features.opp_active_hp > 0:
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
            if features.my_active_hp <= 40 and features.my_active_hp > 0:
                score += 90
            else:
                score += 5

        elif action.kind == "pass":
            score -= 300

        elif action.kind == "card":
            score += self._score_card_choice(board, action)

        elif action.kind == "number":
            score += (action.number or 0) * 100

        return score

    def _score_setup_active(self, action: StructuredAction) -> int:
        text = action.text
        if "kyogre" in text:
            return 1000
        if "snover" in text:
            return 800
        if "mega" in text:
            return 100
        return 300

    def _score_card_choice(self, board: BoardState, action: StructuredAction) -> int:
        context = board.select_context.lower()

        if "setupbenchpokemon" in context:
            return 700

        if board.me.bench_count < 3:
            return 80

        return 20


def choose_best_indices(board: BoardState, options, min_count: int, max_count: int) -> list[int]:
    from agent_core.structured_actions import parse_actions

    actions = parse_actions(list(options))
    evaluator = ActionEvaluator()

    scored = [(evaluator.score(board, action), action.index) for action in actions]
    scored.sort(reverse=True)

    count = max(min_count, max_count)
    count = min(count, len(scored))

    return [index for _, index in scored[:count]]