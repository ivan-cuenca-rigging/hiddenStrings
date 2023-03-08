from maya import cmds


"""
old solution, needs a clean up
"""


def run(control_name='test_c_ctr',
        attr_name='rotateX',
        attr_value=90,
        geometry_name='test_c_geo',
        create_sdk=True,
        connect_to_joint=True,
        joint_usage='skn'):
    # INPUTS
    default_attr_value = cmds.getAttr('{}.{}'.format(control_name, attr_name))
    # Tokens
    control_tokens = control_name.split('_')
    if len(control_tokens) != 3:
        cmds.error('Control name must have 3 tokens separated by "_"')
    desc, side, usage = control_tokens

    # Get blendshape
    geometry_shape = cmds.listRelatives(geometry_name, shapes=True)[0]
    blendshape_name = [x for x in cmds.listHistory(geometry_name) if cmds.nodeType(x) == 'blendShape']
    if not blendshape_name:
        cmds.error('The geometry given has not a blendshape')
    blendshape_name = blendshape_name[0]

    # Create target
    attr_value_formatted = 'm{}'.format(str(attr_value)[1:]) if str(attr_value)[0] == '-' else str(attr_value)

    target_index = int(cmds.blendShape(geometry_shape, query=True, weightCount=True))
    target_name = '{}{}{}{}_{}_crr'.format(desc, attr_name[0].upper(), attr_name[-1].upper(), attr_value_formatted,
                                           side)
    geometry_target_name = cmds.duplicate(geometry_name, name=target_name)[0]

    cmds.blendShape(blendshape_name, edit=True,
                    target=(str(geometry_shape), target_index, str(geometry_target_name), 1), weight=(target_index, 1))
    cmds.blendShape(blendshape_name, edit=True, resetTargetDelta=(0, target_index))
    cmds.sculptTarget(blendshape_name, edit=True, target=target_index)
    cmds.delete(geometry_target_name)

    # Anim curve creation
    if create_sdk:
        sdk_name = '{}{}{}{}_{}_acrv'.format(desc, attr_name[0].upper(), attr_name[-1].upper(),
                                             attr_value_formatted, side)
        sdk_name = cmds.createNode('animCurveUU', name=sdk_name)
        cmds.setKeyframe(sdk_name, float=default_attr_value, value=0, inTangentType='linear', outTangentType='linear')
        cmds.setKeyframe(sdk_name, float=attr_value, value=1, inTangentType='linear', outTangentType='linear')

        # Connections
        driver_name = '{}_{}_{}'.format(desc, side, joint_usage) if connect_to_joint else control_name
        cmds.connectAttr('{}.{}'.format(driver_name, attr_name), '{}.input'.format(sdk_name))
        cmds.connectAttr('{}.output'.format(sdk_name), '{}.{}'.format(blendshape_name, target_name))

    # Get geometry delta
    cmds.refresh()
    delta_mush_name = cmds.deltaMush(geometry_name,
                                     smoothingIterations=10, smoothingStep=0.5, envelope=1,
                                     name='{}{}_{}_dm'.format(desc, usage.capitalize(), side))[0]
    cmds.setAttr('{}.distanceWeight'.format(delta_mush_name), 1)
    cmds.setAttr('{}.inwardConstraint'.format(delta_mush_name), 1)

    cmds.refresh()
    skin_name = [x for x in cmds.listHistory(geometry_name) if cmds.nodeType(x) == 'skinCluster']
    if not skin_name:
        cmds.error('The geometry given has not a skinCluster')
    skin_name = skin_name[0]
    cmds.setAttr('{}.skinningMethod'.format(skin_name), 1)

    cmds.refresh()
    cmds.setAttr('{}.{}'.format(control_name, attr_name), attr_value)

    cmds.refresh()
    geometry_delta = cmds.duplicate(geometry_name, name=target_name)[0]

    cmds.refresh()
    cmds.setAttr('{}.skinningMethod'.format(skin_name), 0)
    cmds.delete(delta_mush_name)

    cmds.refresh()
    send_mesh.run(elemList=[geometry_delta, geometry_name])
    cmds.delete(geometry_delta)
    cmds.setAttr('{}.{}'.format(control_name, attr_name), default_attr_value)
    if not create_sdk:
        cmds.setAttr('{}.{}'.format(blendshape_name, target_name), 0)
