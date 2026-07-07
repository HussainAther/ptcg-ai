from src.knowledge.card_knowledge_graph import CardKnowledgeGraph
from src.planner.heuristic_planner import HeuristicPlanner
from src.planner.lookahead_planner import LookaheadPlanner
from src.planner.mcts import MCTSPlanner
from src.simulation.state_encoder import StateEncoder
from src.evaluation.board_evaluator import BoardEvaluator


def main():
    kg = CardKnowledgeGraph()

    print('Knowledge graph loaded.')
    print('Unique strategic tags:', len(kg.tag_counts()))
    print()

    print('Top strategic tags:')
    for tag, count in sorted(kg.tag_counts().items(), key=lambda x: x[1], reverse=True):
        print(tag, count)

    print()
    print('Example card summary:')
    print(kg.card_summary('Greninja ex'))

    state = {
        'my_prizes_left': 5,
        'opp_prizes_left': 6,
        'my_hand': ['Energy', 'Item', 'Supporter'],
        'opp_hand_size': 4,
        'my_active_hp': 120,
        'opp_active_hp': 50,
        'my_bench': ['Basic A', 'Basic B'],
        'opp_bench': ['Basic C'],
        'turn_number': 4,
        'attack_damage': 60,
        'can_attack': True,
        'can_attach_energy': True,
        'can_play_supporter': True,
        'can_retreat': True,
    }

    encoded = StateEncoder().encode(state)
    print()
    print('Encoded state:')
    print(dict(zip(encoded.feature_names, encoded.vector)))

    print()
    print('Board evaluation:')
    board_eval = BoardEvaluator().evaluate(state)
    print('score:', board_eval.score)
    print('components:', board_eval.components)

    print()
    print('Heuristic planner:')
    print(HeuristicPlanner().choose_action(state))

    print()
    print('Lookahead planner:')
    print(LookaheadPlanner().choose_action(state))

    print()
    print('MCTS planner:')
    print(MCTSPlanner(simulations=200, rollout_depth=4).choose_action(state))


if __name__ == '__main__':
    main()
