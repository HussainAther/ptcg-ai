from typing import List


TAG_PATTERNS = {
    'damage_pressure': ['damage', 'knock out', 'ko'],
    'bench_pressure': ['bench', 'benched'],
    'draw_engine': ['draw'],
    'deck_search': ['search your deck', 'look at the top'],
    'energy_acceleration': ['attach', 'energy'],
    'discard_synergy': ['discard'],
    'switching_mobility': ['switch', 'retreat'],
    'healing_sustain': ['heal', 'recover'],
    'status_control': ['poisoned', 'burned', 'paralyzed', 'asleep', 'confused'],
    'evolution_support': ['evolve', 'evolution'],
    'hand_disruption': ['your opponent shuffles', 'discard a card from your opponent'],
    'damage_prevention': ['prevent all damage', 'prevent effects'],
}


def infer_tags(effect_text: str) -> List[str]:
    text = (effect_text or '').lower()
    tags = []
    for tag, patterns in TAG_PATTERNS.items():
        if any(pattern in text for pattern in patterns):
            tags.append(tag)
    return tags
