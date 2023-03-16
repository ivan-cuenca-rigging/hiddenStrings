# Maya imports
import os

from maya import cmds

# Project imports
from hiddenStrings.libs import connection_lib, window_lib, import_export_lib


class ConnectOffsetParentMatrixWindow(window_lib.Helper):
    def __init__(self, *args):
        """
        Create the connectOffsetParentMatrix option window
        :param title: str, title of the window
        :param size: list, width and height
        """
        super(ConnectOffsetParentMatrixWindow, self).__init__(title='connect offset parent matrix Options',
                                                              size=(450, 150))

        self.translate = cmds.checkBoxGrp(label='Translate: ', value1=True)
        self.rotate = cmds.checkBoxGrp(label='Rotate: ', value1=True)
        self.scale = cmds.checkBoxGrp(label='Scale: ', value1=True)
        self.shear = cmds.checkBoxGrp(label='Shear: ', value1=True)

        # --------------------------------------------------------------------------------------------------------------
        cmds.formLayout(self.main_layout, edit=True,
                        attachForm=[(self.translate, 'top', 10),
                                    (self.translate, 'left', 0)],

                        attachControl=[(self.rotate, 'top', 5, self.translate),
                                       (self.scale, 'top', 5, self.rotate),
                                       (self.shear, 'top', 5, self.scale)])

    def apply_command(self, *args):
        """
        Apply button command
        """
        sel = cmds.ls(selection=True)
        if len(sel) != 2:
            cmds.error('Connect offset parent matrix: You must select two nodes ')

        translate = cmds.checkBoxGrp(self.translate, query=True, value1=True)
        rotate = cmds.checkBoxGrp(self.rotate, query=True, value1=True)
        scale = cmds.checkBoxGrp(self.scale, query=True, value1=True)
        shear = cmds.checkBoxGrp(self.shear, query=True, value1=True)

        connection_lib.connect_offset_parent_matrix(driver=sel[0],
                                                    driven=sel[1],
                                                    translate=translate,
                                                    rotate=rotate,
                                                    scale=scale,
                                                    shear=shear)


class ConnectRotateWindow(window_lib.Helper):
    def __init__(self, *args):
        """
        Create the ConnectRotateMenu option window
        :param title: str, title of the window
        :param size: list, width and height
        """
        super(ConnectRotateWindow, self).__init__(title='connect scale Options', size=(450, 125))

        self.rotate = cmds.checkBoxGrp(label='Rotate: ', value1=True,
                                       onCommand=self.set_rotate_axis_enable,
                                       offCommand=self.set_rotate_axis_enable)
        self.rotate_axis = cmds.checkBoxGrp(numberOfCheckBoxes=3, label1='X ', label2='Y ', label3='Z ',
                                            value1=True, value2=True, value3=True)

        # --------------------------------------------------------------------------------------------------------------
        cmds.formLayout(self.main_layout, edit=True,
                        attachForm=[(self.rotate, 'top', 10),
                                    (self.rotate, 'left', 0),
                                    (self.rotate_axis, 'left', 142)],

                        attachControl=[(self.rotate_axis, 'top', 5, self.rotate)])

    def apply_command(self, *args):
        """
        Apply button command
        """
        sel = cmds.ls(selection=True)
        if len(sel) != 2:
            cmds.error('Connect scale: You must select two nodes ')

        rotate = cmds.checkBoxGrp(self.rotate, query=True, value1=True)
        if rotate:
            rotate_x = cmds.checkBoxGrp(self.rotate_axis, query=True, value1=True, enable=True)
            rotate_y = cmds.checkBoxGrp(self.rotate_axis, query=True, value2=True, enable=True)
            rotate_z = cmds.checkBoxGrp(self.rotate_axis, query=True, value3=True, enable=True)

            if rotate_x:
                cmds.connectAttr('{}.rotateX'.format(sel[0]), '{}.rotateX'.format(sel[1]), force=True)
            if rotate_y:
                cmds.connectAttr('{}.rotateY'.format(sel[0]), '{}.rotateY'.format(sel[1]), force=True)
            if rotate_z:
                cmds.connectAttr('{}.rotateZ'.format(sel[0]), '{}.rotateZ'.format(sel[1]), force=True)

    def set_rotate_axis_enable(self, *args):
        if cmds.checkBoxGrp(self.rotate, query=True, enable=True, value1=True):
            cmds.checkBoxGrp(self.rotate_axis, edit=True, enable=True)
        else:
            cmds.checkBoxGrp(self.rotate_axis, edit=True, enable=False)


