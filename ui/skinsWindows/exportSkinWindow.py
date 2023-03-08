# Imports
import os

# Maya imports
from maya import cmds

# Project imports
from hiddenStrings.libs.helpers import windowHelper
from hiddenStrings.libs import skinLib


class ExportSkinWindow(windowHelper.WindowHelper):
    def __init__(self, *args):
        """
        Create the export skin window
        :param title: str, title of the window
        :param size: list, width and height
        """
        super().__init__(title='Export Skin Options', size=(450, 130))

        self.skin_index = cmds.intFieldGrp(label='Skin index: ', value1=1)
        self.all_skin_index = cmds.checkBoxGrp(label='All: ', value1=False,
                                               onCommand=self.set_skin_index_enable,
                                               offCommand=self.set_skin_index_enable)

        export_path = os.path.dirname(cmds.file(query=True, sceneName=True))
        self.export_path = cmds.textFieldGrp(label='Path: ', text=export_path)

        self.file_search = cmds.iconTextButton(style='iconOnly', image1='folder-closed.png',
                                               command=self.file_dialog_command)

        # --------------------------------------------------------------------------------------------------------------
        cmds.formLayout(self.main_layout, edit=True,
                        attachForm=[(self.skin_index, 'top', 20),
                                    (self.all_skin_index, 'top', 24)],

                        attachControl=[(self.all_skin_index, 'left', 0, self.skin_index),
                                       (self.export_path, 'top', 5, self.skin_index),
                                       (self.file_search, 'top', 5, self.skin_index),
                                       (self.file_search, 'left', 5, self.export_path)])

    def apply_command(self, *args):
        """
        Apply button command
        """
        selection_list = cmds.ls(sl=True)
        all_skin_index = cmds.checkBoxGrp(self.all_skin_index, query=True, value1=True)
        export_path = cmds.textFieldGrp(self.export_path, query=True, text=True)
        if selection_list:
            if all_skin_index:
                skinLib.export_skin_clusters(node_list=selection_list, path=export_path, skin_index=None)
            else:
                skin_index = cmds.intFieldGrp(self.skin_index, query=True, value1=True)
                skinLib.export_skin_clusters(node_list=selection_list, path=export_path, skin_index=skin_index)

    def file_dialog_command(self, *args):
        """
        Open the explorer window to set the path
        """
        folder_path = cmds.fileDialog2(dialogStyle=2, fileMode=2)
        if folder_path:
            cmds.textFieldGrp(self.export_path, edit=True, text=folder_path[0])

    def set_skin_index_enable(self, *args):
        """
        Change skin_index enable
        """
        if cmds.checkBoxGrp(self.all_skin_index, query=True, value1=True):
            cmds.intFieldGrp(self.skin_index, edit=True, enable=False)
        else:
            cmds.intFieldGrp(self.skin_index, edit=True, enable=True)
