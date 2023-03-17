
"""
sides for all the nodes in maya
"""

center = 'c'
left = 'l'
right = 'r'
valid_sides = [center, left, right]


def get_opposite_side(side):
    """
    Get the opposite side
    :return: opposite side
    """
    if side == left:
        return right
    elif side == right:
        return left
    else:
        return center
