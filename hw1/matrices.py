from math import sqrt, acos, isclose, pi
from typing import List


def dot_product(vector1, vector2):
    if len(vector1) != len(vector2):
        raise IndexError(
            f"Cannot perform dot product of vectors of different dimensions: {len(vector1)} and {len(vector2)} "
        )
    return sum((x * y for x, y in zip(vector1, vector2)))


def magnitude(vector):
    return sqrt(dot_product(vector, vector))


def angle_between_vectors(vector1, vector2):
    return acos(dot_product(vector1, vector2) / (magnitude(vector1) * magnitude(vector2)))


def check_and_matrix_shape(matrix):
    if len(matrix) == 0 or len(matrix[0]) == 0 or any((len(row) != len(matrix[0]) for row in matrix)):
        raise IndexError("Matrix cannot be empty or contain empty rows")
    if any((len(row) != len(matrix[0]) for row in matrix)):
        raise IndexError("Matrix must be of rectangular shape")
    return len(matrix), len(matrix[0])


def matrix_transpose(matrix):
    n_rows, n_cols = check_and_matrix_shape(matrix)
    return [[matrix[i][j] for i in range(n_rows)] for j in range(n_cols)]


def matrix_sum(matrix1, matrix2):
    n_rows1, n_cols1 = check_and_matrix_shape(matrix1)
    n_rows2, n_cols2 = check_and_matrix_shape(matrix2)
    if n_rows1 != n_rows2 or n_cols1 != n_cols2:
        raise IndexError("Matrix sum is only defined for matrices of the same shape")
    return [[matrix1[i][j] + matrix2[i][j] for j in range(n_cols1)] for i in range(n_rows1)]


def matrix_multiplication(matrix1, matrix2):
    n_rows1, n_cols1 = check_and_matrix_shape(matrix1)
    n_rows2, n_cols2 = check_and_matrix_shape(matrix2)
    if n_cols1 != n_rows2:
        raise IndexError(
            f"Matrix multiplication is not defined for matrices of shapes {n_rows1}x{n_cols1} and {n_rows2}x{n_cols2}"
        )
    transposed = matrix_transpose(matrix2)
    return [[dot_product(matrix1[i], transposed[j]) for j in range(n_cols2)] for i in range(n_rows1)]


if __name__ == "__main__":
    assert dot_product([2], [3]) == 6
    orthogonal1 = [1, -1, 1]
    orthogonal2 = [1, 1, 0]
    assert dot_product(orthogonal1, orthogonal2) == 0
    assert isclose(magnitude([1 / sqrt(2), 1 / sqrt(2)]), 1)
    assert isclose(angle_between_vectors([1, -1, 1], [1, 1, 0]), pi / 2)
    assert matrix_transpose([[1], [2], [3]]) == [[1, 2, 3]]
    assert matrix_sum([[1, 2, 3], [-1, -2, -3]], [[-1, -2, -3], [1, 2, 3]]) == [[0, 0, 0], [0, 0, 0]]
    assert matrix_multiplication([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [[1, 0, 0], [0, 1, 0], [0, 0, 1]]) == [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ]
