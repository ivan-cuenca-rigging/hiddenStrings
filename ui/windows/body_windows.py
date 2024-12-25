# Maya imports
from maya import cmds

# Project imports
from hiddenStrings.builder.modules.body import arm, leg, neck, root, column
from hiddenStrings.libs import window_lib


class ArmWindow(window_lib.Helper):
    """
    Create the arm window

    Args:
        title (str): title of the window
        size (list): width and height
    """

    def __init__(self, *args):
        """
        Initializes an instance of ArmWindow

        Args:
            title (str): title of the window
            size (list): width and height
        """
        super(ArmWindow, self).__init__(title='Arm Guides Options', size=(450, 450))

        # Name
        self.name = cmds.textFieldGrp(label='Name: ', text='arm')

        # Side
        self.side = cmds.optionMenu(label='Side')
        cmds.menuItem(self.side, label='Left')
        cmds.menuItem(self.side, label='Center')
        cmds.menuItem(self.side, label='Right')
        cmds.optionMenu(self.side, edit=True, value='Left')

        self.connect_to_opposite = cmds.checkBoxGrp(label='Connect to opposite: ', value1=False)

        # hook and base
        self.base = cmds.textFieldGrp(label='Hook: ', text='root_c_outputs.center_c_ctr')

        self.hook = cmds.textFieldGrp(label='Base: ', text='spine_c_outputs.spineTop_c_ctr')

        # System orientation
        self.system_orientation = cmds.optionMenu(label='System Orientation')
        cmds.menuItem(self.system_orientation, label='Horizontal')
        cmds.menuItem(self.system_orientation, label='Vertical')
        cmds.optionMenu(self.system_orientation, edit=True, value='Horizontal')

        # Create Systems
        separator01 = cmds.separator(height=5)

        systems_settings_text = cmds.text(label='   System Settings',
                                          backgroundColor=(0.4, 0.4, 0.4), height=20, align='left')

        self.create_clavicle = cmds.checkBoxGrp(label='Create Clavicle: ', value1=True)

        # Finger attributes
        self.create_fingers = cmds.checkBoxGrp(label='Create Fingers: ', value1=True,
                                               onCommand=self.set_finger_list_enable,
                                               offCommand=self.set_finger_list_enable)
        self.fingers_list = cmds.textFieldGrp(label='Fingers: ', text='A3,B4,C4,D4,E4', enable=True)

        self.roll_finger_exclude_list = cmds.textFieldGrp(label='Exclude from roll: ', text='A', enable=True)

        self.create_end_middle = cmds.checkBoxGrp(label='Create End Middle: ', value1=True)

        # Joints Settings
        separator02 = cmds.separator(height=5)

        joints_settings_text = cmds.text(label='   Joints Settings',
                                         backgroundColor=(0.4, 0.4, 0.4), height=20, align='left')

        # joints number
        self.skin_start_mid_joints_number = cmds.intSliderGrp(label='Start to Mid Skin Joints number: ', field=True,
                                                              value=6, maxValue=15, columnWidth=[1, 170])

        self.skin_mid_end_joints_number = cmds.intSliderGrp(label='Mid to End Skin Joints number: ', field=True,
                                                            value=6, maxValue=15, columnWidth=[1, 170])

        # Layout
        cmds.formLayout(self.main_layout, edit=True,

                        attachForm=[(self.name, 'top', 20),
                                    (self.side, 'left', 115),
                                    (separator01, 'left', 5), (separator01, 'right', 5),
                                    (systems_settings_text, 'left', 5), (systems_settings_text, 'right', 5),
                                    (separator02, 'left', 5), (separator02, 'right', 5),
                                    (joints_settings_text, 'left', 5), (joints_settings_text, 'right', 5),
                                    (self.system_orientation, 'left', 38),
                                    (self.skin_start_mid_joints_number, 'left', 25),
                                    (self.skin_mid_end_joints_number, 'left', 25)],


                        attachControl=[(self.side, 'top', 5, self.name),
                                       (self.connect_to_opposite, 'top', 7, self.name),
                                       (self.connect_to_opposite, 'left', 4, self.side),
                                       (self.system_orientation, 'top', 5, self.side),
                                       (self.base, 'top', 5, self.system_orientation),
                                       (self.hook, 'top', 5, self.base),
                                       (separator01, 'top', 5, self.hook),
                                       (systems_settings_text, 'top', 5, separator01),
                                       (self.create_clavicle, 'top', 5, systems_settings_text),
                                       (self.create_fingers, 'top', 5, self.create_clavicle),
                                       (self.fingers_list, 'top', 5, self.create_fingers),
                                       (self.roll_finger_exclude_list, 'top', 5, self.fingers_list),
                                       (self.create_end_middle, 'top', 5, self.roll_finger_exclude_list),
                                       (separator02, 'top', 5, self.create_end_middle),
                                       (joints_settings_text, 'top', 5, separator02),
                                       (self.skin_start_mid_joints_number, 'top', 5, joints_settings_text),
                                       (self.skin_mid_end_joints_number, 'top', 5, self.skin_start_mid_joints_number)]
                        )

    def apply_command(self, *args):
        """
        Apply button command
        """
        descriptor = cmds.textFieldGrp(self.name, query=True, text=True)

        side = cmds.optionMenu(self.side, query=True, value=True)
        if side == 'Left':
            side = 'l'
        if side == 'Center':
            side = 'c'
        if side == 'Right':
            side = 'r'

        connect_to_opposite = cmds.checkBoxGrp(self.connect_to_opposite, query=True, value1=True)

        system_orientation = cmds.optionMenu(self.system_orientation, query=True, value=True)
        if system_orientation == 'Horizontal':
            system_orientation = 0
        if system_orientation == 'Vertical':
            system_orientation = 1

        base = cmds.textFieldGrp(self.base, query=True, text=True)

        hook = cmds.textFieldGrp(self.hook, query=True, text=True)

        create_clavicle = cmds.checkBoxGrp(self.create_clavicle, query=True, value1=True)

        create_fingers = cmds.checkBoxGrp(self.create_fingers, query=True, value1=True)

        fingers_list = cmds.textFieldGrp(self.fingers_list, query=True, text=True)

        roll_finger_exclude_list = cmds.textFieldGrp(self.roll_finger_exclude_list, query=True, text=True)

        create_end_middle = cmds.checkBoxGrp(self.create_end_middle, query=True, value1=True)

        skin_start_mid_joints_number = cmds.intSliderGrp(self.skin_start_mid_joints_number, query=True, value=True)

        skin_mid_end_joints_number = cmds.intSliderGrp(self.skin_mid_end_joints_number, query=True, value=True)

        arm_module = arm.Arm(descriptor=descriptor, side=side)

        arm_module.create_guides(connect_to_opposite_value=connect_to_opposite,
                                 base_default_value=base,
                                 hook_default_value=hook,
                                 system_orientation_default_value=system_orientation,
                                 create_clavicle_default_value=create_clavicle,
                                 create_fingers_default_value=create_fingers,
                                 fingers_list_default_value=fingers_list,
                                 roll_fingers_exclude_list_value=roll_finger_exclude_list,
                                 create_end_middle_default_value=create_end_middle,
                                 skin_start_mid_joints_number_default_value=skin_start_mid_joints_number,
                                 skin_mid_end_joints_number_default_value=skin_mid_end_joints_number)

    def set_finger_list_enable(self, *args):
        """
        Set the finger list textField enable
        """
        if cmds.textFieldGrp(self.fingers_list, query=True, enable=True):
            cmds.textFieldGrp(self.fingers_list, edit=True, enable=False)
            cmds.textFieldGrp(self.roll_finger_exclude_list, edit=True, enable=False)
        else:
            cmds.textFieldGrp(self.fingers_list, edit=True, enable=True)
            cmds.textFieldGrp(self.roll_finger_exclude_list, edit=True, enable=True)


