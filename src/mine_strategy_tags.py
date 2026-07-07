from pathlib import Path
import pandas as pd

DATA = Path('data')
OUT = Path('outputs')
OUT.mkdir(exist_ok=True)

df = pd.read_csv(DATA / 'EN_Card_Data.csv')
df['effect_text'] = df['Effect Explanation'].fillna('').astype(str).str.lower()

tags = {
    'draw_engine': ['draw'],
    'deck_search': ['search your deck', 'search'],
    'energy_acceleration': ['attach', 'energy'],
    'discard_synergy': ['discard'],
    'bench_pressure': ['bench', 'benched'],
    'switching_mobility': ['switch', 'retreat'],
    'healing_sustain': ['heal'],
    'status_control': ['poisoned', 'burned', 'paralyzed', 'asleep', 'confused'],
    'evolution_support': ['evolve', 'evolution'],
}

rows = []
for tag, terms in tags.items():
    mask = df['effect_text'].apply(lambda x: any(t in x for t in terms))
    rows.append({
        'tag': tag,
        'count': int(mask.sum()),
        'examples': ', '.join(df.loc[mask, 'Card Name'].dropna().astype(str).head(8))
    })

res = pd.DataFrame(rows).sort_values('count', ascending=False)
print(res.to_string(index=False))
res.to_csv(OUT / 'strategy_keyword_counts.csv', index=False)
