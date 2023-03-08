from maya import cmds


"""
old solution, needs a clean up
"""

"""
push_joint(parent_nd='upArm08_r_jnt', rotate_nd='lowArm01_r_skn', 
               forbidden_word='01', push_axis='z', 
               pos_axis=True, neg_axis=True)
"""


# Push Joint System
def push_joint(parent_nd='upArm08_r_jnt', rotate_nd='lowArm01_r_skn',
               forbidden_word='01', push_axis='z',
               pos_axis=True, neg_axis=True):
    desc, side, usage = rotate_nd.split('_')
    if forbidden_word:
        desc = ''.join(desc.split(forbidden_word))

    # BlendMatrix to get the rotation divided by 2
    rot_bm = cmds.createNode('blendMatrix', name='{}PushT{}_{}_blendmat'.format(desc, push_axis, side))
    cmds.connectAttr('{}.worldMatrix'.format(parent_nd), '{}.inputMatrix'.format(rot_bm))
    cmds.connectAttr('{}.worldMatrix'.format(rotate_nd), '{}.target[0].targetMatrix'.format(rot_bm))
    cmds.connectAttr('{}.worldMatrix'.format(rotate_nd), '{}.target[1].targetMatrix'.format(rot_bm))
    cmds.setAttr('{}.target[0].useScale'.format(rot_bm), 0)
    cmds.setAttr('{}.target[0].useShear'.format(rot_bm), 0)
    cmds.setAttr('{}.target[0].useRotate'.format(rot_bm), 0)
    cmds.setAttr('{}.target[1].weight'.format(rot_bm), 0.5)
    cmds.setAttr('{}.target[1].useTranslate'.format(rot_bm), 0)
    cmds.setAttr('{}.target[1].useScale'.format(rot_bm), 0)
    cmds.setAttr('{}.target[1].useShear'.format(rot_bm), 0)

    # Counter pushJoint matrix
    rot_mm = cmds.createNode('multMatrix', name='{}PushT{}_{}_multmat'.format(desc, push_axis, side))
    cmds.connectAttr('{}.outputMatrix'.format(rot_bm), '{}.matrixIn[0]'.format(rot_mm))
    cmds.connectAttr('{}.worldInverseMatrix'.format(parent_nd), '{}.matrixIn[1]'.format(rot_mm))

    # Decompose the matrix to get the rotation in 1 axis
    rot_dm = cmds.createNode('decomposeMatrix', name='{}PushT{}_{}_decmat'.format(desc, push_axis, side))
    cmds.connectAttr('{}.matrixSum'.format(rot_mm), '{}.inputMatrix'.format(rot_dm))

    # Create and connect joints
    push_axis_side = []
    if pos_axis: push_axis_side.append('Pos')
    if neg_axis: push_axis_side.append('Neg')

    for axis_side in push_axis_side:
        jnt = create_joint(jnt_name='{}PushT{}{}_{}_skn'.format(desc, push_axis, axis_side, side), parent_nd=parent_nd,
                           position_nd=rotate_nd)[0]

        cmds.connectAttr('{}.matrixSum'.format(rot_mm), '{}.offsetParentMatrix'.format(jnt))

        rot_mult = cmds.createNode('multDoubleLinear',
                                   name='{}PushT{}{}_{}_multmat'.format(desc, push_axis, axis_side, side))
        cmds.connectAttr('{}.outputRotateY'.format(rot_dm), '{}.input1'.format(rot_mult))
        cmds.connectAttr('{}.output'.format(rot_mult), '{}.t{}'.format(jnt, push_axis))


def create_joint(jnt_name='', parent_nd='', position_nd=''):
    desc, side, usage = jnt_name.split('_')

    jnt_zero = cmds.createNode('transform', name='{}{}_{}_zero'.format(desc, usage.capitalize(), side),
                               parent=parent_nd)
    jnt = cmds.createNode('joint', name=jnt_name, parent=jnt_zero)

    position_mat = cmds.xform(position_nd, query=True, worldSpace=True, matrix=True)
    cmds.xform(jnt_zero, worldSpace=True, matrix=position_mat)
    return jnt, jnt_zero
