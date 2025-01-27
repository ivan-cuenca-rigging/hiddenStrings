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
    cmds.setAttr(f'{crv_0}.translate{axis.upper()}', -width/2)
    cmds.setAttr(f'{crv_1}.translate{axis.upper()}', width/2)

    nurbs_transform = cmds.loft(crv_0, crv_1, degree=3, constructionHistory=False)
    nurbs_transform = cmds.rename(nurbs_transform, f'{descriptor}_{side}_{usage_lib.nurbs}')

    cmds.delete(crv_0, crv_1)

    cmds.rebuildSurface(nurbs_transform,
                        replaceOriginal=True,
                        rebuildType=0,
                        endKnots=1,
                        keepRange=False,
                        keepControlPoints=False,
                        keepCorners=False,
                        spansU=0,
                        degreeU=1,
                        spansV=0,
                        degreeV=3,
                        fitRebuild=False,
                        direction=2)

    return nurbs_transform


def get_param_along_x(nurbs):
    """
    Detects if the change on the X axis is related to U or V of a NURBS surface.

    Args:
        nurbs (str): Name of the NURBS surface (e.g., 'test_c_nurbs').

    Returns:
        str: 'U' or 'V', depending on which axis affects X.
    """
    # Key CV points in U and V:
    cv_u0_v0 = cmds.xform(f'{nurbs}.cv[0][0]', q=True, ws=True, t=True)  # U=0, V=0
    cv_u1_v0 = cmds.xform(f'{nurbs}.cv[1][0]', q=True, ws=True, t=True)  # U=1, V=0
    cv_u0_v1 = cmds.xform(f'{nurbs}.cv[0][1]', q=True, ws=True, t=True)  # U=0, V=1

    # Changes on the X axis:
    delta_u_x = abs(cv_u1_v0[0] - cv_u0_v0[0])  # Change in X along U
    delta_v_x = abs(cv_u0_v1[0] - cv_u0_v0[0])  # Change in X along V

    # Determines which axis causes the change:
    if delta_u_x > delta_v_x:
        return 'U'
    else:
        return 'V'
