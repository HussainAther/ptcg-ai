from src.cabt.observation_parser import CABTObservationParser


def test_parse_cabt_observation_options():
    obs = {
        "select": {
            "minCount": 1,
            "maxCount": 1,
            "option": [{"type": "attack"}, {"type": "pass"}],
        }
    }

    parsed = CABTObservationParser().parse(obs)

    assert parsed.has_selection is True
    assert parsed.min_count == 1
    assert parsed.max_count == 1
    assert len(parsed.options) == 2
    assert parsed.options[0].index == 0