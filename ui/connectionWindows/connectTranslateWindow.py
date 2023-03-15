# Maya imports
from maya import cmds

# Project imports
from hiddenStrings.libs.helpers import windowHelper


class ConnectTranslateWindow(windowHelper.WindowHelper):
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
