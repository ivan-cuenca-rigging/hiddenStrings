# Imports
import math

# Maya imports
from maya import cmds


identity_matrix = [1, 0, 0, 0,
                   0, 1, 0, 0,
                   0, 0, 1, 0,
                   0, 0, 0, 1]

identity_matrix_x_negative = [-1, 0, 0, 0,
                              0, 1, 0, 0,
                              0, 0, 1, 0,
                              0, 0, 0, 1]


def distance_from_a_to_b(a, b):
    """
    Get distance between two nodes

    Args:
        a (str): dag node
        b (str): dag node

    Returns:
        float: distance
    """
    a_pos = cmds.xform(a, query=True, worldSpace=True, translation=True)
    b_pos = cmds.xform(b, query=True, worldSpace=True, translation=True)

    return float(math.dist(a_pos, b_pos))


def distance_from_a_to_b_xyz(a, b):
    """
    Get distance between two [x, y, z]

    Args:
        a (str): [x, y, z]
        b (str): [x, y, z]

    Returns:
        float: distance
    """
    return float(math.dist(a, b))



def get_n_positions_from_a_to_b(a, b, n):
    """
    Get a number of positions between two points

    Args:
        a (str): dag node
        b (str): dag node
        n (int): number of positions

    Returns:
        list: list of positions (translations)
    """
    awp = a
    bwp = b
    if isinstance(a, str):
        awp = cmds.xform(a, query=True, worldSpace=True, translation=True)
    if isinstance(b, str):
        bwp = cmds.xform(b, query=True, worldSpace=True, translation=True)
    atob = [bb - aa for aa, bb in zip(awp, bwp)]
    return list([p + (inc/(n-1)) * index for p, inc in zip(awp, atob)]
                for index in range(n))


def get_n_matrices_from_a_to_b(a, b, n):
    """
    Get a number of matrices between two points

    Args:
        a (str): dag node
        b (str): dag node
        n (int): number of positions

    Returns:
        list: list of matrices
    """
    position_list = get_n_positions_from_a_to_b(a, b, n)
    a_rotation = cmds.xform(a, query=True, worldSpace=True, rotation=True)
    matrices_list = list()
    for i in range(n):
        temp_transform = cmds.createNode('transform', name='temp')

        cmds.xform(temp_transform, worldSpace=True, translation=position_list[i])
        cmds.xform(temp_transform, worldSpace=True, rotation=a_rotation)

        i_matrix = cmds.xform(temp_transform, query=True, worldSpace=True, matrix=True)
        matrices_list.append(i_matrix)

        cmds.delete(temp_transform)

    return matrices_list


def get_percentage_positions_from_a_to_b(a, b, percentage_values=None):
    """
    Get a number of positions between two points given percentages

    Args:
        a (str): dag node
        b (str): dag node
        percentage_values (list): percentages. Defaults to None.

    Returns:
        list: list of positions (translations)
    """
    if percentage_values is None:
        percentage_values = [0, 0.25, 0.5, 0.75, 1]
    awp = a
    bwp = b
    if isinstance(a, str):
        awp = cmds.xform(a, query=True, worldSpace=True, translation=True)
    if isinstance(b, str):
        bwp = cmds.xform(b, query=True, worldSpace=True, translation=True)

    atob = [bb - aa for aa, bb in zip(awp, bwp)]

    pos_values = []
    for value in percentage_values:
        pos = [init_pos + (dis * value) for init_pos, dis in zip(awp, atob)]
        pos_values.append(pos)
    return pos_values


def get_percentage_matrices_from_a_to_b(a, b, percentage_values=None):
    """
    Get a number of positions between two points given percentages

    Args:
        a (str): dag node
        b (str): dag node
        percentage_values (list): percentages. Defaults to None.

    Returns:
        list: list of matrices
    """
    position_list = get_percentage_positions_from_a_to_b(a, b, percentage_values)
    a_rotation = cmds.xform(a, query=True, worldSpace=True, rotation=True)
    matrices_list = list()
    for i in range(len(percentage_values)):
        temp_transform = cmds.createNode('transform', name='temp')

        cmds.xform(temp_transform, worldSpace=True, translation=position_list[i])
        cmds.xform(temp_transform, worldSpace=True, rotation=a_rotation)

        i_matrix = cmds.xform(temp_transform, query=True, worldSpace=True, matrix=True)
        matrices_list.append(i_matrix)

        cmds.delete(temp_transform)

    return matrices_list


def inverse_matrix(matrix_a):
    """
    Get the inverse matrix of the matrix given

    Args:
        matrix_a (matrix): matrix

    Returns:
        matrix: inverse matrix
    """
    matrix_result = identity_matrix

    a_rows = list()
    result_rows = list()

    for index in range(4):
        a_rows.append(matrix_a[index*4:(index*4)+4])
        result_rows.append(matrix_result[index*4:(index*4)+4])

    indices = list(range(4))
    for row in range(4):
        if a_rows[row][row] == 0:  # Error when we divide by zero
            row_scale = 1.0
        else:
            row_scale = 1.0 / a_rows[row][row]

        for column in range(4):
            a_rows[row][column] *= row_scale
            result_rows[row][column] *= row_scale
        for i in indices[0:row] + indices[row + 1:]:
            current_row_scale = a_rows[i][row]
            for column in range(4):
                a_rows[i][column] = a_rows[i][column] - current_row_scale * a_rows[row][column]
                result_rows[i][column] = result_rows[i][column] - current_row_scale * result_rows[row][column]

    matrix_result_clean = list()
    for index in range(len(result_rows)):
        matrix_result_clean.extend(result_rows[index])

    return matrix_result_clean


def multiply_matrices_4_by_4(matrix_a, matrix_b):
    """
    Multiply 2 matrices

    Args:
        matrix_a (matrix): matrix
        matrix_b (matrix): matrix

    Returns:
        matrix: matrix result
    """
    a_rows = list()
    b_rows = list()
    for index in range(4):
        a_rows.append(matrix_a[index*4:(index*4)+4])
        b_rows.append(matrix_b[index*4:(index*4)+4])

    matrix_result = [[0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0]]

    for a_row in range(len(a_rows)):
        for b_column in range(len(b_rows[0])):
            for b_row in range(len(b_rows)):
                matrix_result[a_row][b_column] += a_rows[a_row][b_row] * b_rows[b_row][b_column]

    matrix_result_clean = list()
    for index in range(len(matrix_result)):
        matrix_result_clean.extend(matrix_result[index])

    return matrix_result_clean


def get_center_pivot(input_list):
    """
    Get the center position of the nodes or components given

    Args:
        input_list (list): list of inputs

    Returns:
        center_pivot: [x, y, z]
    """
    x_min, y_min, z_min, x_max, y_max, z_max = cmds.exactWorldBoundingBox(input_list)

    return [0.5*(x_min + x_max), 0.5*(y_min + y_max), 0.5*(z_min + z_max)]
