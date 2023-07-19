# Imports
import os
from functools import partial

# Maya imports
from maya import cmds

# Project imports
from hiddenStrings.libs import window_lib, import_export_lib, trigger_lib, blend_shape_lib


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


class CreateAngleWindow(window_lib.Helper):
    def __init__(self, *args):
        """
        Create the import blendShape window
        :param title: str, title of the window
        :param size: list, width and height
        """
        super(CreateAngleWindow, self).__init__(title='Create Bary Options', size=(450, 105))

        self.parent = cmds.textFieldGrp(label='Parent: ')
        self.get_parent = cmds.iconTextButton(image='addClip.png', command=partial(self.get_from_scene,
                                                                                   text_field=self.parent))
        self.driver = cmds.textFieldGrp(label='Driver: ')
        self.get_driver = cmds.iconTextButton(image='addClip.png', command=partial(self.get_from_scene,
                                                                                   text_field=self.driver))
        # --------------------------------------------------------------------------------------------------------------
        cmds.formLayout(self.main_layout, edit=True,
                        attachForm=[(self.parent, 'top', 10),
                                    (self.get_parent, 'top', 10)],

                        attachControl=[(self.driver, 'top', 5, self.parent),
                                       (self.get_driver, 'top', 5, self.parent),
                                       (self.get_driver, 'left', 5, self.driver),
                                       (self.get_parent, 'left', 5, self.parent)])

    def apply_command(self, *args):
        """
        Apply button command
        """
        parent = cmds.textFieldGrp(self.parent, query=True, text=True)

        driver = cmds.textFieldGrp(self.driver, query=True, text=True)

        trigger_lib.create_angle_trigger(parent_node=parent, driver_node=driver)

    @staticmethod
    def get_from_scene(text_field, *args):
        cmds.textFieldGrp(text_field, edit=True, text=cmds.ls(selection=True)[0])


class CreateBaryWindow(window_lib.Helper):
    def __init__(self, *args):
        """
        Create the import blendShape window
        :param title: str, title of the window
        :param size: list, width and height
        """
        super(CreateBaryWindow, self).__init__(title='Create Bary Options', size=(450, 185))

        self.descriptor = cmds.textFieldGrp(label='Descriptor: ', text='bary')

        # Side
        self.side = cmds.optionMenu(label='Side')
        cmds.menuItem(self.side, label='Left')
        cmds.menuItem(self.side, label='Center')
        cmds.menuItem(self.side, label='Right')
        cmds.optionMenu(self.side, edit=True, value='Center')

        self.parent = cmds.textFieldGrp(label='Parent: ')
        self.get_parent = cmds.iconTextButton(image='addClip.png', command=partial(self.get_from_scene,
                                                                                   text_field=self.parent))
        self.driver = cmds.textFieldGrp(label='Driver: ')
        self.get_driver = cmds.iconTextButton(image='addClip.png', command=partial(self.get_from_scene,
                                                                                   text_field=self.driver))

        # Driver axis
        self.driver_axis = cmds.optionMenu(label='Driver axis')
        cmds.menuItem(self.driver_axis, label='X')
        cmds.menuItem(self.driver_axis, label='-X')
        cmds.menuItem(self.driver_axis, label='Y')
        cmds.menuItem(self.driver_axis, label='-Y')
        cmds.menuItem(self.driver_axis, label='Z')
        cmds.menuItem(self.driver_axis, label='-Z')
        cmds.optionMenu(self.driver_axis, edit=True, value='X')

        # --------------------------------------------------------------------------------------------------------------
        cmds.formLayout(self.main_layout, edit=True,
                        attachForm=[(self.descriptor, 'top', 10),
                                    (self.side, 'left', 115),
                                    (self.driver_axis, 'left', 85)],

                        attachControl=[(self.side, 'top', 5, self.descriptor),
                                       (self.parent, 'top', 5, self.side),
                                       (self.get_parent, 'top', 5, self.side),
                                       (self.get_parent, 'left', 5, self.parent),
                                       (self.driver, 'top', 5, self.parent),
                                       (self.get_driver, 'top', 5, self.parent),
                                       (self.get_driver, 'left', 5, self.driver),
                                       (self.driver_axis, 'top', 5, self.driver)])

    def apply_command(self, *args):
        """
        Apply button command
        """
        descriptor = cmds.textFieldGrp(self.descriptor, query=True, text=True)

        side = cmds.optionMenu(self.side, query=True, value=True)
        if side == 'Left':
            side = 'l'
        if side == 'Center':
            side = 'c'
        if side == 'Right':
            side = 'r'

        parent = cmds.textFieldGrp(self.parent, query=True, text=True)

        driver = cmds.textFieldGrp(self.driver, query=True, text=True)

        driver_axis = cmds.optionMenu(self.driver_axis, query=True, value=True)

        trigger_lib.create_bary_trigger(descriptor=descriptor,
                                        side=side,
                                        parent_node=parent,
                                        driver_node=driver,
                                        driver_axis=driver_axis)

    @staticmethod
    def get_from_scene(text_field, *args):
        cmds.textFieldGrp(text_field, edit=True, text=cmds.ls(selection=True)[0])