class ConnectScaleWindow(window_lib.Helper):
    def __init__(self, *args):
        """
        Create connect scale option Window
        :param title: str, title of the window
        :param size: list, width and height
        """
        super(ConnectScaleWindow, self).__init__(title='connect scale Options', size=(450, 125))

        self.scale = cmds.checkBoxGrp(label='Scale: ', value1=True,
                                      onCommand=self.set_scale_axis_enable,
                                      offCommand=self.set_scale_axis_enable)
        self.scale_axis = cmds.checkBoxGrp(numberOfCheckBoxes=3, label1='X ', label2='Y ', label3='Z ',
                                           value1=True, value2=True, value3=True)

        # --------------------------------------------------------------------------------------------------------------
        cmds.formLayout(self.main_layout, edit=True,
                        attachForm=[(self.scale, 'top', 10),
                                    (self.scale, 'left', 0),
                                    (self.scale_axis, 'left', 142)],

                        attachControl=[(self.scale_axis, 'top', 5, self.scale)])

    def apply_command(self, *args):
        """
        Apply button command
        """
        sel = cmds.ls(selection=True)
        if len(sel) != 2:
            cmds.error('Connect scale: You must select two nodes ')

        scale = cmds.checkBoxGrp(self.scale, query=True, value1=True)
        if scale:
            scale_x = cmds.checkBoxGrp(self.scale_axis, query=True, value1=True, enable=True)
            scale_y = cmds.checkBoxGrp(self.scale_axis, query=True, value2=True, enable=True)
            scale_z = cmds.checkBoxGrp(self.scale_axis, query=True, value3=True, enable=True)

            if scale_x:
                cmds.connectAttr('{}.scaleX'.format(sel[0]), '{}.scaleX'.format(sel[1]), force=True)
            if scale_y:
                cmds.connectAttr('{}.scaleY'.format(sel[0]), '{}.scaleY'.format(sel[1]), force=True)
            if scale_z:
                cmds.connectAttr('{}.scaleZ'.format(sel[0]), '{}.scaleZ'.format(sel[1]), force=True)

    def set_scale_axis_enable(self, *args):
        if cmds.checkBoxGrp(self.scale, query=True, enable=True, value1=True):
            cmds.checkBoxGrp(self.scale_axis, edit=True, enable=True)
        else:
            cmds.checkBoxGrp(self.scale_axis, edit=True, enable=False)


