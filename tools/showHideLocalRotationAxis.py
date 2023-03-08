from maya import cmds


def show_local_rotation_axis(hierarchy=False, *args):
    if hierarchy:
        cmds.select(hierarchy=True)
    selection_list = cmds.ls(sl=True)

    for node in selection_list:
        if cmds.attributeQuery('displayLocalAxis', node=node, exists=True):
            cmds.setAttr('{}.displayLocalAxis'.format(node), True)


def hide_local_rotation_axis(hierarchy=False, *args):
    if hierarchy:
        cmds.select(hierarchy=True)
    selection_list = cmds.ls(sl=True)

    for node in selection_list:
        if cmds.attributeQuery('displayLocalAxis', node=node, exists=True):
            cmds.setAttr('{}.displayLocalAxis'.format(node), False)