class AutomaticCorrectiveWindow(window_lib.Helper):
    def __init__(self, *args):
        """
        Create the import blendShape window
        :param title: str, title of the window
        :param size: list, width and height
        """
        super(AutomaticCorrectiveWindow, self).__init__(title='Create automatic corrective Options', size=(450, 185))

        self.geometry = cmds.textFieldGrp(label='Geometry: ')
        self.get_geometry = cmds.iconTextButton(image='addClip.png', command=partial(self.get_from_scene,
                                                                                     text_field=self.geometry))

        self.control = cmds.textFieldGrp(label='Control: ')
        self.get_control = cmds.iconTextButton(image='addClip.png', command=partial(self.get_from_scene,
                                                                                    text_field=self.control))

        self.attribute_name = cmds.textFieldGrp(label='Attribute: ')
        self.attribute_value = cmds.textFieldGrp(label='Value: ')

        self.create_sdk = cmds.checkBoxGrp(label='Create SetDrivenKey: ', value1=True)

        # --------------------------------------------------------------------------------------------------------------
        cmds.formLayout(self.main_layout, edit=True,
                        attachForm=[(self.geometry, 'top', 10),
                                    (self.get_geometry, 'top', 10)],

                        attachControl=[(self.get_geometry, 'left', 5, self.geometry),
                                       (self.control, 'top', 5, self.geometry),
                                       (self.get_control, 'top', 5, self.geometry),
                                       (self.get_control, 'left', 5, self.control),
                                       (self.attribute_name, 'top', 5, self.control),
                                       (self.attribute_value, 'top', 5, self.attribute_name),
                                       (self.create_sdk, 'top', 5, self.attribute_value)])

    def apply_command(self, *args):
        geometry = cmds.textFieldGrp(self.geometry, query=True, text=True)

        control_list = cmds.ls(cmds.textFieldGrp(self.control, query=True, text=True))

        attribute_name = cmds.textFieldGrp(self.attribute_name, query=True, text=True)
        attribute_value = float(cmds.textFieldGrp(self.attribute_value, query=True, text=True))
        attribute_value = int(attribute_value) if attribute_value.is_integer() else attribute_value

        create_sdk = cmds.checkBoxGrp(self.create_sdk, query=True, value1=True)

        for ctr in control_list:
            blend_shape_lib.automatic_corrective(geometry_name=geometry,
                                                 control_name=ctr,
                                                 attr_name=attribute_name,
                                                 attr_value=attribute_value,
                                                 create_sdk=create_sdk)

    @staticmethod
    def get_from_scene(text_field, *args):
        cmds.textFieldGrp(text_field, edit=True, text=cmds.ls(selection=True)[0])
