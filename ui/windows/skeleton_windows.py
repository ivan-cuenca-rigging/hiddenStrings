# Imports
import os
from functools import partial

# Maya imports
from maya import cmds

# Project imports
from hiddenStrings.libs import window_lib, skeleton_lib, usage_lib


class CreateSkeletonChainWindow(window_lib.Helper):
    """
    Create a skeleton chain
    
    Args:
        title (str): title of the window
        size (list): width and height
    """

    def __init__(self, *args):
        """
        Initializes an instance of CreateSkeletonChain

        Args:
            title (str): title of the window
            size (list): width and height
        """
        super(CreateSkeletonChainWindow, self).__init__(title='Create skeleton chain', size=(450, 240))

        # Descriptor
        self.descriptor = cmds.textFieldGrp(label='Descriptor: ')

        # Side
        self.side = cmds.optionMenu(label='Side')
        cmds.menuItem(self.side, label='Left')
        cmds.menuItem(self.side, label='Center')
        cmds.menuItem(self.side, label='Right')
        cmds.optionMenu(self.side, edit=True, value='Center')

        # joint usage
        self.usage = cmds.optionMenu(label='Usage')
        for valid_usage in usage_lib.skeleton_valid_usages:
            cmds.menuItem(self.usage, label=valid_usage)

        cmds.optionMenu(self.usage, edit=True, value=usage_lib.skin_joint)

        # A
        self.start_node = cmds.textFieldGrp(label='Start node: ')
        self.get_start_node = cmds.iconTextButton(image='addClip.png',
                                                  command=partial(self.get_last_selection_and_set_text_field,
                                                                  text_field=self.start_node))
        # B
        self.end_node = cmds.textFieldGrp(label='End node: ')
        self.get_end_node = cmds.iconTextButton(image='addClip.png',
                                                command=partial(self.get_last_selection_and_set_text_field,
                                                                text_field=self.end_node))
        # Number of joints
        self.joints_number = cmds.intSliderGrp(label='Number of joints: ', field=True,
                                               value=20, maxValue=50, columnWidth=[1, 170])
        # Parent of the joints
        self.parent_node = cmds.textFieldGrp(label='Parent: ')
        self.get_parent = cmds.iconTextButton(image='addClip.png',
                                              command=partial(self.get_last_selection_and_set_text_field,
                                                              text_field=self.parent_node))

        # --------------------------------------------------------------------------------------------------------------
        cmds.formLayout(self.main_layout, edit=True,
                        attachForm=[(self.descriptor, 'top', 10),
                                    (self.side, 'left', 115),
                                    (self.usage, 'left', 105),
                                    (self.joints_number, 'left', -30)],

                        attachControl=[(self.side, 'top', 5, self.descriptor),
                                       (self.usage, 'top', 5, self.side),
                                       (self.start_node, 'top', 5, self.usage),
                                       (self.get_start_node, 'top', 5, self.usage),
                                       (self.get_start_node, 'left', 5, self.start_node),
                                       (self.end_node, 'top', 5, self.start_node),
                                       (self.get_end_node, 'top', 5, self.start_node),
                                       (self.get_end_node, 'left', 5, self.end_node),
                                       (self.joints_number, 'top', 5, self.end_node),
                                       (self.parent_node, 'top', 5, self.joints_number),
                                       (self.get_parent, 'top', 5, self.joints_number),
                                       (self.get_parent, 'left', 5, self.parent_node)])

    def apply_command(self, *args):
        descriptor = cmds.textFieldGrp(self.descriptor, query=True, text=True)

        side = cmds.optionMenu(self.side, query=True, value=True)
        if side == 'Left':
            side = 'l'
        if side == 'Center':
            side = 'c'
        if side == 'Right':
            side = 'r'

        usage = cmds.optionMenu(self.usage, query=True, value=True)

        start_node = cmds.textFieldGrp(self.start_node, query=True, text=True)

        end_node = cmds.textFieldGrp(self.end_node, query=True, text=True)

        joints_number = cmds.intSliderGrp(self.joints_number, query=True, value=True)

        parent_node = cmds.textFieldGrp(self.parent_node, query=True, text=True)

        skeleton_lib.create_skeleton_chain_from_a_to_b(descriptor=descriptor,
                                                       side=side,
                                                       joint_usage=usage,
                                                       a=start_node,
                                                       b=end_node,
                                                       joints_number=joints_number,
                                                       joints_parent=parent_node)


