from __future__ import annotations


def isfloat(v):
    try:
        float(v)
    except (TypeError, ValueError):
        return False
    return True


def clip(x, a_min: None | float, a_max: None | float):
    if a_min is not None:
        if x < a_min:
            return a_min

    if a_max is not None:
        if x > a_max:
            return a_max

    return x


def determine_alarm_state(value, lowlow, low, high, highhigh):
    alarm_state = 0

    if lowlow is not None:
        if value < lowlow:
            alarm_state = 2

    if highhigh is not None:
        if value > highhigh:
            alarm_state = 2

    if low is not None:
        if value < low:
            alarm_state = 1

    if high is not None:
        if value > high:
            alarm_state = 1

    return alarm_state