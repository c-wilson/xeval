"""
This module holds abstract algorithm functions with very simple interfaces and with very weak assumptions
on the input of the data. Other processors will parse and proofread the data from the database for use in 
these functions.

THESE DEPEND ON NOTHING in the project - changes to the database structure, web interface, etc. will not 
require changes to these functions.
"""

import numpy as np


def reach(X: np.array, *args, **kwargs):
    """
    Returns the Reach score and confidence from an input array.

    :param X: input array
    :return: score, confidence
    """
    if len(X):
        score = X.mean()
        confidence = _sigmoid(len(X), 2., 6.)
    else:
        score, confidence = 0., 0.
    return score, confidence


def clarity(X: np.array, *args, **kwargs):
    """
    Returns the Clarity score and confidence from an input array.

    :param X: input array
    :return: value, confidence
    """
    if len(X):
        score = X.mean()
        confidence = _sigmoid(len(X), 4., 8.)
    else:
        score, confidence = 0, 0
    return score, confidence


def clout(X_clarity: np.array, X_reach:np.array, *args, **kwargs):
    """
    Calculates the Clout score and confidence. Clout is normalized weighted average of Reach and Clarity metrics.

    :param X_clarity: input array for clarity feature
    :param X_reach: input array for reach feature
    :return: value, confidence
    """

    if not len(X_clarity) or not len(X_reach):
        return 0., 0.

    reach_val, reach_con = reach(X_reach)
    clarity_val, clarity_con = clarity(X_clarity)

    total_con = reach_con + clarity_con
    r_weight, c_weight = [x / total_con for x in (reach_con, clarity_con)]
    weighted_avg = r_weight * reach_val + c_weight * clarity_val
    score = weighted_avg / 10.  # normalize to max score value.

    confidence = min(reach_con, clarity_con)

    return score, confidence


def _sigmoid(x: float, a: float, b: float) -> float:
    """
    Evaluates a sigmoid at a specified value "x" using two shape parameters, a and b.
    a and b params determine the x values of the sigmoid's threshold and saturation points, respectively.

    :param x: input value
    :param a: threshold shape parameter
    :param b: saturation shape parameter
    :return: scalar
    """

    midpoint = a+b / 2.
    if x <= a:
        return 0.
    elif a < x < midpoint:
        return 2. * ((x - a) / (b - a)) ** 2.
    elif midpoint <= x < b:
        return 1. - 2. * ((x - a) / (b - a)) ** 2
    else:  # x >= b
        return 1.