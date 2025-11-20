import os
import sys
import pytest

ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.weather_planner.app import (
    find_activity,
    find_outfit,
    activity_list,
    outfit_list)

@pytest.mark.parametrize("temp, wind, precipitation, expected_activity", [
    (80, 5, "clear", "swimming"),
    (30, 10, "rainy", "read"),
    (20, 5, "snowy", "snowman"),
])

def test_find_activity(temp, wind, precipitation, expected_activity):
    #activities = activity_list()
    result = find_activity(temp, wind, precipitation,)
    assert result.name == expected_activity