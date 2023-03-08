# Maya imports
from maya import cmds

# Project imports
from hiddenStrings.libs import sideLib, usageLib


def delete_guides(*args):
    guides_grp = 'guides_{}_{}'.format(sideLib.center, usageLib.group)
    if cmds.objExists(guides_grp):
        cmds.delete(cmds.ls(guides_grp))
    else:
        cmds.warning('{} does not exists'.format(guides_grp))