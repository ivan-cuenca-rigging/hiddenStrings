# Maya imports
from maya import cmds

# Project imports
from hiddenStrings.libs import node_lib, side_lib, usage_lib, spline_lib, skeleton_lib, math_lib


class Helper(node_lib.Helper):
    def __init__(self, name):
        """
        :param name: str
        """
        super(Helper, self).__init__(name)
        self.name = name
        self.check_usage()

        self.guides_grp = 'guides_{}_{}'.format(side_lib.center, usage_lib.group)
        self.vis_labels_attribute = 'visLabels'

    #
    # ---------- Checks Methods ----------
    def check_usage(self):
        """
        Check if the usage is in the guides usage_lib
        """
        if self.get_usage() not in usage_lib.guide_valid_usages:
            cmds.warning('this guide has not a valid usage, use {}'.format(usage_lib.guide_valid_usages))

    # ---------- Set Methods ----------
    def set_shape_color(self, color_key='yellow'):
        """
        Override control's color
        :param color_key: str, check valid colors in the lib
        """
        spline_lib.set_override_color([self.name], color_key=color_key)

    def set_shape(self, shape_name='sphere', shape_scale=0.25):
        """
        Set guide's shape
        :param shape_name: float
        :param shape_scale: str, from libs/spline_shapes
        """
        spline_lib.set_shape(node=self.name, shape_name=shape_name, shape_scale=shape_scale)

    def set_draw_label(self, value):
        """
        break the incoming connection from guides_grp and set the draw label
        :param value: bool
        """
        cmds.setAttr('{}.drawLabel'.format(self.name), value)

    # ---------- Create Methods ----------
    def create(self,
               guide_shape_scale=0.25,
               parent=None):
        """
        Create a guide
        :param guide_shape_scale: float, scale of the guide's shape
        :param parent: string
        :return: guide's name
        """

        # Check if exists
        if cmds.objExists(self.name):
            cmds.error('the {} already exists in the scene'.format(self.name))

        self.name = cmds.createNode('joint', name=self.name)

        # Add the shape to the guide
        self.set_shape(shape_scale=guide_shape_scale)
        cmds.setAttr('{}.radius'.format(self.name), 0)

        # Lock attributes
        self.lock_and_hide_attributes(['scaleX', 'scaleY', 'scaleZ', 'radius', 'visibility'])

        # Draw guide's label
        skeleton_lib.set_joint_guide_label(self.name)
        cmds.setAttr('{}.side'.format(self.name), 0)
        self.set_draw_label(True)
        cmds.setAttr('{}.drawLabel'.format(self.name), keyable=True)

        if parent:
            cmds.parent(self.name, parent)

        return self.name

    # ---------- Connect Methods ----------
    def connect_to_opposite_side(self):
        if self.side == side_lib.center:
            cmds.error('the guide "{}" does not have opposite side'.format(self.name))

        opposite_side = side_lib.left if self.side == side_lib.right else side_lib.right

        opposite_name = '{}_{}_{}'.format(self.descriptor, opposite_side, self.usage)
        if not cmds.objExists(opposite_name):
            cmds.warning('{} does not exist in the scene, cannot connect opposite side'.format(opposite_name))
        else:
            mult_matrix = cmds.createNode('multMatrix', name='{}{}_{}_{}'.format(self.descriptor,
                                                                                 self.usage.capitalize(),
                                                                                 self.side,
                                                                                 usage_lib.mult_matrix))

            cmds.connectAttr('{}.worldMatrix'.format(opposite_name), '{}.matrixIn[0]'.format(mult_matrix))
            cmds.setAttr('{}.matrixIn[1]'.format(mult_matrix), math_lib.identity_matrix_x_negative, type='matrix')

            cmds.connectAttr('{}.matrixSum'.format(mult_matrix), '{}.offsetParentMatrix'.format(self.name))

    def connect_to_opposite_side_with_parent(self, parent_node):
        if self.side == side_lib.center:
            cmds.error('the guide "{}" does not have opposite side'.format(self.name))

        opposite_side = side_lib.left if self.side == side_lib.right else side_lib.right

        opposite_name = '{}_{}_{}'.format(self.descriptor, opposite_side, self.usage)
        if not cmds.objExists(opposite_name):
            cmds.warning('{} does not exist in the scene, cannot connect opposite side'.format(opposite_name))
        else:
            mult_matrix = cmds.createNode('multMatrix', name='{}{}_{}_{}'.format(self.descriptor,
                                                                                 self.usage.capitalize(),
                                                                                 self.side,
                                                                                 usage_lib.mult_matrix))

            cmds.connectAttr('{}.matrix'.format(opposite_name), '{}.matrixIn[0]'.format(mult_matrix))
            cmds.connectAttr('{}.worldMatrix'.format(parent_node), '{}.matrixIn[1]'.format(mult_matrix))

            cmds.connectAttr('{}.matrixSum'.format(mult_matrix), '{}.offsetParentMatrix'.format(self.name))


def delete_guides(*args):
    guides_grp = 'guides_{}_{}'.format(side_lib.center, usage_lib.group)
    if cmds.objExists(guides_grp):
        cmds.delete(cmds.ls(guides_grp))
    else:
        cmds.warning('{} does not exists'.format(guides_grp))
