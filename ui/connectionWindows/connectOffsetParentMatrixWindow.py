# Maya imports
from maya import cmds

# Project imports
from hiddenStrings.libs import connectionLib
from hiddenStrings.libs.helpers import windowHelper


class ConnectOffsetParentMatrixWindow(windowHelper.WindowHelper):
    def __init__(self, *args):
        """
        Create the connectOffsetParentMatrix option window
        :param title: str, title of the window
        :param size: list, width and height
        """
        super().__init__(title='connect offset parent matrix Options', size=(450, 150))

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

        connectionLib.connect_offset_parent_matrix(driver=sel[0],
                                                   driven=sel[1],
                                                   translate=translate,
                                                   rotate=rotate,
                                                   scale=scale,
                                                   shear=shear)
