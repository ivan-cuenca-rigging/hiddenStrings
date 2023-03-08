# Imports
import os

# Maya imports
from maya import cmds

# Project imports
from hiddenStrings.libs.helpers import windowHelper
from hiddenStrings.libs import blendShapeLib


class ExportBlendShapeWindow(windowHelper.WindowHelper):
    def __init__(self, *args):
        """
        Create the export blendShape window
        :param title: str, title of the window
        :param size: list, width and height
        """
        super().__init__(title='Export blendShape Options', size=(450, 130))

        export_path = os.path.dirname(cmds.file(query=True, sceneName=True))
        self.export_path = cmds.textFieldGrp(label='Path: ', text=export_path)

        self.file_search = cmds.iconTextButton(style='iconOnly', image1='folder-closed.png',
                                               command=self.file_dialog_command)

        # --------------------------------------------------------------------------------------------------------------
        cmds.formLayout(self.main_layout, edit=True,
                        attachForm=[(self.export_path, 'top', 35),
                                    (self.file_search, 'top', 35)],

                        attachControl=[(self.file_search, 'left', 5, self.export_path)])

    def apply_command(self, *args):
        """
        Apply button command
        """
        if len(cmds.ls(selection=True)) == 0:
            cmds.error('Nothing selected')

        export_path = cmds.textFieldGrp(self.export_path, query=True, text=True)

        blendShapeLib.export_blend_shapes(node_list=cmds.ls(selection=True), path=export_path)

    def file_dialog_command(self, *args):
        """
        Open the explorer window to set the path
        """
        folder_path = cmds.fileDialog2(dialogStyle=2, fileMode=2)
        if folder_path:
            cmds.textFieldGrp(self.export_path, edit=True, text=folder_path[0])
