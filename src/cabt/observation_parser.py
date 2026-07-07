from dataclasses import dataclass, field
from typing import Any


@dataclass
class CABTOption:
    index: int
    text: str
    raw: Any


@dataclass
class CABTObservation:
    has_selection: bool
    min_count: int = 0
    max_count: int = 0
    options: list[CABTOption] = field(default_factory=list)
    raw: dict[str, Any] = field(default_factory=dict)


class CABTObservationParser:
    def parse(self, obs_dict: dict[str, Any]) -> CABTObservation:
        select = obs_dict.get("select")

        if select is None:
            return CABTObservation(has_selection=False, raw=obs_dict)

        options = [
            CABTOption(index=i, text=str(option), raw=option)
            for i, option in enumerate(select.get("option", []))
        ]

        return CABTObservation(
            has_selection=True,
            min_count=int(select.get("minCount", 0)),
            max_count=int(select.get("maxCount", 0)),
            options=options,
            raw=obs_dict,
        )