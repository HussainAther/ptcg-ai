from dataclasses import dataclass
from typing import Any


@dataclass
class StructuredAction:
    index: int
    kind: str
    raw: Any
    text: str = ""
    card_name: str = ""
    number: int | None = None
    area: int | None = None
    target_index: int | None = None


def parse_action(index: int, option: Any) -> StructuredAction:
    text = str(option).lower()

    action = StructuredAction(
        index=index,
        kind="unknown",
        raw=option,
        text=text,
    )

    if isinstance(option, dict):
        option_type = str(option.get("type", "")).lower()
        action.number = option.get("number")
        action.area = option.get("area")
        action.target_index = option.get("index")

        if option_type in {"card", "3"}:
            action.kind = "card"
        elif option_type in {"number", "0"}:
            action.kind = "number"
        elif option_type in {"yes", "1"}:
            action.kind = "yes"
        elif option_type in {"no", "2"}:
            action.kind = "no"

        name = str(option.get("name", "")).lower()
        if name:
            action.card_name = name

    if "attack" in text:
        action.kind = "attack"
    elif "retreat" in text:
        action.kind = "retreat"
    elif "energy" in text or "attach" in text:
        action.kind = "attach_energy"
    elif "evolve" in text:
        action.kind = "evolve"
    elif "ability" in text:
        action.kind = "ability"
    elif "pass" in text or "end" in text:
        action.kind = "pass"

    return action

def parse_actions(options: list[Any]) -> list[StructuredAction]:
    return [parse_action(i, option) for i, option in enumerate(options)]