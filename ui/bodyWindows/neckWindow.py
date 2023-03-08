# Maya imports
from maya import cmds

# Project imports
from hiddenStrings.builder.modules.body import neck
from hiddenStrings.libs.helpers import windowHelper


class NeckWindow(windowHelper.WindowHelper):
    def __init__(self, *args):
        """
        Create the neck option window
        :param title: str, title of the window
        :param size: list, width and height
        """
        super().__init__(title='Neck Guides Options', size=(450, 450))

        # Name
        self.name = cmds.textFieldGrp(label='Name: ', text='neck')

        # Side
        self.side = cmds.optionMenu(label='Side')
        cmds.menuItem(self.side, label='Left')
        cmds.menuItem(self.side, label='Center')
        cmds.menuItem(self.side, label='Right')
        cmds.optionMenu(self.side, edit=True, value='Center')

        self.base = cmds.textFieldGrp(label='Hook: ', text='rootOutputs_c_grp.center_c_ctr')

        self.hook = cmds.textFieldGrp(label='Base: ', text='spineOutputs_c_grp.spineTop_c_ctr')

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

        # End Ik world rotation
        self.end_ik_world_rotation = cmds.optionMenu(label='End Ik orientation')
        cmds.menuItem(self.end_ik_world_rotation, label='System')
        cmds.menuItem(self.end_ik_world_rotation, label='World')
        cmds.optionMenu(self.end_ik_world_rotation, edit=True, value='World')

        # Layout
        cmds.formLayout(self.main_layout, edit=True,

                        attachForm=[(self.name, 'top', 5),
                                    (separator01, 'left', 5), (separator01, 'right', 5),
                                    (joints_settings_text, 'left', 5), (joints_settings_text, 'right', 5),
                                    (self.side, 'left', 115),
                                    (separator02, 'left', 5), (separator02, 'right', 5),
                                    (fk_settings_text, 'left', 5), (fk_settings_text, 'right', 5),
                                    (separator03, 'left', 5), (separator03, 'right', 5),
                                    (ik_settings_text, 'left', 5), (ik_settings_text, 'right', 5),
                                    (self.end_ik_world_rotation, 'left', 43),
                                    (self.end_ik_world_rotation, 'bottom', 5)],

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
                                       (self.end_ik_world_rotation, 'top', 5, self.create_ik_middle_system)],

                        attachPosition=[(self.name, 'top', 0, 5),
                                        (self.end_ik_world_rotation, 'bottom', 0, 5)]
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
                                  end_ik_world_rotation_default_value=end_ik_world_rotation)