class LegWindow(window_lib.Helper):
    """
    Create the leg window

    Args:
        title (str): title of the window
        size (list): width and height
    """

    def __init__(self, *args):
        """
        Initializes an instance of LegWindow

        Args:
            title (str): title of the window
            size (list): width and height
        """
        super(LegWindow, self).__init__(title='Leg Guides Options', size=(450, 450))

        # Name
        self.name = cmds.textFieldGrp(label='Name: ', text='leg')

        # Side
        self.side = cmds.optionMenu(label='Side')
        cmds.menuItem(self.side, label='Left')
        cmds.menuItem(self.side, label='Center')
        cmds.menuItem(self.side, label='Right')
        cmds.optionMenu(self.side, edit=True, value='Left')

        self.connect_to_opposite = cmds.checkBoxGrp(label='Connect to opposite: ', value1=False)

        # hook and base
        self.base = cmds.textFieldGrp(label='Hook: ', text='root_c_outputs.center_c_ctr')

        self.hook = cmds.textFieldGrp(label='Base: ', text='spine_c_outputs.spineBottom_c_ctr')

        # System orientation
        self.system_orientation = cmds.optionMenu(label='System Orientation')
        cmds.menuItem(self.system_orientation, label='Horizontal')
        cmds.menuItem(self.system_orientation, label='Vertical')
        cmds.optionMenu(self.system_orientation, edit=True, value='Vertical')

        # Create Systems
        separator01 = cmds.separator(height=5)

        systems_settings_text = cmds.text(label='   System Settings',
                                          backgroundColor=(0.4, 0.4, 0.4), height=20, align='left')

        self.create_clavicle = cmds.checkBoxGrp(label='Create Clavicle: ', value1=False)

        # Finger attributes
        self.create_fingers = cmds.checkBoxGrp(label='Create Fingers: ', value1=False,
                                               onCommand=self.set_finger_list_enable,
                                               offCommand=self.set_finger_list_enable)
        self.fingers_list = cmds.textFieldGrp(label='Fingers: ', text='A3,B4,C4,D4,E4', enable=False)

        self.roll_finger_exclude_list = cmds.textFieldGrp(label='Exclude from roll: ', text='A', enable=False)

        self.create_end_middle = cmds.checkBoxGrp(label='Create End Middle: ', value1=True)

        # Joints Settings
        separator02 = cmds.separator(height=5)

        joints_settings_text = cmds.text(label='   Joints Settings',
                                         backgroundColor=(0.4, 0.4, 0.4), height=20, align='left')

        # joints number
        self.skin_start_mid_joints_number = cmds.intSliderGrp(label='Start to Mid Skin Joints number: ', field=True,
                                                              value=6, maxValue=15, columnWidth=[1, 170])

        self.skin_mid_end_joints_number = cmds.intSliderGrp(label='Mid to End Skin Joints number: ', field=True,
                                                            value=6, maxValue=15, columnWidth=[1, 170])

        # Layout
        cmds.formLayout(self.main_layout, edit=True,

                        attachForm=[(self.name, 'top', 20),
                                    (self.side, 'left', 115),
                                    (separator01, 'left', 5), (separator01, 'right', 5),
                                    (systems_settings_text, 'left', 5), (systems_settings_text, 'right', 5),
                                    (separator02, 'left', 5), (separator02, 'right', 5),
                                    (joints_settings_text, 'left', 5), (joints_settings_text, 'right', 5),
                                    (self.system_orientation, 'left', 38),
                                    (self.skin_start_mid_joints_number, 'left', 25),
                                    (self.skin_mid_end_joints_number, 'left', 25)],


                        attachControl=[(self.side, 'top', 5, self.name),
                                       (self.connect_to_opposite, 'top', 7, self.name),
                                       (self.connect_to_opposite, 'left', 4, self.side),
                                       (self.system_orientation, 'top', 5, self.side),
                                       (self.base, 'top', 5, self.system_orientation),
                                       (self.hook, 'top', 5, self.base),
                                       (separator01, 'top', 5, self.hook),
                                       (systems_settings_text, 'top', 5, separator01),
                                       (self.create_clavicle, 'top', 5, systems_settings_text),
                                       (self.create_fingers, 'top', 5, self.create_clavicle),
                                       (self.fingers_list, 'top', 5, self.create_fingers),
                                       (self.roll_finger_exclude_list, 'top', 5, self.fingers_list),
                                       (self.create_end_middle, 'top', 5, self.roll_finger_exclude_list),
                                       (separator02, 'top', 5, self.create_end_middle),
                                       (joints_settings_text, 'top', 5, separator02),
                                       (self.skin_start_mid_joints_number, 'top', 5, joints_settings_text),
                                       (self.skin_mid_end_joints_number, 'top', 5, self.skin_start_mid_joints_number)]
                        )

    def apply_command(self, *args):
        """
        Apply button command
        """
        descriptor = cmds.textFieldGrp(self.name, query=True, text=True)

        side = cmds.optionMenu(self.side, query=True, value=True)
        if side == 'Left':
            side = 'l'
        if side == 'Center':
            side = 'c'
        if side == 'Right':
            side = 'r'

        connect_to_opposite = cmds.checkBoxGrp(self.connect_to_opposite, query=True, value1=True)

        system_orientation = cmds.optionMenu(self.system_orientation, query=True, value=True)
        if system_orientation == 'Horizontal':
            system_orientation = 0
        if system_orientation == 'Vertical':
            system_orientation = 1

        base = cmds.textFieldGrp(self.base, query=True, text=True)

        hook = cmds.textFieldGrp(self.hook, query=True, text=True)

        create_clavicle = cmds.checkBoxGrp(self.create_clavicle, query=True, value1=True)

        create_fingers = cmds.checkBoxGrp(self.create_fingers, query=True, value1=True)

        fingers_list = cmds.textFieldGrp(self.fingers_list, query=True, text=True)

        roll_finger_exclude_list = cmds.textFieldGrp(self.roll_finger_exclude_list, query=True, text=True)

        create_end_middle = cmds.checkBoxGrp(self.create_end_middle, query=True, value1=True)

        skin_start_mid_joints_number = cmds.intSliderGrp(self.skin_start_mid_joints_number, query=True, value=True)

        skin_mid_end_joints_number = cmds.intSliderGrp(self.skin_mid_end_joints_number, query=True, value=True)

        leg_module = leg.Leg(descriptor=descriptor, side=side)

        leg_module.create_guides(connect_to_opposite_value=connect_to_opposite,
                                 base_default_value=base,
                                 hook_default_value=hook,
                                 system_orientation_default_value=system_orientation,
                                 create_clavicle_default_value=create_clavicle,
                                 create_fingers_default_value=create_fingers,
                                 fingers_list_default_value=fingers_list,
                                 roll_fingers_exclude_list_value=roll_finger_exclude_list,
                                 create_end_middle_default_value=create_end_middle,
                                 skin_start_mid_joints_number_default_value=skin_start_mid_joints_number,
                                 skin_mid_end_joints_number_default_value=skin_mid_end_joints_number)

    def set_finger_list_enable(self, *args):
        """
        Set the finger list textField enable
        """
        if cmds.textFieldGrp(self.fingers_list, query=True, enable=True):
            cmds.textFieldGrp(self.fingers_list, edit=True, enable=False)
            cmds.textFieldGrp(self.roll_finger_exclude_list, edit=True, enable=False)
        else:
            cmds.textFieldGrp(self.fingers_list, edit=True, enable=True)
            cmds.textFieldGrp(self.roll_finger_exclude_list, edit=True, enable=True)


