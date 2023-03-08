# Maya imports
from maya import cmds

# Project imports
from hiddenStrings.builder.modules.body import root
from hiddenStrings.libs.helpers import windowHelper


class RootWindow(windowHelper.WindowHelper):
    def __init__(self, *args):
        """
        Create the root option window
        :param title: str, title of the window
        :param size: list, width and height
        """
        super().__init__(title='Root Guides Options', size=(450, 100))

        self.system_orientation = cmds.optionMenu(label='System Orientation')
        cmds.menuItem(self.system_orientation, label='Horizontal')
        cmds.menuItem(self.system_orientation, label='Vertical')
        cmds.optionMenu(self.system_orientation, edit=True, value='Vertical')

        # --------------------------------------------------------------------------------------------------------------
        cmds.formLayout(self.main_layout, edit=True,
                        attachForm=[(self.system_orientation, 'top', 10),
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