class ConnectTranslateRotateScaleWindow(window_lib.Helper):
    def __init__(self, *args):
        """
        Create the ConnectTranslateRotateScale option window
        :param title: str, title of the window
        :param size: list, width and height
        """
        super(ConnectTranslateRotateScaleWindow, self).__init__(title='connect translate rotate scale Options',
                                                                size=(450, 200))

        self.translate = cmds.checkBoxGrp(label='Translate: ', label1='All', value1=True,
                                          onCommand=self.set_translate_axis_enable,
                                          offCommand=self.set_translate_axis_enable)
        self.translate_axis = cmds.checkBoxGrp(numberOfCheckBoxes=3, label1='X ', label2='Y ', label3='Z ',
                                               value1=True, value2=True, value3=True)

        self.rotate = cmds.checkBoxGrp(label='Rotate: ', value1=True,
                                       onCommand=self.set_rotate_axis_enable,
                                       offCommand=self.set_rotate_axis_enable)
        self.rotate_axis = cmds.checkBoxGrp(numberOfCheckBoxes=3, label1='X ', label2='Y ', label3='Z ',
                                            value1=True, value2=True, value3=True)

        self.scale = cmds.checkBoxGrp(label='Scale: ', value1=True,
                                      onCommand=self.set_scale_axis_enable,
                                      offCommand=self.set_scale_axis_enable)
        self.scale_axis = cmds.checkBoxGrp(numberOfCheckBoxes=3, label1='X ', label2='Y ', label3='Z ',
                                           value1=True, value2=True, value3=True)

        # --------------------------------------------------------------------------------------------------------------
        cmds.formLayout(self.main_layout, edit=True,
                        attachForm=[(self.translate, 'top', 10),
                                    (self.translate, 'left', 0),
                                    (self.translate_axis, 'left', 142),
                                    (self.rotate_axis, 'left', 142),
                                    (self.scale_axis, 'left', 142)],

                        attachControl=[(self.translate_axis, 'top', 5, self.translate),
                                       (self.rotate, 'top', 5, self.translate_axis),
                                       (self.rotate_axis, 'top', 5, self.rotate),
                                       (self.scale, 'top', 5, self.rotate_axis),
                                       (self.scale_axis, 'top', 5, self.scale)])

    def apply_command(self, *args):
        """
        Apply button command
        """
        sel = cmds.ls(selection=True)
        if len(sel) != 2:
            cmds.error('Connect translate rotate scale: You must select two nodes ')

        translate = cmds.checkBoxGrp(self.translate, query=True, value1=True)
        if translate:
            translate_x = cmds.checkBoxGrp(self.translate_axis, query=True, value1=True, enable=True)
            translate_y = cmds.checkBoxGrp(self.translate_axis, query=True, value2=True, enable=True)
            translate_z = cmds.checkBoxGrp(self.translate_axis, query=True, value3=True, enable=True)

            if translate_x:
                cmds.connectAttr('{}.translateX'.format(sel[0]), '{}.translateX'.format(sel[1]), force=True)
            if translate_y:
                cmds.connectAttr('{}.translateY'.format(sel[0]), '{}.translateY'.format(sel[1]), force=True)
            if translate_z:
                cmds.connectAttr('{}.translateZ'.format(sel[0]), '{}.translateZ'.format(sel[1]), force=True)

        rotate = cmds.checkBoxGrp(self.rotate, query=True, value1=True)
        if rotate:
            rotate_x = cmds.checkBoxGrp(self.rotate_axis, query=True, value1=True, enable=True)
            rotate_y = cmds.checkBoxGrp(self.rotate_axis, query=True, value2=True, enable=True)
            rotate_z = cmds.checkBoxGrp(self.rotate_axis, query=True, value3=True, enable=True)

            if rotate_x:
                cmds.connectAttr('{}.rotateX'.format(sel[0]), '{}.rotateX'.format(sel[1]), force=True)
            if rotate_y:
                cmds.connectAttr('{}.rotateY'.format(sel[0]), '{}.rotateY'.format(sel[1]), force=True)
            if rotate_z:
                cmds.connectAttr('{}.rotateZ'.format(sel[0]), '{}.rotateZ'.format(sel[1]), force=True)

        scale = cmds.checkBoxGrp(self.scale, query=True, value1=True)
        if scale:
            scale_x = cmds.checkBoxGrp(self.scale_axis, query=True, value1=True, enable=True)
            scale_y = cmds.checkBoxGrp(self.scale_axis, query=True, value2=True, enable=True)
            scale_z = cmds.checkBoxGrp(self.scale_axis, query=True, value3=True, enable=True)

            if scale_x:
                cmds.connectAttr('{}.scaleX'.format(sel[0]), '{}.scaleX'.format(sel[1]), force=True)
            if scale_y:
                cmds.connectAttr('{}.scaleY'.format(sel[0]), '{}.scaleY'.format(sel[1]), force=True)
            if scale_z:
                cmds.connectAttr('{}.scaleZ'.format(sel[0]), '{}.scaleZ'.format(sel[1]), force=True)

    def set_translate_axis_enable(self, *args):
        if cmds.checkBoxGrp(self.translate, query=True, enable=True, value1=True):
            cmds.checkBoxGrp(self.translate_axis, edit=True, enable=True)
        else:
            cmds.checkBoxGrp(self.translate_axis, edit=True, enable=False)

    def set_rotate_axis_enable(self, *args):
        if cmds.checkBoxGrp(self.rotate, query=True, enable=True, value1=True):
            cmds.checkBoxGrp(self.rotate_axis, edit=True, enable=True)
        else:
            cmds.checkBoxGrp(self.rotate_axis, edit=True, enable=False)

    def set_scale_axis_enable(self, *args):
        if cmds.checkBoxGrp(self.scale, query=True, enable=True, value1=True):
            cmds.checkBoxGrp(self.scale_axis, edit=True, enable=True)
        else:
            cmds.checkBoxGrp(self.scale_axis, edit=True, enable=False)


