# Imports
import os
from PySide2.QtGui import QIcon
from shiboken2 import wrapInstance
from PySide2.QtWidgets import QWidget

# Maya imports
from maya import cmds
from maya import OpenMayaUI


class WindowHelper(object):
    def __init__(self, title, size=(400, 400), *args):
        """
        Create a default window with the 3 buttons on the bottom (add, apply, close)
        :param title: str, tittle of the window
        :param size: list, width and height
        """

        self.window = ''.join([x.capitalize() for x in title.split(' ')])
        self.window = '{}_window'.format(self.window)
        self.title = title
        self.size = size

        # Close old window if it is open
        if cmds.window(self.window, exists=True):
            self.close_window()

        # Create new window
        self.open_window()

        # Main Layout
        self.main_layout = cmds.formLayout(numberOfDivisions=100)

        # Bottom Layout
        self.bottom_layout()

        # Display new window
        cmds.showWindow()

        # Add the icon to the window -- we need a QWidget
        window_q_widget = OpenMayaUI.MQtUtil.findWindow(self.window)
        window_widget = wrapInstance(int(window_q_widget), QWidget)
        icon_path = r"{}//icons//hiddenStrings.png".format(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        q_icon = QIcon(icon_path)
        window_widget.setWindowIcon(q_icon)

    def bottom_layout(self,):
        """
        Create the bottom layout (add, apply and close buttons)
        """
        bottom_separator = cmds.separator(height=20)
        add_button = cmds.button(label='Add', command=self.add_command)
        apply_button = cmds.button(label='Apply', command=self.apply_command)
        close_button = cmds.button(label='Close', command=self.close_window)

        cmds.formLayout(self.main_layout, edit=True,

                        attachForm=[(bottom_separator, 'bottom', 30),
                                    (bottom_separator, 'left', 5), (bottom_separator, 'right', 5),
                                    (add_button, 'bottom', 5), (add_button, 'left', 5),
                                    (apply_button, 'bottom', 5),
                                    (close_button, 'bottom', 5), (close_button, 'right', 5)],

                        attachControl=[(add_button, 'top', 0, bottom_separator),
                                       (apply_button, 'top', 0, bottom_separator),
                                       (close_button, 'top', 0, bottom_separator),

                                       (apply_button, 'left', 5, add_button),
                                       (apply_button, 'right', 5, close_button)],

                        attachPosition=[(add_button, 'right', 0, 33),
                                        (close_button, 'left', 0, 66)]
                        )

    def open_window(self):
        """
        open a window with the settings given
        """
        if cmds.window(self.window, exists=True):
            cmds.windowPref(self.window, remove=True)

        self.window = cmds.window(self.window, title=self.title, widthHeight=self.size, sizeable=False,
                                  minimizeButton=True, maximizeButton=False)

        return self.window

    def add_command(self, *args):
        """
        Add button command
        """
        self.apply_command()
        self.close_window()

    def apply_command(self, *args):
        """
        Apply button command
        """
        cmds.warning('{} need an Apply Command'.format(self.title))

    def close_window(self, *args):
        """
        Close button command
        """
        cmds.deleteUI(self.window, window=True)
        cmds.windowPref(self.window, remove=True)
