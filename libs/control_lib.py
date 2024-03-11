# Imports
import logging

# Maya imports
from maya import cmds

# Project imports
from hiddenStrings.libs import usage_lib, spline_lib, node_lib, attribute_lib

logging = logging.getLogger(__name__)


class Helper(node_lib.Helper, attribute_lib.Helper):
    """
    control Helper class

    Args:
        name (str): name of the control
    """
    def __init__(self, name):
        """
        Initializes an instance of control's Helper

        Args:
            name (str): name of the control
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
            logging.info('this control has not a valid usage, use "{}".'.format(usage_lib.control_valid_usages))

    # ---------- Get and Set Methods ----------
    def get_shape(self):
        """
        Get the shape of the node

        Returns:
            list: list of the shapes
        """
        return spline_lib.get_shapes(self.name)

    def set_shape(self, shape_name, offset, shape_scale=1):
        """
        Set the control shape

        Args:
            shape_name (str): name of the shape node
            offset (dict): E.G. {translateY:1}
            shape_scale (float, optional): _description_. Defaults to 1.
        """
        spline_lib.set_shape(node=self.name, shape_name=shape_name, shape_scale=shape_scale, shape_offset=offset)

    def set_shape_color(self, color_key='yellow'):
        """
        Override the control's color

        Args:
            color_key (str, optional): check valid colors in the spline_lib. Defaults to 'yellow'.
        """
        spline_lib.set_override_color([self.name], color_key=color_key)

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
        Create the control

        Args:
            as_joint (bool, optional): True == control will be a joint else: will be a transform node. Defaults to True.
            zero (bool, optional): create zero node. Defaults to False.
            parent (_type_, optional): parent of the control. Defaults to None.
            matrix (_type_, optional): matrix of the control. Defaults to None.
            matrix_translation (bool, optional): True == only translation will be used. Defaults to False.
            matrix_rotation (bool, optional): True == only rotation will be used. Defaults to False.
            shape (_type_, optional): name of the spline node. Defaults to None.
            shape_scale (float, optional): scale of the control shape. Defaults to 1.
            shape_offset (dict, optional): E.G. {'translateY': 1}. Defaults to False.
            color_key (str, optional): check color in the spline_lib. Defaults to 'yellow'.

        Returns:
            str: name of the control
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
