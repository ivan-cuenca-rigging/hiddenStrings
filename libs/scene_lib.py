# Maya imports
from maya import cmds


def togle_hidden_in_outliner(*args):
    """
    Toggle hidden in outliner property in all the outliners of the scene
    """
    outliner_panels_list = cmds.getPanel(type="outlinerPanel")
    attr_value = cmds.outlinerEditor(outliner_panels_list[0], query=True, ignoreHiddenAttribute=True)

    for outliner_panel in outliner_panels_list:
        cmds.outlinerEditor(outliner_panel, edit=True, ignoreHiddenAttribute=not attr_value)
