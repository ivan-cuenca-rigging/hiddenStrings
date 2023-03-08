# Maya imports
from maya import cmds

# Project imports
from hiddenStrings.libs.helpers import windowHelper
from hiddenStrings.libs import blendShapeLib


class ImportBlendShapeWindow(windowHelper.WindowHelper):
    def __init__(self, *args):
        """
        Create the import blendShape window
        :param title: str, title of the window
        :param size: list, width and height
        """
        super().__init__(title='Import blendShape Options', size=(450, 150))

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
            blendShapeLib.import_blend_shapes(path=import_path)
        else:
            node = cmds.ls(sl=True)[0]
            blendShapeLib.import_blend_shape(node=node, path=import_path)

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
