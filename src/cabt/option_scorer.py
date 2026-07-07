class CABTOptionScorer:
    def score_text(self, text: str) -> int:
        text = text.lower()
        score = 0

        if "attack" in text:
            score += 100
        if "knock" in text or "damage" in text:
            score += 50
        if "energy" in text or "attach" in text:
            score += 40
        if "draw" in text or "search" in text:
            score += 35
        if "evolve" in text:
            score += 30
        if "ability" in text:
            score += 25
        if "retreat" in text:
            score += 10
        if "pass" in text or "end" in text:
            score -= 20

        return score

    def choose_indices(self, options, max_count: int):
        scored = [(self.score_text(str(option)), i) for i, option in enumerate(options)]
        scored.sort(reverse=True)
        return [i for _, i in scored[:max_count]]