from math import sqrt

from typing import Union, List


def mat_multiply(mat: Union[List[tuple], tuple], vec: tuple) -> tuple:
    return tuple([sum([el1 * el2 for el1, el2 in zip(row, vec)]) for row in mat])


# minimal math
def dot(v1: tuple, v2: tuple) -> float:
    return sum(x*y for x, y in zip(v1, v2))


def norm(vec: tuple) -> float:
    return sqrt(sum([el * el for el in vec]))


def cross(a, b) -> tuple:
    return (a[1]*b[2] - a[2]*b[1],
            a[2]*b[0] - a[0]*b[2],
            a[0]*b[1] - a[1]*b[0])


def sum_col(data: List[tuple]) -> List[float]:
    num_cols = len(data[0])  # number of columns in the data
    assert all([len(el) == num_cols for el in data])
    col_sums = [0] * num_cols  # initialize a list of zeros for column sums

    # iterate over the tuples and accumulate the sums of each column
    for row in data:
        for i in range(num_cols):
            col_sums[i] += row[i]
    return col_sums


def sum_tuple(t1: tuple, t2: tuple) -> tuple:
    return tuple(sum(el) for el in zip(t1, t2))