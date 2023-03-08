# Maya imports
from maya import cmds

# Project imports
from hiddenStrings.libs.helpers import windowHelper
from hiddenStrings.libs import skinLib


class ImportSkinWindow(windowHelper.WindowHelper):
    def __init__(self, *args):
        """
        Create the import skin window
        :param title: str, title of the window
        :param size: list, width and height
        """
        super().__init__(title='Import Skin Options', size=(450, 175))

        self.skin_index = cmds.intFieldGrp(label='Skin index: ', value1=1)
        self.import_folder = cmds.checkBoxGrp(label='Import folder: ', value1=False,
                                              onCommand=self.set_skin_index_enable,
                                              offCommand=self.set_skin_index_enable)

        self.import_method = cmds.optionMenu(label='Import method')
        cmds.menuItem(self.import_method, label='Index')
        cmds.menuItem(self.import_method, label='Nearest')

        self.import_path = cmds.textFieldGrp(label='Path: ')
        self.file_search = cmds.iconTextButton(style='iconOnly', image1='folder-closed.png',
                                               command=self.file_dialog_command)

        # --------------------------------------------------------------------------------------------------------------
        cmds.formLayout(self.main_layout, edit=True,
                        attachForm=[(self.import_folder, 'top', 20),
                                    (self.import_method, 'left', 59)],

                        attachControl=[(self.skin_index, 'top', 5, self.import_folder),
                                       (self.import_method, 'top', 5, self.skin_index),
                                       (self.import_path, 'top', 5, self.import_method),
                                       (self.file_search, 'top', 5, self.import_method),
                                       (self.file_search, 'left', 5, self.import_path)])

    def apply_command(self, *args):
        """
        Apply button command
        """
        import_folder = cmds.checkBoxGrp(self.import_folder, query=True, value1=True)

        import_method = cmds.optionMenu(self.import_method, query=True, value=True).lower()

        import_path = cmds.textFieldGrp(self.import_path, query=True, text=True)

        if import_folder:
            skinLib.import_skin_clusters(path=import_path, import_method=import_method)
        else:
            node = cmds.ls(sl=True)[0]
            skin_index = cmds.intFieldGrp(self.skin_index, query=True, value1=True)
            skinLib.import_skin_cluster(node=node, path=import_path,
                                        skin_index=skin_index, import_method=import_method)

    def file_dialog_command(self, *args):
        """
        Open the explorer window to set the path
        """
        if cmds.checkBoxGrp(self.import_folder, query=True, value1=True):
            folder_path = cmds.fileDialog2(dialogStyle=2, fileMode=3)
        else:
            folder_path = cmds.fileDialog2(dialogStyle=2, fileMode=1)

        if folder_path:
            cmds.textFieldGrp(self.import_path, edit=True, text=folder_path[0])

    def set_skin_index_enable(self, *args):
        """
        Change skin_index enable
        """
        if cmds.checkBoxGrp(self.import_folder, query=True, value1=True):
            cmds.intFieldGrp(self.skin_index, edit=True, enable=False)
        else:
            cmds.intFieldGrp(self.skin_index, edit=True, enable=True)