class NeckWindow(window_lib.Helper):
    """
    Create the neck window

    Args:
        title (str): title of the window
        size (list): width and height
    """

    def __init__(self, *args):
        """
        Initializes an instance of NeckWindow

        Args:
            title (str): title of the window
            size (list): width and height
        """
        super(NeckWindow, self).__init__(title='Neck Guides Options', size=(450, 450))

        # Name
        self.name = cmds.textFieldGrp(label='Name: ', text='neck')

        # Side
        self.side = cmds.optionMenu(label='Side')
        cmds.menuItem(self.side, label='Left')
        cmds.menuItem(self.side, label='Center')
        cmds.menuItem(self.side, label='Right')
        cmds.optionMenu(self.side, edit=True, value='Center')

        self.base = cmds.textFieldGrp(label='Hook: ', text='root_c_outputs.center_c_ctr')

        self.hook = cmds.textFieldGrp(label='Base: ', text='spine_c_outputs.spineTop_c_ctr')

        # Joints Settings
        separator01 = cmds.separator(height=5)

        joints_settings_text = cmds.text(label='   Joints Settings',
                                         backgroundColor=(0.4, 0.4, 0.4), height=20, align='left')
        # Skin joints number
        self.skin_joints_number = cmds.intSliderGrp(label='Skin Joints number: ', field=True, value=10, maxValue=30)

        # Fk Settings
        separator02 = cmds.separator(height=5)

        fk_settings_text = cmds.text(label='   Fk Settings',
                                     backgroundColor=(0.4, 0.4, 0.4), height=20, align='left')

        # Fk controls number
        self.fk_controls_number = cmds.intSliderGrp(label='Fk controls number: ', field=True,
                                                    value=3, minValue=2, maxValue=5)

        # Create Fk system
        self.create_fk_system = cmds.checkBoxGrp(label='Create Fk: ', value1=False)

        # Create Fk inv system
        self.create_fk_inv_system = cmds.checkBoxGrp(label='Create Fk inverse: ', value1=False)

        # Ik Settings
        separator03 = cmds.separator(height=5)

        ik_settings_text = cmds.text(label='   Ik Settings',
                                     backgroundColor=(0.4, 0.4, 0.4), height=20, align='left')

        # Create Ik middle
        self.create_ik_middle_system = cmds.checkBoxGrp(label='Create Ik middle: ', value1=True)

        # Start Ik world rotation
        self.start_ik_world_rotation = cmds.optionMenu(label='Start Ik orientation')
        cmds.menuItem(self.start_ik_world_rotation, label='System')
        cmds.menuItem(self.start_ik_world_rotation, label='World')
        cmds.optionMenu(self.start_ik_world_rotation, edit=True, value='World')

        # End Ik world rotation
        self.end_ik_world_rotation = cmds.optionMenu(label='End Ik orientation')
        cmds.menuItem(self.end_ik_world_rotation, label='System')
        cmds.menuItem(self.end_ik_world_rotation, label='World')
        cmds.optionMenu(self.end_ik_world_rotation, edit=True, value='World')

        # Layout
        cmds.formLayout(self.main_layout, edit=True,

                        attachForm=[(self.name, 'top', 20),
                                    (separator01, 'left', 5), (separator01, 'right', 5),
                                    (joints_settings_text, 'left', 5), (joints_settings_text, 'right', 5),
                                    (self.side, 'left', 115),
                                    (separator02, 'left', 5), (separator02, 'right', 5),
                                    (fk_settings_text, 'left', 5), (fk_settings_text, 'right', 5),
                                    (separator03, 'left', 5), (separator03, 'right', 5),
                                    (ik_settings_text, 'left', 5), (ik_settings_text, 'right', 5),
                                    (self.start_ik_world_rotation, 'left', 39),
                                    (self.end_ik_world_rotation, 'left', 43)],

                        attachControl=[(self.side, 'top', 5, self.name),
                                       (self.base, 'top', 5, self.side),
                                       (self.hook, 'top', 5, self.base),
                                       (separator01, 'top', 5, self.hook),
                                       (joints_settings_text, 'top', 5, separator01),
                                       (self.skin_joints_number, 'top', 5, joints_settings_text),
                                       (separator02, 'top', 5, self.skin_joints_number),
                                       (fk_settings_text, 'top', 5, separator02),
                                       (self.fk_controls_number, 'top', 5, fk_settings_text),
                                       (self.create_fk_system, 'top', 10, self.fk_controls_number),
                                       (self.create_fk_inv_system, 'top', 10, self.create_fk_system),
                                       (separator03, 'top', 5, self.create_fk_inv_system),
                                       (ik_settings_text, 'top', 5, separator03),
                                       (self.create_ik_middle_system, 'top', 5, ik_settings_text),
                                       (self.start_ik_world_rotation, 'top', 5, self.create_ik_middle_system),
                                       (self.end_ik_world_rotation, 'top', 5, self.start_ik_world_rotation)]
                        )

    def apply_command(self, *args):
        """
        Apply button command
        """
        descriptor = cmds.textFieldGrp(self.name, query=True, text=True)

        side = cmds.optionMenu(self.side, query=True, value=True)
        if side == 'Left':
            side = 'l'
        if side == 'Center':
            side = 'c'
        if side == 'Right':
            side = 'r'

        base = cmds.textFieldGrp(self.base, query=True, text=True)

        hook = cmds.textFieldGrp(self.hook, query=True, text=True)

        skin_joints_number = cmds.intSliderGrp(self.skin_joints_number, query=True, value=True)

        fk_controls_number = cmds.intSliderGrp(self.fk_controls_number, query=True, value=True)

        create_fk_system = cmds.checkBoxGrp(self.create_fk_system, query=True, value1=True)

        create_fk_inv_system = cmds.checkBoxGrp(self.create_fk_inv_system, query=True, value1=True)

        create_ik_middle_system = cmds.checkBoxGrp(self.create_ik_middle_system, query=True, value1=True)

        start_ik_world_rotation = cmds.optionMenu(self.start_ik_world_rotation, query=True, value=True)
        if start_ik_world_rotation == 'System':
            start_ik_world_rotation = False
        if start_ik_world_rotation == 'World':
            start_ik_world_rotation = True

        end_ik_world_rotation = cmds.optionMenu(self.end_ik_world_rotation, query=True, value=True)
        if end_ik_world_rotation == 'System':
            end_ik_world_rotation = False
        if end_ik_world_rotation == 'World':
            end_ik_world_rotation = True

        neck_module = neck.Neck(descriptor=descriptor, side=side)

        neck_module.create_guides(base_default_value=base,
                                  hook_default_value=hook,
                                  skin_joints_number_default_value=skin_joints_number,
                                  fk_controls_number_default_value=fk_controls_number,
                                  create_fk_system_default_value=create_fk_system,
                                  create_fk_inverse_default_value=create_fk_inv_system,
                                  create_ik_middle_default_value=create_ik_middle_system,
                                  start_ik_world_rotation_default_value=start_ik_world_rotation,
                                  end_ik_world_rotation_default_value=end_ik_world_rotation)


