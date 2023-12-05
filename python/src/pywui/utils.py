import numpy as np


def distance(a, b):
    return np.sqrt(((a[0] - b[0]) ** 2) + ((a[1] - b[1]) ** 2))


def angle(a, b, c):
    v1 = np.array([a[0] - b[0], a[1] - b[1]])
    v2 = np.array([c[0] - b[0], c[1] - b[1]])
    if np.linalg.norm(v1) == 0 or np.linalg.norm(v2) == 0:
        return 0

    return np.degrees(np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))))


def get_side(positions):
    left_side = distance(positions["left_shoulder"], positions["left_hip"])
    right_side = distance(positions["right_shoulder"], positions["right_hip"])

    if left_side > right_side:
        return "gauche"
    elif left_side < right_side:
        return "droite"
    else:
        return "centre"


def get_head_inclination(positions):
    left_side = distance(positions["left_ear"], positions["left_shoulder"])
    right_side = distance(positions["right_ear"], positions["right_shoulder"])

    if left_side > right_side:
        return "gauche"
    elif left_side < right_side:
        return "droite"
    else:
        return "centre"
