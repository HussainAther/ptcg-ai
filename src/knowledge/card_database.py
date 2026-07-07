from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict
import pandas as pd


@dataclass
class Card:
    card_id: int
    name: str
    stage: str
    rule: str
    category: str
    hp: str
    card_type: str
    move_name: str
    cost: str
    damage: str
    effect: str
    tags: List[str] = field(default_factory=list)


class CardDatabase:
    def __init__(self, csv_path: str = 'data/EN_Card_Data.csv'):
        self.csv_path = Path(csv_path)
        self.df = pd.read_csv(self.csv_path)
        self.stage_col = [c for c in self.df.columns if c.startswith('Stage')][0]
        self.cards = self._load_cards()

    def _clean(self, value):
        if pd.isna(value):
            return ''
        return str(value)

    def _load_cards(self) -> List[Card]:
        cards = []
        for _, row in self.df.iterrows():
            cards.append(Card(
                card_id=int(row['Card ID']),
                name=self._clean(row['Card Name']),
                stage=self._clean(row[self.stage_col]),
                rule=self._clean(row['Rule']),
                category=self._clean(row['Category']),
                hp=self._clean(row['HP']),
                card_type=self._clean(row['Type']),
                move_name=self._clean(row['Move Name']),
                cost=self._clean(row['Cost']),
                damage=self._clean(row['Damage']),
                effect=self._clean(row['Effect Explanation']),
            ))
        return cards

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame([card.__dict__ for card in self.cards])
