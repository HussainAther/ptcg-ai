import json
from pathlib import Path
from pprint import pprint


def summarize_obj(obj, depth=0, max_depth=4):
    indent = "  " * depth

    if depth > max_depth:
        print(indent + "... max depth ...")
        return

    if isinstance(obj, dict):
        print(indent + f"dict keys={list(obj.keys())}")
        for key, value in obj.items():
            print(indent + f"- {key}: {type(value).__name__}")
            summarize_obj(value, depth + 1, max_depth)
    elif isinstance(obj, list):
        print(indent + f"list len={len(obj)}")
        for i, value in enumerate(obj[:5]):
            print(indent + f"[{i}] {type(value).__name__}")
            summarize_obj(value, depth + 1, max_depth)
        if len(obj) > 5:
            print(indent + f"... {len(obj) - 5} more items")
    else:
        print(indent + repr(obj))


def inspect_observation(obs_dict):
    print("=" * 80)
    print("RAW OBSERVATION STRUCTURE")
    print("=" * 80)
    summarize_obj(obs_dict)

    print()
    print("=" * 80)
    print("TOP-LEVEL KEYS")
    print("=" * 80)
    pprint(list(obs_dict.keys()))

    print()
    print("=" * 80)
    print("SELECT / OPTIONS")
    print("=" * 80)

    select = obs_dict.get("select")
    if select is None:
        print("select is None")
        return

    pprint(select)

    options = select.get("option", [])
    print()
    print("Number of options:", len(options))

    for i, option in enumerate(options[:20]):
        print()
        print(f"OPTION {i}")
        pprint(option)


def main():
    fixture = Path("fixtures/cabt_observation_sample.json")

    if not fixture.exists():
        print("Missing fixture:")
        print(fixture)
        print()
        print("Next step: save a real observation JSON there.")
        return

    obs_dict = json.loads(fixture.read_text(encoding="utf-8-sig"))
    inspect_observation(obs_dict)


if __name__ == "__main__":
    main()