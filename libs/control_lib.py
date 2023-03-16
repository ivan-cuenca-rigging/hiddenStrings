# Maya imports
from maya import cmds

from hiddenStrings.libs import usage_lib, spline_lib, node_lib, attribute_lib


class Helper(node_lib.Helper, attribute_lib.Helper):
    def __init__(self, name):
        """
        :param name: str
        """
        super(Helper, self).__init__(name)

        self.name = name
        self.check_usage()
        self.check_side()

    # ---------- Checks Methods ----------
    def check_usage(self):
        """
        Check if the usage is valid
        """
        if self.get_usage() not in usage_lib.control_valid_usages:
            cmds.warning('this control has not a valid usage, use {}'.format(usage_lib.control_valid_usages))

    # ---------- Get and Set Methods ----------
    def get_shape(self):
        """
        get the shapes' node
        :return: shapes' list
        """
        return spline_lib.get_shapes(self.name)

    def set_shape(self, shape_name, offset, shape_scale=1):
        """
        Set a new shape for the control
        :param shape_name: str, spline node name
        :param offset: dict, E.g. shape_offset[ty]=1
        :param shape_scale: float
        """
        spline_lib.set_shape(node=self.name, shape_name=shape_name, shape_scale=shape_scale, shape_offset=offset)

    def set_shape_color(self, color_key='yellow'):
        """
        Override control's color
        :param color_key: str, check valid colors in the lib
        """
        spline_lib.override_color([self.name], color_key=color_key)

    # ---------- Create Method ----------
    def create(self,
               as_joint=True,
               zero=False,
               parent=None,
               matrix=None,
               matrix_translation=False,
               matrix_rotation=False,
               shape=None,
               shape_scale=1,
               shape_offset=False,
               color_key='yellow'):
        """
        Create a control
        :param as_joint: bool, if yes the control will be a joint if not, it will be a transform node
        :param zero: bool, if yes it will create a zero group
        :param parent: str, control's parent
        :param matrix: matrix, control's matrix
        :param matrix_translation: bool, if true only translation will be used
        :param matrix_rotation: bool, if true only rotation will be used
        :param shape: str, spline node's name
        :param shape_scale: float
        :param shape_offset: dict, E.g. shape_offset=dict(); shape_offset['translateY'] = 1
        :param color_key: str, check color in the lib
        :return: control's name
        """
        # Check if the control already exists
        if cmds.objExists(self.name):
            cmds.error('the {} already exists in the scene'.format(self.name))

        # Create control as joint or transform
        ctr_type = 'joint' if as_joint else 'transform'
        cmds.createNode(ctr_type, name=self.name)

        # lock and hide attributes
        ctr_ah = attribute_lib.Helper(self.name)
        ctr_ah.lock_and_hide_attribute('visibility')

        if ctr_type == 'joint':
            cmds.setAttr('{}.drawStyle'.format(self.name), 2)
            ctr_ah.lock_and_hide_attribute('radius')

        # Checks
        if zero:
            self.create_zero()
        if parent:
            self.set_parent(parent)

        if shape:
            self.set_shape(shape_name=shape, shape_scale=shape_scale, offset=shape_offset)
            self.set_shape_color(color_key=color_key)

        if matrix:
            self.set_offset_parent_matrix(matrix, translation=matrix_translation, rotation=matrix_rotation)

        cmds.select(self.name)

        return self.name
