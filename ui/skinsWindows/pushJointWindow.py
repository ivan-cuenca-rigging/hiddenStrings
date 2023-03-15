# Maya imports
from maya import cmds

# Project imports
from hiddenStrings.libs.helpers import windowHelper
from hiddenStrings.libs import skeletonLib


class PushJointWindow(windowHelper.WindowHelper):
    def __init__(self, *args):
        """
        Create the renamer window
        :param title: str, title of the window
        :param size: list, width and height
        """
        super(PushJointWindow, self).__init__(title='Push Joint', size=(450, 215))

        # Search and replace
        self.parent_node = cmds.textFieldGrp(label='Parent: ')

        self.driver_node = cmds.textFieldGrp(label='Driver: ')

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
                                    (self.rotation_axis, 'left', 70)],

                        attachControl=[(self.driver_node, 'top', 5, self.parent_node),
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

        skeletonLib.push_joint(parent_node=parent_node, driven_node=driver_node,
                               suffix=suffix,
                               forbidden_word=forbidden_word,
                               rotation_axis=rotation_axis,
                               structural_parent=structural_parent)