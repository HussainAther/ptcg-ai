from card_database import CardDatabase
from card_tags import infer_tags
from planner import HeuristicPlanner
from state_encoder import StateEncoder


def main():
    db = CardDatabase()
    df = db.to_dataframe()
    df['tags'] = df['effect'].apply(infer_tags)

    print('Loaded cards:', len(df))
    print('Cards with strategic tags:', int(df['tags'].apply(len).gt(0).sum()))

    tag_counts = {}
    for tags in df['tags']:
        for tag in tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1

    print()
    print('Top tags:')
    for tag, count in sorted(tag_counts.items(), key=lambda x: x[1], reverse=True):
        print(tag, count)

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
        'can_attack': True,
        'can_attach_energy': True,
        'can_play_supporter': True,
        'can_retreat': True,
    }

    encoded = StateEncoder().encode(state)
    print()
    print('Encoded state:', dict(zip(encoded.feature_names, encoded.vector)))

    planner = HeuristicPlanner()
    decision = planner.choose_action(state)
    print()
    print('Chosen action:', decision.action)
    print('Score:', decision.score)
    print('Reason:', decision.reason)


if __name__ == '__main__':
    main()
