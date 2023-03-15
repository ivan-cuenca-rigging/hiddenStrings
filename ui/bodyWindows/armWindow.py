# Maya imports
from maya import cmds

# Project imports
from hiddenStrings.builder.modules.body import arm
from hiddenStrings.libs.helpers import windowHelper


class ArmWindow(windowHelper.WindowHelper):
    def __init__(self, *args):
        """
        Create the arm option window
        :param title: str, title of the window
        :param size: list, width and height
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
        self.base = cmds.textFieldGrp(label='Hook: ', text='rootOutputs_c_grp.center_c_ctr')

        self.hook = cmds.textFieldGrp(label='Base: ', text='spineOutputs_c_grp.spineTop_c_ctr')

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
                                                            value=6, maxValue=15,  columnWidth=[1, 170])

        # Layout
        cmds.formLayout(self.main_layout, edit=True,

                        attachForm=[(self.name, 'top', 5),
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
                                       (self.skin_mid_end_joints_number, 'top', 5, self.skin_start_mid_joints_number)],

                        attachPosition=[(self.name, 'top', 0, 5)]
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
        if cmds.textFieldGrp(self.fingers_list, query=True, enable=True):
            cmds.textFieldGrp(self.fingers_list, edit=True, enable=False)
            cmds.textFieldGrp(self.roll_finger_exclude_list, edit=True, enable=False)
        else:
            cmds.textFieldGrp(self.fingers_list, edit=True, enable=True)
            cmds.textFieldGrp(self.roll_finger_exclude_list, edit=True, enable=True)
