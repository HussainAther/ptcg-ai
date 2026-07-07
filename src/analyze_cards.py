from pathlib import Path
import pandas as pd

DATA = Path('data')
OUT = Path('outputs')
OUT.mkdir(exist_ok=True)

df = pd.read_csv(DATA / 'EN_Card_Data.csv')

stage_col = [c for c in df.columns if c.startswith('Stage')][0]

print('Shape:', df.shape)
print()
print('Stage/type counts:')
print(df[stage_col].value_counts(dropna=False).head(40))
print()
print('Rules:')
print(df['Rule'].value_counts(dropna=False).head(30))
print()
print('Most common move/effect words:')

text = df['Effect Explanation'].fillna('').str.lower()
for word in ['draw', 'search', 'attach', 'energy', 'discard', 'bench', 'switch', 'heal', 'damage', 'evolve']:
    print(word, int(text.str.contains(word, regex=False).sum()))

out = df[[ 'Card ID', 'Card Name', stage_col, 'Rule', 'Category', 'HP', 'Type', 'Move Name', 'Cost', 'Damage', 'Effect Explanation' ]]
out.to_csv(OUT / 'en_card_clean_view.csv', index=False)

print()
print('Saved outputs/en_card_clean_view.csv')
