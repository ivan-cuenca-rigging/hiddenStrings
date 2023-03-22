# Imports
import os

# Maya imports
from maya import cmds

# Project imports
from hiddenStrings.libs import window_lib, import_export_lib


class ExportBlendShapeWindow(window_lib.Helper):
    def __init__(self, *args):
        """
        Create the export blendShape window
        :param title: str, title of the window
        :param size: list, width and height
        """
        super(ExportBlendShapeWindow, self).__init__(title='Export blendShape Options', size=(450, 130))
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

        import_export_lib.export_blend_shapes(node_list=cmds.ls(selection=True), path=export_path)

    def file_dialog_command(self, *args):
        """
        Open the explorer window to set the path
        """
        folder_path = cmds.fileDialog2(dialogStyle=2, fileMode=2)
        if folder_path:
            cmds.textFieldGrp(self.export_path, edit=True, text=folder_path[0])

    def bottom_layout(self):
        add_button, apply_button, close_button = super(ExportBlendShapeWindow, self).bottom_layout()
        cmds.button(add_button, edit=True, label='Export')


class ImportBlendShapeWindow(window_lib.Helper):
    def __init__(self, *args):
        """
        Create the import blendShape window
        :param title: str, title of the window
        :param size: list, width and height
        """
        super(ImportBlendShapeWindow, self).__init__(title='Import blendShape Options', size=(450, 150))

        self.import_folder = cmds.checkBoxGrp(label='Import folder: ', value1=False)

        self.import_path = cmds.textFieldGrp(label='Path: ')
        self.file_search = cmds.iconTextButton(style='iconOnly', image1='folder-closed.png',
                                               command=self.file_dialog_command)

        # --------------------------------------------------------------------------------------------------------------
        cmds.formLayout(self.main_layout, edit=True,
                        attachForm=[(self.import_folder, 'top', 35)],

                        attachControl=[(self.import_path, 'top', 5, self.import_folder),
                                       (self.file_search, 'top', 5, self.import_folder),
                                       (self.file_search, 'left', 5, self.import_path)])

    def apply_command(self, *args):
        """
        Apply button command
        """
        import_folder = cmds.checkBoxGrp(self.import_folder, query=True, value1=True)

        import_path = cmds.textFieldGrp(self.import_path, query=True, text=True)

        if import_folder:
            import_export_lib.import_blend_shapes(path=import_path)
        else:
            node = cmds.ls(sl=True)[0]
            import_export_lib.import_blend_shape(node=node, path=import_path)

    def file_dialog_command(self, *args):
        """
        Open the explorer window to set the path
        """
        if cmds.checkBoxGrp(self.import_folder, query=True, value1=True):
            folder_path = cmds.fileDialog2(dialogStyle=2, fileMode=2)
        else:
            folder_path = cmds.fileDialog2(dialogStyle=2, fileMode=1)

        if folder_path:
            cmds.textFieldGrp(self.import_path, edit=True, text=folder_path[0])

    def bottom_layout(self):
        add_button, apply_button, close_button = super(ImportBlendShapeWindow, self).bottom_layout()
        cmds.button(add_button, edit=True, label='Import')
