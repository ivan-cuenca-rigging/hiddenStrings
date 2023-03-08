# Maya imports
from maya import cmds

# Project imports
from hiddenStrings.libs.helpers import windowHelper
from hiddenStrings.libs import skinLib


class TransferSkinWindow(windowHelper.WindowHelper):
    def __init__(self, *args):
        """
        Create the import skin window
        :param title: str, title of the window
        :param size: list, width and height
        """
        super().__init__(title='Import Skin Options', size=(450, 150))

        self.source_skin_index = cmds.intFieldGrp(label='Source skin index: ', value1=1)
        self.target_skin_index = cmds.intFieldGrp(label='Target skin index: ', value1=1)

        self.transfer_method = cmds.optionMenu(label='Surface association')
        cmds.menuItem(self.transfer_method, label='Closest point')
        cmds.menuItem(self.transfer_method, label='Closest component')

        # --------------------------------------------------------------------------------------------------------------
        cmds.formLayout(self.main_layout, edit=True,
                        attachForm=[(self.source_skin_index, 'top', 20),
                                    (self.source_skin_index, 'left', 20),
                                    (self.target_skin_index, 'left', 20),
                                    (self.transfer_method, 'left', 59)],

                        attachControl=[(self.target_skin_index, 'top', 5, self.source_skin_index),
                                       (self.transfer_method, 'top', 5, self.target_skin_index)])

    def apply_command(self, *args):
        """
        Apply button command
        """
        if len(cmds.ls(selection=True)) != 2:
            cmds.error('Select two nodes')

        source_skin_index = cmds.intFieldGrp(self.source_skin_index, query=True, value1=True)

        target_skin_index = cmds.intFieldGrp(self.target_skin_index, query=True, value1=True)

        transfer_method = cmds.optionMenu(self.transfer_method, query=True, value=True)
        if transfer_method == 'Closest point':
            transfer_method = 'closestPoint'
        if transfer_method == 'Closest component':
            transfer_method = 'closestComponent'

        skinLib.transfer_skin(source=cmds.ls(selection=True)[0],
                              target=cmds.ls(selection=True)[-1],
                              source_skin_index=source_skin_index,
                              target_skin_index=target_skin_index,
                              surface_association=transfer_method)
