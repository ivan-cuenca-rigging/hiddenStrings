# Imports
import os
from functools import partial

# Maya imports
from maya import cmds

# Project imports
from hiddenStrings.libs import window_lib, import_export_lib, skeleton_lib, skin_lib


class ExportSkinWindow(window_lib.Helper):
    def __init__(self, *args):
        """
        Create the export skin window
        :param title: str, title of the window
        :param size: list, width and height
        """
        super(ExportSkinWindow, self).__init__(title='Export Skin Options', size=(450, 130))

        self.skin_index = cmds.intFieldGrp(label='Skin index: ', value1=1)
        self.all_skin_index = cmds.checkBoxGrp(label='All: ', value1=False,
                                               onCommand=self.set_skin_index_enable,
                                               offCommand=self.set_skin_index_enable)

        export_path = '{}/skinClusters'.format(os.path.dirname(cmds.file(query=True, sceneName=True)))
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
                import_export_lib.export_skin_clusters(node_list=selection_list, path=export_path, skin_index=None)
            else:
                skin_index = cmds.intFieldGrp(self.skin_index, query=True, value1=True)
                import_export_lib.export_skin_clusters(node_list=selection_list, path=export_path,
                                                       skin_index=skin_index)

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

    def bottom_layout(self):
        add_button, apply_button, close_button = super(ExportSkinWindow, self).bottom_layout()
        cmds.button(add_button, edit=True, label='Export')


class ImportSkinWindow(window_lib.Helper):
    def __init__(self, *args):
        """
        Create the import skin window
        :param title: str, title of the window
        :param size: list, width and height
        """
        super(ImportSkinWindow, self).__init__(title='Import Skin Options', size=(450, 225))

        self.skin_index = cmds.intFieldGrp(label='Skin index: ', value1=1)
        self.import_folder = cmds.checkBoxGrp(label='Import folder: ', value1=False,
                                              onCommand=self.set_skin_index_enable,
                                              offCommand=self.set_skin_index_enable)

        self.import_method = cmds.optionMenu(label='Import method')
        cmds.menuItem(self.import_method, label='Index')
        cmds.menuItem(self.import_method, label='Nearest')

        self.search_for = cmds.textFieldGrp(label='Search for: ')

        self.replace_with = cmds.textFieldGrp(label='Replace with: ')

        import_path = '{}/skinClusters'.format(os.path.dirname(cmds.file(query=True, sceneName=True)))
        self.import_path = cmds.textFieldGrp(label='Path: ', text=import_path)
        self.file_search = cmds.iconTextButton(style='iconOnly', image1='folder-closed.png',
                                               command=self.file_dialog_command)

        # --------------------------------------------------------------------------------------------------------------
        cmds.formLayout(self.main_layout, edit=True,
                        attachForm=[(self.import_folder, 'top', 20),
                                    (self.import_method, 'left', 59)],

                        attachControl=[(self.skin_index, 'top', 5, self.import_folder),
                                       (self.import_method, 'top', 5, self.skin_index),
                                       (self.search_for, 'top', 5, self.import_method),
                                       (self.replace_with, 'top', 5, self.search_for),
                                       (self.import_path, 'top', 5, self.replace_with),
                                       (self.file_search, 'top', 5, self.replace_with),
                                       (self.file_search, 'left', 5, self.import_path)])

    def apply_command(self, *args):
        """
        Apply button command
        """
        import_folder = cmds.checkBoxGrp(self.import_folder, query=True, value1=True)

        import_method = cmds.optionMenu(self.import_method, query=True, value=True).lower()

        search_for = cmds.textFieldGrp(self.search_for, query=True, text=True)

        replace_with = cmds.textFieldGrp(self.replace_with, query=True, text=True)

        import_path = cmds.textFieldGrp(self.import_path, query=True, text=True)

        if import_folder:
            import_export_lib.import_skin_clusters(path=import_path, import_method=import_method)
        else:
            node = cmds.ls(sl=True)[0]
            skin_index = cmds.intFieldGrp(self.skin_index, query=True, value1=True)
            import_export_lib.import_skin_cluster(node=node, path=import_path,
                                                  skin_index=skin_index, import_method=import_method,
                                                  search_for=search_for, replace_with=replace_with)

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

    def set_skin_index_enable(self, *args):
        """
        Change skin_index enable
        """
        if cmds.checkBoxGrp(self.import_folder, query=True, value1=True):
            cmds.intFieldGrp(self.skin_index, edit=True, enable=False)
        else:
            cmds.intFieldGrp(self.skin_index, edit=True, enable=True)

    def bottom_layout(self):
        add_button, apply_button, close_button = super(ImportSkinWindow, self).bottom_layout()
        cmds.button(add_button, edit=True, label='Import')


