# Maya imports
from maya import cmds

# Project imports
from hiddenStrings.libs import usageLib


def create_nurbs_from_points(descriptor,
                             side,
                             points,
                             width=0.2,
                             axis='X'):
    positions = list()
    for point in points:
        positions.append(cmds.xform(point, query=True, worldSpace=True, translation=True))

    crv_0 = cmds.curve(p=positions, degree=1)
    crv_1 = cmds.curve(p=positions, degree=1)
    cmds.setAttr('{}.translate{}'.format(crv_0, axis.upper()), -width/2)
    cmds.setAttr('{}.translate{}'.format(crv_1, axis.upper()), width/2)

    nurbs_transform = cmds.loft(crv_0, crv_1, degree=3, constructionHistory=False)
    nurbs_transform = cmds.rename(nurbs_transform, '{}_{}_{}'.format(descriptor, side, usageLib.nurbs))

    cmds.rebuildSurface(nurbs_transform, constructionHistory=False, replaceOriginal=True, rebuildType=0,
                        keepRange=False, keepControlPoints=False, direction=2,
                        spansU=1, degreeU=1, spansV=int(len(points)), degreeV=3)

    cmds.delete(crv_0, crv_1)

    return nurbs_transform
