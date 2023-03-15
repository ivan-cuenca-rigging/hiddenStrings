# Imports
import os

# Maya imports
from maya import cmds

# Project imports
from hiddenStrings.libs.helpers import windowHelper
from hiddenStrings.libs import importExportLib


class ExportNodesAndConnectionsWindow(windowHelper.WindowHelper):
    def __init__(self, *args):
        """
        Create the export nodes and connections window
        :param title: str, title of the window
        :param size: list, width and height
        """
        super(ExportNodesAndConnectionsWindow, self).__init__(title='Export nodes and connections Options',
                                                              size=(450, 130))

        self.export_nodes = cmds.checkBoxGrp(label='Export nodes: ', value1=True)
        self.export_edges = cmds.checkBoxGrp(label='Export edges: ', value1=False)
        self.export_connections = cmds.checkBoxGrp(label='Export connections: ', value1=True)

        export_path = os.path.dirname(cmds.file(query=True, sceneName=True))
        self.export_path = cmds.textFieldGrp(label='Path: ', text=export_path)

        self.file_search = cmds.iconTextButton(style='iconOnly', image1='folder-closed.png',
                                               command=self.file_dialog_command)

        # --------------------------------------------------------------------------------------------------------------
        cmds.formLayout(self.main_layout, edit=True,
                        attachForm=[(self.export_nodes, 'top', 15),
                                    (self.export_nodes, 'left', -50),
                                    (self.export_edges, 'top', 15),
                                    (self.export_connections, 'top', 15),
                                    (self.export_path, 'left', -25)],

                        attachControl=[(self.export_edges, 'left', 0, self.export_nodes),
                                       (self.export_connections, 'left', 0, self.export_edges),
                                       (self.export_path, 'top', 20, self.export_nodes),
                                       (self.file_search, 'top', 20, self.export_nodes),
                                       (self.file_search, 'left', 5, self.export_path)])

    def apply_command(self, *args):
        """
        Apply button command
        """
        export_nodes = cmds.checkBoxGrp(self.export_nodes, query=True, value1=True)
        export_edges = cmds.checkBoxGrp(self.export_edges, query=True, value1=True)
        export_connections = cmds.checkBoxGrp(self.export_connections, query=True, value1=True)

        export_path = cmds.textFieldGrp(self.export_path, query=True, text=True)
        file_name = os.path.basename(export_path).split('.ma')[0]
        export_path = os.path.dirname(export_path)

        importExportLib.export_nodes_and_connections(file_name=file_name, path=export_path,
                                                     export_nodes=export_nodes,
                                                     export_edges=export_edges,
                                                     export_connections=export_connections)

    def file_dialog_command(self, *args):
        """
        Open the explorer window to set the path
        """
        folder_path = cmds.fileDialog2(dialogStyle=2, fileMode=0, fileFilter='*.ma')
        if folder_path:
            cmds.textFieldGrp(self.export_path, edit=True, text=folder_path[0])