class PushJointWindow(window_lib.Helper):
    def __init__(self, *args):
        """
        Create the renamer window
        :param title: str, title of the window
        :param size: list, width and height
        """
        super(PushJointWindow, self).__init__(title='Push Joint', size=(450, 215))

        # Search and replace
        self.parent_node = cmds.textFieldGrp(label='Parent: ')
        self.get_parent = cmds.iconTextButton(image='addClip.png', command=partial(self.get_from_scene,
                                                                                   text_field=self.parent_node))
        self.driver_node = cmds.textFieldGrp(label='Driver: ')
        self.get_driver = cmds.iconTextButton(image='addClip.png', command=partial(self.get_from_scene,
                                                                                   text_field=self.driver_node))
        self.suffix = cmds.textFieldGrp(label='Suffix: ')

        self.forbidden_word = cmds.textFieldGrp(label='Forbidden word: ', text='01')

        self.rotation_axis = cmds.optionMenu(label='Rotation axis')
        cmds.menuItem(self.rotation_axis, label=' X')
        cmds.menuItem(self.rotation_axis, label='-X')
        cmds.menuItem(self.rotation_axis, label=' Y')
        cmds.menuItem(self.rotation_axis, label='-Y')
        cmds.menuItem(self.rotation_axis, label=' Z')
        cmds.menuItem(self.rotation_axis, label='-Z')
        cmds.optionMenu(self.rotation_axis, edit=True, value='-Y')

        self.structural_parent = cmds.textFieldGrp(label='Structural parent: ', text='pushJoints_c_grp')

        # --------------------------------------------------------------------------------------------------------------
        cmds.formLayout(self.main_layout, edit=True,
                        attachForm=[(self.parent_node, 'top', 10),
                                    (self.get_parent, 'top', 10),
                                    (self.rotation_axis, 'left', 70)],

                        attachControl=[(self.get_parent, 'left', 5, self.parent_node),
                                       (self.driver_node, 'top', 5, self.parent_node),
                                       (self.get_driver, 'top', 5, self.parent_node),
                                       (self.get_driver, 'left', 5, self.parent_node),
                                       (self.suffix, 'top', 5, self.driver_node),
                                       (self.forbidden_word, 'top', 5, self.suffix),
                                       (self.rotation_axis, 'top', 5, self.forbidden_word),
                                       (self.structural_parent, 'top', 5, self.rotation_axis)])

    def apply_command(self, *args):
        parent_node = cmds.textFieldGrp(self.parent_node, query=True, text=True)

        driver_node = cmds.textFieldGrp(self.driver_node, query=True, text=True)

        suffix = cmds.textFieldGrp(self.suffix, query=True, text=True)

        forbidden_word = cmds.textFieldGrp(self.forbidden_word, query=True, text=True)

        rotation_axis = cmds.optionMenu(self.rotation_axis, query=True, value=True)
        if '-' not in rotation_axis:
            rotation_axis = rotation_axis[-1]

        structural_parent = cmds.textFieldGrp(self.structural_parent, query=True, text=True)

        skeleton_lib.create_push_joint(parent_node=parent_node, driver_node=driver_node,
                                       suffix=suffix,
                                       forbidden_word=forbidden_word,
                                       rotation_axis=rotation_axis,
                                       structural_parent=structural_parent)

    @staticmethod
    def get_from_scene(text_field, *args):
        cmds.textFieldGrp(text_field, edit=True, text=cmds.ls(selection=True)[0])


class TransferSkinWindow(window_lib.Helper):
    def __init__(self, *args):
        """
        Create the import skin window
        :param title: str, title of the window
        :param size: list, width and height
        """
        super(TransferSkinWindow, self).__init__(title='Import Skin Options', size=(450, 150))

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

        skin_lib.transfer_skin(source=cmds.ls(selection=True)[0],
                               target=cmds.ls(selection=True)[-1],
                               source_skin_index=source_skin_index,
                               target_skin_index=target_skin_index,
                               surface_association=transfer_method)
