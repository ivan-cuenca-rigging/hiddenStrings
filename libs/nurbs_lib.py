# Maya imports
from maya import cmds

# Project imports
from hiddenStrings.libs import usage_lib


def create_nurbs_from_points(descriptor,
                             side,
                             points_list,
                             width=0.2,
                             axis='X'):
    """
    Create a nurbs with the points given

    Args:
        descriptor (str): descriptor
        side (str): side
        points_list (list): list of points
        width (float, optional): width of the nurbs. Defaults to 0.2.
        axis (str, optional): axis of the nurbs. Defaults to 'X'.

    Returns:
        str: nurbs transform
    """
    positions = list()
    for point in points_list:
        positions.append(cmds.xform(point, query=True, worldSpace=True, translation=True))

    crv_0 = cmds.curve(p=positions, degree=3)
    crv_1 = cmds.curve(p=positions, degree=3)
    cmds.setAttr('{}.translate{}'.format(crv_0, axis.upper()), -width/2)
    cmds.setAttr('{}.translate{}'.format(crv_1, axis.upper()), width/2)

    nurbs_transform = cmds.loft(crv_0, crv_1, degree=3, constructionHistory=False)
    nurbs_transform = cmds.rename(nurbs_transform, '{}_{}_{}'.format(descriptor, side, usage_lib.nurbs))

    cmds.delete(crv_0, crv_1)

    return nurbs_transform
