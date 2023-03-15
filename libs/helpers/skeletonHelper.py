# Maya imports
from maya import cmds

# Project imports
from hiddenStrings.libs import usageLib, skeletonLib
from hiddenStrings.libs.helpers import nodeHelper


class SkeletonHelper(nodeHelper.NodeHelper):
    def __init__(self, name):
        """
        :param name: str
        """
        super(SkeletonHelper, self).__init__(name)
        self.name = name
        self.check_usage()
        self.check_side()

    # ---------- Checks Methods----------
    def check_usage(self):
        """
        Check if the usage is valid
        """
        if self.get_usage() not in usageLib.skeleton_valid_usages:
            cmds.warning('this control has not a valid usage, {}'.format(usageLib.skeleton_valid_usages))

    # ---------- Create Method ----------
    def create(self,
               zero=False,
               parent=None,
               matrix=None,
               matrix_translation=False,
               matrix_rotation=False,):
        """
        Create a skeleton
        :param zero: bool, if yes it will create a zero group
        :param parent: str, control's parent
        :param matrix: skeleton, control's matrix
        :param matrix_translation: bool, if true only translation will be used
        :param matrix_rotation: bool, if true only rotation will be used
        :return: skeleton's name
        """
        if cmds.objExists(self.name):
            cmds.error('the {} already exists in the scene'.format(self.name))

        cmds.createNode('joint', name=self.name)

        skeletonLib.set_joint_label(self.name)

        if zero:
            self.create_zero()
        if parent:
            self.set_parent(parent)
        if matrix:
            self.set_offset_parent_matrix(matrix, translation=matrix_translation, rotation=matrix_rotation)

        cmds.select(self.name)

        return self.name
