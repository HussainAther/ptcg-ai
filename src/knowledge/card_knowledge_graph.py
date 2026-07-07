from collections import defaultdict
from typing import Dict, List
from src.knowledge.card_database import CardDatabase
from src.knowledge.card_tags import infer_tags


class CardKnowledgeGraph:
    def __init__(self, csv_path: str = 'data/EN_Card_Data.csv'):
        self.db = CardDatabase(csv_path)
        self.df = self.db.to_dataframe()
        self.df['tags'] = self.df['effect'].apply(infer_tags)
        self.by_name = defaultdict(list)
        self.by_tag = defaultdict(list)
        self.by_stage = defaultdict(list)
        self._build()

    def _build(self):
        for _, row in self.df.iterrows():
            name = row['name']
            self.by_name[name].append(row.to_dict())
            self.by_stage[row['stage']].append(name)
            for tag in row['tags']:
                self.by_tag[tag].append(name)

    def cards_with_tag(self, tag: str) -> List[str]:
        return sorted(set(self.by_tag.get(tag, [])))

    def card_summary(self, name: str) -> Dict:
        rows = self.by_name.get(name, [])
        if not rows:
            return {'name': name, 'found': False}

        tags = sorted(set(t for row in rows for t in row.get('tags', [])))
        stages = sorted(set(row.get('stage', '') for row in rows))
        effects = [row.get('effect', '') for row in rows if row.get('effect')]

        return {
            'name': name,
            'found': True,
            'rows': len(rows),
            'stages': stages,
            'tags': tags,
            'sample_effects': effects[:3],
        }

    def tag_counts(self) -> Dict[str, int]:
        return {tag: len(set(cards)) for tag, cards in self.by_tag.items()}
