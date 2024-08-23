"""
This module provides utility functions for calculating GSB (Good, Same, Bad) scores and accuracy.

The GSB scores are used to compare two values (reference and target) and determine if the target
value is greater, equal, or smaller than the reference value. The GSB scores are represented as
'G' (Good), 'S' (Same), or 'B' (Bad).

The module includes the following functions:
- gsb2int(x): Converts a GSB literal to an integer.
- int2gsb(x): Converts an integer to a GSB literal.
- calc_gsb(ref: int | float, val: int | float) -> str: Calculates the GSB score for a given
    reference and target value.
- calc_gsb_integer(ref: int | float, val: int | float) -> int: Calculates the GSB score as an
    integer (-1, 0, or 1) for a given reference and target value.
- calc_pairwise_gsb(scores: list[int | float]) -> list[int]: Calculates pairwise GSB scores
    for a list of scores.
- get_gsb_matrix(score_mat: list[list[int | float]] | np.ndarray): Calculates a GSB matrix
    for a matrix of scores.
- calc_gsb_acc(pred, truth): Calculates the accuracy of GSB predictions.
- calc_gb_acc(pred, truth): Calculates the accuracy of GSB predictions, excluding 'S' (Same) scores.

"""

import itertools
import numpy as np


def gsb2int(x):
    """
    Converts a GSB literal to an integer.
    """
    match x.upper():
        case 'G':
            return 1
        case 'S':
            return 0
        case 'B':
            return -1
        case _:
            raise ValueError(f"Got {x.upper()}")

def int2gsb(x):
    """
    Converts an integer to a GSB literal.
    """
    match x:
        case 1:
            return 'G'
        case 0:
            return 'S'
        case -1:
            return 'B'
        case _:
            raise ValueError(f"Got {x}")

def calc_gsb(ref: int | float, val: int | float) -> str:
    """
    Calculates the GSB score for a given reference and target value.

    Args:
        ref (int | float): The reference value.
        val (int | float): The target value.

    Returns:
        str: The GSB score, which can be 'G' (Good), 'S' (Same), or 'B' (Bad).
    """
    res = ''
    if val > ref:
        res = 'G'
    elif val < ref:
        res = 'B'
    else:
        res = 'S'
    return res


def calc_gsb_integer(ref: int | float, val: int | float) -> int:
    """
    Calculates the GSB score as an integer (-1, 0, or 1) for a given reference and target value.

    Args:
        ref (int | float): The reference value.
        val (int | float): The target value.

    Returns:
        int: The GSB score as an integer. -1 represents 'B' (Bad), 0 represents 'S' (Same), and 1 represents 'G' (Good).
    """
    res = calc_gsb(ref, val)
    return gsb2int(res)


def calc_pairwise_gsb(scores: list[int | float]) -> list[int]:
    """
    Calculates pairwise GSB scores for a list of scores.

    Args:
        scores (list[int | float]): The list of scores.

    Returns:
        list[int]: The list of pairwise GSB scores.
    """
    pairs = itertools.combinations(scores, 2)
    return [
        calc_gsb_integer(a, b)
        for a, b in pairs
    ]


def get_gsb_matrix(score_mat: list[list[int | float]] | np.ndarray):
    """
    Calculates a GSB matrix for a matrix of scores.

    Args:
        score_mat (list[list[int | float]] | np.ndarray): The matrix of scores.

    Returns:
        np.ndarray: The GSB matrix.
    """
    mat = []
    for scores in score_mat:
        mat.append(calc_pairwise_gsb(scores))
    return np.array(mat)


def calc_gsb_acc(pred, truth):
    """
    Calculates the accuracy of GSB predictions.

    Args:
        pred: The predicted GSB scores.
        truth: The ground truth GSB scores.

    Returns:
        float: The accuracy of GSB predictions.
    """
    return np.mean(pred == truth)


def calc_gb_acc(pred, truth):
    """
    Calculates the accuracy of GSB predictions, excluding 'S' (Same) scores.

    Args:
        pred: The predicted GSB scores.
        truth: The ground truth GSB scores.

    Returns:
        float: The accuracy of GSB predictions, excluding 'S' scores.
    """
    return np.mean(pred == truth, where=np.logical_and(pred != 0, truth != 0))
