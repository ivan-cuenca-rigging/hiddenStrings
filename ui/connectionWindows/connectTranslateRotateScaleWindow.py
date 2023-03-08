# Maya imports
from maya import cmds

# Project imports
from hiddenStrings.libs.helpers import windowHelper


class ConnectTranslateRotateScaleWindow(windowHelper.WindowHelper):
    def __init__(self, *args):
        """
        Create the ConnectTranslateRotateScale option window
        :param title: str, title of the window
        :param size: list, width and height
        """
        super().__init__(title='connect translate rotate scale Options', size=(450, 200))

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
