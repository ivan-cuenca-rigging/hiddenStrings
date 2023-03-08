# Maya imports
from maya import cmds

# Project imports
from hiddenStrings.libs.helpers import windowHelper


class RenamerWindow(windowHelper.WindowHelper):
    def __init__(self, *args):
        """
        Create the renamer window
        :param title: str, title of the window
        :param size: list, width and height
        """
        super().__init__(title='Renamer', size=(300, 210))

        # Search and replace
        self.search_for = cmds.textFieldGrp(label='Search for: ', columnWidth=[(1, 70), (2, 217)],
                                            columnAlign=(1, 'left'))
        self.replace_with = cmds.textFieldGrp(label='Replace with: ', columnWidth=[(1, 70), (2, 217)],
                                              columnAlign=(1, 'left'))
        self.replace_button = cmds.button(label='Replace', command=self.search_and_replace_command)
        separator01 = cmds.separator(height=5)

        # Rename
        prefix_text = cmds.text(label='Prefix')
        self.prefix = cmds.textFieldGrp(columnWidth=(1, 65), columnAlign=(1, 'left'))
        rename_text = cmds.text(label='Rename')
        self.rename = cmds.textFieldGrp(columnWidth=(1, 100), columnAlign=(1, 'left'))
        increment_text = cmds.text(label='Increment')
        self.increment = cmds.textFieldGrp(columnWidth=(1, 42), columnAlign=(1, 'left'))
        suffix_text = cmds.text(label='Suffix')
        self.suffix = cmds.textFieldGrp(columnWidth=(1, 65), columnAlign=(1, 'left'))

        self.rename_button = cmds.button(label='Rename', command=self.rename_command)

        # Clean
        separator02 = cmds.separator(height=5)
        self.clean_button = cmds.button(label='Clean', command=self.clean_command)

        # --------------------------------------------------------------------------------------------------------------
        cmds.formLayout(self.main_layout, edit=True,
                        attachForm=[(self.search_for, 'top', 5),
                                    (self.search_for, 'left', 5),
                                    (self.replace_with, 'left', 5),
                                    (self.replace_button, 'left', 5),
                                    (self.replace_button, 'right', 5),
                                    (self.prefix, 'left', 5),
                                    (prefix_text, 'left', 25),
                                    (self.rename_button, 'left', 5),
                                    (self.rename_button, 'right', 5),
                                    (self.clean_button, 'left', 5),
                                    (self.clean_button, 'right', 5),
                                    (separator01, 'left', 5),
                                    (separator01, 'right', 5),
                                    (separator02, 'left', 5),
                                    (separator02, 'right', 5)],

                        attachControl=[(self.replace_with, 'top', 5, self.search_for),
                                       (self.replace_button, 'top', 5, self.replace_with),
                                       (separator01, 'top', 5, self.replace_button),

                                       (prefix_text, 'top', 5, separator01),
                                       (rename_text, 'top', 5, separator01),
                                       (rename_text, 'left', 55, prefix_text),
                                       (increment_text, 'top', 5, separator01),
                                       (increment_text, 'left', 30, rename_text),
                                       (suffix_text, 'top', 5, separator01),
                                       (suffix_text, 'left', 18, increment_text),

                                       (self.prefix, 'top', 5, prefix_text),
                                       (self.rename, 'top', 5, prefix_text),
                                       (self.rename, 'left', 0, self.prefix),
                                       (self.increment, 'top', 5, prefix_text),
                                       (self.increment, 'left', 0, self.rename),
                                       (self.suffix, 'top', 5, prefix_text),
                                       (self.suffix, 'left', 0, self.increment),
                                       (self.rename_button, 'top', 5, self.rename),
                                       (separator02, 'top', 5, self.rename_button),
                                       (self.clean_button, 'top', 5, separator02)])

    def bottom_layout(self, *args):
        """
        Override bottom layout
        """
        pass

    def search_and_replace_command(self, *args):
        """
        Search and replace names of the nodes selected
        """
        selection_list = cmds.ls(selection=True, allPaths=True)

        for node in selection_list:
            cmds.rename(node, node.split('|')[-1].replace(cmds.textFieldGrp(self.search_for, query=True, text=True),
                                                          cmds.textFieldGrp(self.replace_with, query=True, text=True)))

    def rename_command(self, *args):
        """
        Rename nodes selected
        """
        selection_list = cmds.ls(selection=True, allPaths=True)

        rename = cmds.textFieldGrp(self.rename, query=True, text=True)
        prefix = cmds.textFieldGrp(self.prefix, query=True, text=True)
        suffix = cmds.textFieldGrp(self.suffix, query=True, text=True)
        increment = cmds.textFieldGrp(self.increment, query=True, text=True)

        for node in selection_list:
            if rename:
                node = cmds.rename(node, cmds.textFieldGrp(self.rename, query=True, text=True))

            if increment:
                print(increment)
                node = cmds.rename(node, '{}{}'.format(node, increment))
                increment = self.increment_string(increment)
            if prefix:
                node = cmds.rename(node, '{}{}'.format(prefix, node.split('|')[-1]))

            if suffix:
                cmds.rename(node, '{}{}'.format(node.split('|')[-1], suffix))

    def clean_command(self, *args):
        """
        Clean all fields of the window
        """
        cmds.textFieldGrp(self.search_for, edit=True, text='')
        cmds.textFieldGrp(self.replace_with, edit=True, text='')
        cmds.textFieldGrp(self.rename, edit=True, text='')
        cmds.textFieldGrp(self.prefix, edit=True, text='')
        cmds.textFieldGrp(self.suffix, edit=True, text='')
        cmds.textFieldGrp(self.increment, edit=True, text='')

    @staticmethod
    def increment_character(character):
        return chr(ord(character) + 1) if character != 'Z' else 'A'

    def increment_string(self, string_character):
        if string_character.isdigit():
            new_string = str(int(string_character) + 1).zfill(len(string_character))
        else:
            last_part = string_character.rstrip('Z')
            num_replacements = len(string_character) - len(last_part)
            new_string = last_part[:-1] + self.increment_character(last_part[-1]) if last_part else 'A'
            new_string += 'A' * num_replacements
        return new_string

