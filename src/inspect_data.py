from pathlib import Path
import pandas as pd

DATA = Path('data')

print('Files:')
for p in DATA.rglob('*'):
    if p.is_file():
        print(p, round(p.stat().st_size / 1_000_000, 2), 'MB')

for csv_path in DATA.glob('*.csv'):
    print('\n' + '=' * 80)
    print(csv_path)
    df = pd.read_csv(csv_path)
    print('shape:', df.shape)
    print('columns:', list(df.columns))
    print(df.head(10))
