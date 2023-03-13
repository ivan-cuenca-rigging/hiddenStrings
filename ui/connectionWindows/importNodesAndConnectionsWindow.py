# Imports
import os

# Maya imports
from maya import cmds

# Project imports
from hiddenStrings.libs.helpers import windowHelper
from hiddenStrings.libs import importExportLib


class ImportNodesAndConnectionsWindow(windowHelper.WindowHelper):
    def __init__(self, *args):
        """
        Create the import nodes and connections window
        :param title: str, title of the window
        :param size: list, width and height
        """
        super().__init__(title='Import nodes and connections Options', size=(450, 130))

        self.import_nodes = cmds.checkBoxGrp(label='Import nodes: ', value1=True)
        self.import_connections = cmds.checkBoxGrp(label='Import connections: ', value1=True)

        import_path = os.path.dirname(cmds.file(query=True, sceneName=True))
        self.import_path = cmds.textFieldGrp(label='Path: ', text=import_path)

        self.file_search = cmds.iconTextButton(style='iconOnly', image1='folder-closed.png',
                                               command=self.file_dialog_command)

        # --------------------------------------------------------------------------------------------------------------
        cmds.formLayout(self.main_layout, edit=True,
                        attachForm=[(self.import_nodes, 'top', 15),
                                    (self.import_nodes, 'left', 40),
                                    (self.import_connections, 'top', 15),
                                    (self.import_path, 'left', -25)],

                        attachControl=[(self.import_connections, 'left', 0, self.import_nodes),
                                       (self.import_path, 'top', 20, self.import_nodes),
                                       (self.file_search, 'top', 20, self.import_nodes),
                                       (self.file_search, 'left', 5, self.import_path)])

    def apply_command(self, *args):
        """
        Apply button command
        """
        import_nodes = cmds.checkBoxGrp(self.import_nodes, query=True, value1=True)
        import_connections = cmds.checkBoxGrp(self.import_connections, query=True, value1=True)

        import_path = cmds.textFieldGrp(self.import_path, query=True, text=True)

        importExportLib.import_nodes_and_connections(path=import_path,
                                                     import_nodes=import_nodes,
                                                     import_connections=import_connections)

    def file_dialog_command(self, *args):
        """
        Open the explorer window to set the path
        """
        folder_path = cmds.fileDialog2(dialogStyle=2, fileMode=1, fileFilter='*.ma')
        if folder_path:
            cmds.textFieldGrp(self.import_path, edit=True, text=folder_path[0])