class ConnectTranslateWindow(window_lib.Helper):
    def __init__(self, *args):
        """
        Create the ConnectTranslateMenu option window
        :param title: str, title of the window
        :param size: list, width and height
        """
        super(ConnectTranslateWindow, self).__init__(title='connect translate Options', size=(450, 125))

        self.translate = cmds.checkBoxGrp(label='Translate: ', label1='All', value1=True,
                                          onCommand=self.set_translate_axis_enable,
                                          offCommand=self.set_translate_axis_enable)
        self.translate_axis = cmds.checkBoxGrp(numberOfCheckBoxes=3, label1='X ', label2='Y ', label3='Z ',
                                               value1=True, value2=True, value3=True)

        # --------------------------------------------------------------------------------------------------------------
        cmds.formLayout(self.main_layout, edit=True,
                        attachForm=[(self.translate, 'top', 10),
                                    (self.translate, 'left', 0),
                                    (self.translate_axis, 'left', 142)],

                        attachControl=[(self.translate_axis, 'top', 5, self.translate)])

    def apply_command(self, *args):
        """
        Apply button command
        """
        sel = cmds.ls(selection=True)
        if len(sel) != 2:
            cmds.error('Connect translate: You must select two nodes ')

        translate = cmds.checkBoxGrp(self.translate, query=True, value1=True)
        if translate:
            translate_x = cmds.checkBoxGrp(self.translate_axis, query=True, value1=True, enable=True)
            translate_y = cmds.checkBoxGrp(self.translate_axis, query=True, value2=True, enable=True)
            translate_z = cmds.checkBoxGrp(self.translate_axis, query=True, value3=True, enable=True)

            if translate_x:
                cmds.connectAttr('{}.translateX'.format(sel[0]), '{}.translateX'.format(sel[1]), force=True)
            if translate_y:
                cmds.connectAttr('{}.translateY'.format(sel[0]), '{}.translateY'.format(sel[1]), force=True)
            if translate_z:
                cmds.connectAttr('{}.translateZ'.format(sel[0]), '{}.translateZ'.format(sel[1]), force=True)

    def set_translate_axis_enable(self, *args):
        if cmds.checkBoxGrp(self.translate, query=True, enable=True, value1=True):
            cmds.checkBoxGrp(self.translate_axis, edit=True, enable=True)
        else:
            cmds.checkBoxGrp(self.translate_axis, edit=True, enable=False)


class ExportNodesAndConnectionsWindow(window_lib.Helper):
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

        import_export_lib.export_nodes_and_connections(file_name=file_name, path=export_path,
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


class ImportNodesAndConnectionsWindow(window_lib.Helper):
    def __init__(self, *args):
        """
        Create the import nodes and connections window
        :param title: str, title of the window
        :param size: list, width and height
        """
        super(ImportNodesAndConnectionsWindow, self).__init__(title='Import nodes and connections Options',
                                                              size=(450, 130))

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

        import_export_lib.import_nodes_and_connections(path=import_path,
                                                       import_nodes=import_nodes,
                                                       import_connections=import_connections)

    def file_dialog_command(self, *args):
        """
        Open the explorer window to set the path
        """
        folder_path = cmds.fileDialog2(dialogStyle=2, fileMode=1, fileFilter='*.ma')
        if folder_path:
            cmds.textFieldGrp(self.import_path, edit=True, text=folder_path[0])
