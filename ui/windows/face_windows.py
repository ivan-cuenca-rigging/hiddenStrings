# Maya imports
from maya import cmds

# Project imports
from hiddenStrings.builder.modules.face import ear
from hiddenStrings.libs import window_lib


class EarWindow(window_lib.Helper):
    def __init__(self, *args):
        """
        Create the ear option window
        :param title: str, title of the window
        :param size: list, width and height
        """
        super(EarWindow, self).__init__(title='Ear Guide Options', size=(450, 175))

        # Name
        self.name = cmds.textFieldGrp(label='Name: ', text='ear')

        # Side
        self.side = cmds.optionMenu(label='Side')
        cmds.menuItem(self.side, label='Left')
        cmds.menuItem(self.side, label='Center')
        cmds.menuItem(self.side, label='Right')
        cmds.optionMenu(self.side, edit=True, value='Left')

        self.connect_to_opposite = cmds.checkBoxGrp(label='Connect to opposite: ', value1=False)

        # hook and base
        self.base = cmds.textFieldGrp(label='Hook: ', text='rootOutputs_c_grp.center_c_ctr')

        self.hook = cmds.textFieldGrp(label='Base: ', text='neckOutputs_c_grp.head_c_ctr')

        # --------------------------------------------------------------------------------------------------------------
        cmds.formLayout(self.main_layout, edit=True,

                        attachForm=[(self.name, 'top', 5),
                                    (self.side, 'left', 115)],

                        attachControl=[(self.side, 'top', 5, self.name),
                                       (self.connect_to_opposite, 'top', 5, self.side),
                                       (self.base, 'top', 5, self.connect_to_opposite),
                                       (self.hook, 'top', 5, self.base)]
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

        base = cmds.textFieldGrp(self.base, query=True, text=True)

        hook = cmds.textFieldGrp(self.hook, query=True, text=True)

        ear_module = ear.Ear(descriptor=descriptor, side=side)

        ear_module.create_guides(connect_to_opposite_value=connect_to_opposite,
                                 base_default_value=base,
                                 hook_default_value=hook)


class CheekWindow(window_lib.Helper):
    def __init__(self, *args):
        """
        Create the ear option window
        :param title: str, title of the window
        :param size: list, width and height
        """
        super(CheekWindow, self).__init__(title='Cheek Guide Options', size=(450, 175))

        # Name
        self.name = cmds.textFieldGrp(label='Name: ', text='cheek')

        # Side
        self.side = cmds.optionMenu(label='Side')
        cmds.menuItem(self.side, label='Left')
        cmds.menuItem(self.side, label='Center')
        cmds.menuItem(self.side, label='Right')
        cmds.optionMenu(self.side, edit=True, value='Left')

        self.connect_to_opposite = cmds.checkBoxGrp(label='Connect to opposite: ', value1=False)

        # hook and base
        self.base = cmds.textFieldGrp(label='Hook: ', text='rootOutputs_c_grp.center_c_ctr')

        self.hook = cmds.textFieldGrp(label='Base: ', text='neckOutputs_c_grp.head_c_ctr')

        # --------------------------------------------------------------------------------------------------------------
        cmds.formLayout(self.main_layout, edit=True,

                        attachForm=[(self.name, 'top', 5),
                                    (self.side, 'left', 115)],

                        attachControl=[(self.side, 'top', 5, self.name),
                                       (self.connect_to_opposite, 'top', 5, self.side),
                                       (self.base, 'top', 5, self.connect_to_opposite),
                                       (self.hook, 'top', 5, self.base)]
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

        base = cmds.textFieldGrp(self.base, query=True, text=True)

        hook = cmds.textFieldGrp(self.hook, query=True, text=True)

        ear_module = ear.Ear(descriptor=descriptor, side=side)

        ear_module.create_guides(connect_to_opposite_value=connect_to_opposite,
                                 base_default_value=base,
                                 hook_default_value=hook)