class CreateRibbonJoints(window_lib.Helper):
    """
    Create a skeleton chain
    
    Args:
        title (str): title of the window
        size (list): width and height
    """

    def __init__(self, *args):
        """
        Initializes an instance of CreateSkeletonChain

        Args:
            title (str): title of the window
            size (list): width and height
        """
        super(CreateRibbonJoints, self).__init__(title='Create ribbon joints', size=(450, 350))

        # Descriptor
        self.descriptor = cmds.textFieldGrp(label='Descriptor: ')

        # Side
        self.side = cmds.optionMenu(label='Side')
        cmds.menuItem(self.side, label='Left')
        cmds.menuItem(self.side, label='Center')
        cmds.menuItem(self.side, label='Right')
        cmds.optionMenu(self.side, edit=True, value='Center')

        # joint usage
        self.usage = cmds.optionMenu(label='Usage')
        for valid_usage in usage_lib.skeleton_valid_usages:
            cmds.menuItem(self.usage, label=valid_usage)

        cmds.optionMenu(self.usage, edit=True, value=usage_lib.skin_joint)

        # Nurbs
        self.nurbs_node = cmds.textFieldGrp(label='Nurbs: ')
        self.get_nurbs_node = cmds.iconTextButton(image='addClip.png',
                                                  command=partial(self.get_last_selection_and_set_text_field,
                                                                  text_field=self.nurbs_node))
        # Direction
        self.direction = cmds.optionMenu(label='Direction')
        cmds.menuItem(self.side, label='U')
        cmds.menuItem(self.side, label='V')
        cmds.optionMenu(self.direction, edit=True, value='U')

        # Number of joints
        self.joints_number = cmds.intSliderGrp(label='Number of joints: ', field=True,
                                               value=20, maxValue=50, columnWidth=[1, 170])
        # Parent of the joints
        self.parent_node = cmds.textFieldGrp(label='Parent: ')
        self.get_parent = cmds.iconTextButton(image='addClip.png',
                                              command=partial(self.get_last_selection_and_set_text_field,
                                                              text_field=self.parent_node))

        # Create uvPin
        separator01 = cmds.separator(height=5)

        self.create_uv_pin = cmds.checkBoxGrp(label='Create uvPin: ', value1=True,
                                              onCommand=self.set_create_uv_pin_list_enable,
                                              offCommand=self.set_create_uv_pin_list_enable)
        
        self.use_translate = cmds.checkBoxGrp(label='useTranslate: ', value1=True)
        self.use_rotate = cmds.checkBoxGrp(label='useRotate: ', value1=True)
        self.use_scale = cmds.checkBoxGrp(label='useScale: ', value1=True)
        self.use_shear = cmds.checkBoxGrp(label='useShear: ', value1=True)

        # --------------------------------------------------------------------------------------------------------------
        cmds.formLayout(self.main_layout, edit=True,
                        attachForm=[(self.descriptor, 'top', 10),
                                    (self.side, 'left', 115),
                                    (self.usage, 'left', 105),
                                    (self.direction, 'left', 90),
                                    (self.joints_number, 'left', -30),
                                    (self.use_translate, 'left', 25),
                                    (self.use_rotate, 'left', 25),
                                    (self.use_scale, 'left', 25),
                                    (self.use_shear, 'left', 25),
                                    (separator01, 'left', 5), (separator01, 'right', 5)],

                        attachControl=[(self.side, 'top', 5, self.descriptor),
                                       (self.usage, 'top', 5, self.side),
                                       (self.nurbs_node, 'top', 5, self.usage),
                                       (self.get_nurbs_node, 'top', 5, self.usage),
                                       (self.get_nurbs_node, 'left', 5, self.nurbs_node),
                                       (self.direction, 'top', 5, self.nurbs_node),
                                       (self.joints_number, 'top', 5, self.direction),
                                       (self.parent_node, 'top', 5, self.joints_number),
                                       (self.get_parent, 'top', 5, self.joints_number),
                                       (self.get_parent, 'left', 5, self.parent_node),
                                       (separator01, 'top', 5, self.get_parent),
                                       (self.create_uv_pin, 'top', 5, separator01),
                                       (self.use_translate, 'top', 5, self.create_uv_pin),
                                       (self.use_rotate, 'top', 5, self.use_translate),
                                       (self.use_scale, 'top', 5, self.use_rotate),
                                       (self.use_shear, 'top', 5, self.use_scale)])

    def apply_command(self, *args):
        descriptor = cmds.textFieldGrp(self.descriptor, query=True, text=True)

        side = cmds.optionMenu(self.side, query=True, value=True)
        if side == 'Left':
            side = 'l'
        if side == 'Center':
            side = 'c'
        if side == 'Right':
            side = 'r'

        usage = cmds.optionMenu(self.usage, query=True, value=True)

        nurbs_node = cmds.textFieldGrp(self.nurbs_node, query=True, text=True)

        direction = cmds.optionMenu(self.direction, query=True, value=True)

        joints_number = cmds.intSliderGrp(self.joints_number, query=True, value=True)

        parent_node = cmds.textFieldGrp(self.parent_node, query=True, text=True)

        create_uv_pin = cmds.checkBoxGrp(self.create_uv_pin, query=True, value1=True)

        use_translate = cmds.checkBoxGrp(self.use_translate, query=True, value1=True)
        use_rotate = cmds.checkBoxGrp(self.use_rotate, query=True, value1=True)
        use_scale = cmds.checkBoxGrp(self.use_scale, query=True, value1=True)
        use_shear = cmds.checkBoxGrp(self.use_shear, query=True, value1=True)

        skeleton_lib.create_n_joints_in_a_nurbs(descriptor=descriptor,
                                                side=side,
                                                joint_usage=usage,
                                                nurbs=nurbs_node,
                                                direction=direction,
                                                joints_number=joints_number,
                                                joints_parent=parent_node,
                                                create_uv_pin=create_uv_pin,
                                                use_Translate=use_translate,
                                                use_rotate=use_rotate,
                                                use_scale=use_scale,
                                                use_shear=use_shear)

    def set_create_uv_pin_list_enable(self, *args):
        """
        Set the create uv pin list enable
        """
        if cmds.checkBoxGrp(self.use_translate, query=True, enable=True):
            cmds.checkBoxGrp(self.use_translate, edit=True, enable=False)
            cmds.checkBoxGrp(self.use_rotate, edit=True, enable=False)
            cmds.checkBoxGrp(self.use_scale, edit=True, enable=False)
            cmds.checkBoxGrp(self.use_shear, edit=True, enable=False)
        else:
            cmds.checkBoxGrp(self.use_translate, edit=True, enable=True)
            cmds.checkBoxGrp(self.use_rotate, edit=True, enable=True)
            cmds.checkBoxGrp(self.use_scale, edit=True, enable=True)
            cmds.checkBoxGrp(self.use_shear, edit=True, enable=True)
