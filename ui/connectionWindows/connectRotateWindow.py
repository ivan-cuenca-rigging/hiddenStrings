# Maya imports
from maya import cmds

# Project imports
from hiddenStrings.libs.helpers import windowHelper


class ConnectRotateWindow(windowHelper.WindowHelper):
    def __init__(self, *args):
        """
        Create the ConnectRotateMenu option window
        :param title: str, title of the window
        :param size: list, width and height
        """
        super().__init__(title='connect scale Options', size=(450, 125))

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
