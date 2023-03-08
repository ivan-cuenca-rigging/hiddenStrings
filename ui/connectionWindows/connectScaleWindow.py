# Maya imports
from maya import cmds

# Project imports
from hiddenStrings.libs.helpers import windowHelper


class ConnectScaleWindow(windowHelper.WindowHelper):
    def __init__(self, *args):
        """
        Create connect scale option Window
        :param title: str, title of the window
        :param size: list, width and height
        """
        super().__init__(title='connect scale Options', size=(450, 125))

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
