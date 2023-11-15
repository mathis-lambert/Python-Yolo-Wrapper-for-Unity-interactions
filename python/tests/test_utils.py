import numpy as np
from src.utils import *


def test_distance():
    assert distance([0, 0], [0, 0]) == 0
    assert distance([0, 0], [3, 4]) == 5


def test_angle():
    assert angle([0, 0], [0, 0], [0, 0]) == 0
    assert angle([1, 0], [0, 0], [0, 1]) == 90


def test_get_side():
    positions = {
        "left_shoulder": [0, 0],
        "left_hip": [0, 2],
        "right_shoulder": [0, 0],
        "right_hip": [0, 3]
    }
    assert get_side(positions) == "droite"


def test_get_head_inclination():
    positions = {
        "left_ear": [0, 0],
        "left_shoulder": [0, 2],
        "right_ear": [0, 0],
        "right_shoulder": [0, 3]
    }
    assert get_head_inclination(positions) == "droite"