class RootWindow(window_lib.Helper):
    """
    Create the root window

    Args:
        title (str): title of the window
        size (list): width and height
    """

    def __init__(self, *args):
        """
        Initializes an instance of RootWindow

        Args:
            title (str): title of the window
            size (list): width and height
        """
        super(RootWindow, self).__init__(title='Root Guides Options', size=(450, 100))

        self.system_orientation = cmds.optionMenu(label='System Orientation')
        cmds.menuItem(self.system_orientation, label='Horizontal')
        cmds.menuItem(self.system_orientation, label='Vertical')
        cmds.optionMenu(self.system_orientation, edit=True, value='Vertical')

        # --------------------------------------------------------------------------------------------------------------
        cmds.formLayout(self.main_layout, edit=True,
                        attachForm=[(self.system_orientation, 'top', 20),
                                    (self.system_orientation, 'left', 25)])

    def apply_command(self, *args):
        """
        Apply button command
        """
        system_orientation = cmds.optionMenu(self.system_orientation, query=True, value=True)
        if system_orientation == 'Horizontal':
            system_orientation = 0
        if system_orientation == 'Vertical':
            system_orientation = 1

        root_module = root.Root()
        root_module.create_guides(system_orientation_default_value=system_orientation)


class SpineWindow(window_lib.Helper):
    """
    Create the spine window
    
    Args:
        title (str): title of the window
        size (list): width and height
    """

    def __init__(self, *args):
        """
        Initializes an instance of SpineWindow

        Args:
            title (str): title of the window
            size (list): width and height
        """
        super(SpineWindow, self).__init__(title='Spine Guides Options', size=(450, 450))

        # Name
        self.name = cmds.textFieldGrp(label='Name: ', text='spine')

        # Side
        self.side = cmds.optionMenu(label='Side')
        cmds.menuItem(self.side, label='Left')
        cmds.menuItem(self.side, label='Center')
        cmds.menuItem(self.side, label='Right')
        cmds.optionMenu(self.side, edit=True, value='Center')

        # hook and base
        self.base = cmds.textFieldGrp(label='Hook: ', text='root_c_outputs.center_c_ctr')

        self.hook = cmds.textFieldGrp(label='Base: ', text='root_c_outputs.root_c_ctr')

        # Joints Settings
        separator01 = cmds.separator(height=5)

        joints_settings_text = cmds.text(label='   Joints Settings',
                                         backgroundColor=(0.4, 0.4, 0.4), height=20, align='left')
        # Skin joints number
        self.skin_joints_number = cmds.intSliderGrp(label='Skin Joints number: ', field=True, value=10, maxValue=30)

        # Fk Settings
        separator02 = cmds.separator(height=5)

        fk_settings_text = cmds.text(label='   Fk Settings',
                                     backgroundColor=(0.4, 0.4, 0.4), height=20, align='left')

        # Fk controls number
        self.fk_controls_number = cmds.intSliderGrp(label='Fk controls number: ', field=True,
                                                    value=3, minValue=2, maxValue=5)

        # Create Fk system
        self.create_fk_system = cmds.checkBoxGrp(label='Create Fk: ', value1=True)

        # Create Fk inv system
        self.create_fk_inv_system = cmds.checkBoxGrp(label='Create Fk inverse: ', value1=True)

        # Ik Settings
        separator03 = cmds.separator(height=5)

        ik_settings_text = cmds.text(label='   Ik Settings',
                                     backgroundColor=(0.4, 0.4, 0.4), height=20, align='left')

        # Create Ik middle
        self.create_ik_middle_system = cmds.checkBoxGrp(label='Create Ik middle: ', value1=True)

        # Start Ik world rotation
        self.start_ik_world_rotation = cmds.optionMenu(label='Start Ik orientation')
        cmds.menuItem(self.start_ik_world_rotation, label='System')
        cmds.menuItem(self.start_ik_world_rotation, label='World')
        cmds.optionMenu(self.start_ik_world_rotation, edit=True, value='System')

        # End Ik world rotation
        self.end_ik_world_rotation = cmds.optionMenu(label='End Ik orientation')
        cmds.menuItem(self.end_ik_world_rotation, label='System')
        cmds.menuItem(self.end_ik_world_rotation, label='World')
        cmds.optionMenu(self.end_ik_world_rotation, edit=True, value='System')

        # --------------------------------------------------------------------------------------------------------------
        cmds.formLayout(self.main_layout, edit=True,

                        attachForm=[(self.name, 'top', 20),
                                    (separator01, 'left', 5), (separator01, 'right', 5),
                                    (joints_settings_text, 'left', 5), (joints_settings_text, 'right', 5),
                                    (self.side, 'left', 115),
                                    (separator02, 'left', 5), (separator02, 'right', 5),
                                    (fk_settings_text, 'left', 5), (fk_settings_text, 'right', 5),
                                    (separator03, 'left', 5), (separator03, 'right', 5),
                                    (ik_settings_text, 'left', 5), (ik_settings_text, 'right', 5),
                                    (self.start_ik_world_rotation, 'left', 39),
                                    (self.end_ik_world_rotation, 'left', 43)],

                        attachControl=[(self.side, 'top', 5, self.name),
                                       (self.base, 'top', 5, self.side),
                                       (self.hook, 'top', 5, self.base),
                                       (separator01, 'top', 5, self.hook),
                                       (joints_settings_text, 'top', 5, separator01),
                                       (self.skin_joints_number, 'top', 5, joints_settings_text),
                                       (separator02, 'top', 5, self.skin_joints_number),
                                       (fk_settings_text, 'top', 5, separator02),
                                       (self.fk_controls_number, 'top', 5, fk_settings_text),
                                       (self.create_fk_system, 'top', 10, self.fk_controls_number),
                                       (self.create_fk_inv_system, 'top', 10, self.create_fk_system),
                                       (separator03, 'top', 5, self.create_fk_inv_system),
                                       (ik_settings_text, 'top', 5, separator03),
                                       (self.create_ik_middle_system, 'top', 5, ik_settings_text),
                                       (self.start_ik_world_rotation, 'top', 5, self.create_ik_middle_system),
                                       (self.end_ik_world_rotation, 'top', 5, self.start_ik_world_rotation)]
                        )

    def apply_command(self, *args):
        """
        Apply button command
        """
        descriptor = cmds.textFieldGrp(self.name, query=True, text=True)

        side = cmds.optionMenu(self.side, query=True, value=True)
        if side == 'Left':
            side = 'l'
        if side == 'Center':
            side = 'c'
        if side == 'Right':
            side = 'r'

        base = cmds.textFieldGrp(self.base, query=True, text=True)

        hook = cmds.textFieldGrp(self.hook, query=True, text=True)

        skin_joints_number = cmds.intSliderGrp(self.skin_joints_number, query=True, value=True)

        fk_controls_number = cmds.intSliderGrp(self.fk_controls_number, query=True, value=True)

        create_fk_system = cmds.checkBoxGrp(self.create_fk_system, query=True, value1=True)

        create_fk_inv_system = cmds.checkBoxGrp(self.create_fk_inv_system, query=True, value1=True)

        create_ik_middle_system = cmds.checkBoxGrp(self.create_ik_middle_system, query=True, value1=True)

        start_ik_world_rotation = cmds.optionMenu(self.start_ik_world_rotation, query=True, value=True)
        if start_ik_world_rotation == 'System':
            start_ik_world_rotation = False
        if start_ik_world_rotation == 'World':
            start_ik_world_rotation = True

        end_ik_world_rotation = cmds.optionMenu(self.end_ik_world_rotation, query=True, value=True)
        if end_ik_world_rotation == 'System':
            end_ik_world_rotation = False
        if end_ik_world_rotation == 'World':
            end_ik_world_rotation = True

        spine_module = column.Column(descriptor=descriptor, side=side)

        spine_module.create_guides(base_default_value=base,
                                   hook_default_value=hook,
                                   skin_joints_number_default_value=skin_joints_number,
                                   fk_controls_number_default_value=fk_controls_number,
                                   create_fk_system_default_value=create_fk_system,
                                   create_fk_inverse_default_value=create_fk_inv_system,
                                   create_ik_middle_default_value=create_ik_middle_system,
                                   start_ik_world_rotation_default_value=start_ik_world_rotation,
                                   end_ik_world_rotation_default_value=end_ik_world_rotation)
