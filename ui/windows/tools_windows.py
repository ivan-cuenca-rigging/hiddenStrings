# Imports
import os
from functools import partial

# Maya imports
from maya import cmds

# Project imports
from hiddenStrings import module_utils
from hiddenStrings.libs import window_lib, spline_lib, side_lib, usage_lib, import_export_lib, blend_shape_lib


class RenamerWindow(window_lib.Helper):
    def __init__(self, *args):
        """
        Create the renamer window
        :param title: str, title of the window
        :param size: list, width and height
        """
        super(RenamerWindow, self).__init__(title='Renamer', size=(300, 210))

        # Search and replace
        self.search_for = cmds.textFieldGrp(label='Search for: ', columnWidth=[(1, 70), (2, 217)],
                                            columnAlign=(1, 'left'))
        self.replace_with = cmds.textFieldGrp(label='Replace with: ', columnWidth=[(1, 70), (2, 217)],
                                              columnAlign=(1, 'left'))

        self.replace_button = cmds.button(label='Replace', width=142,
                                          command=self.search_and_replace_command)

        self.replace_with_hierarchy_button = cmds.button(label='Replace with hierarchy', width=142,
                                                         command=self.search_and_replace_with_hierarchy_command)

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
                                    (self.replace_with_hierarchy_button, 'right', 5),
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
                                       (self.replace_with_hierarchy_button, 'top', 5, self.replace_with),
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

    def search_and_replace(self, node):
        """
        Search and replace name
        """
        node = cmds.ls(node, allPaths=True)[0]

        cmds.rename(node, node.split('|')[-1].replace(cmds.textFieldGrp(self.search_for, query=True, text=True),
                                                      cmds.textFieldGrp(self.replace_with, query=True, text=True)))

    def search_and_replace_command(self, *args):
        """
        Search and replace names of the nodes selected
        """
        selection_list = cmds.ls(selection=True, uuid=True)

        # Search adn replace
        for node in selection_list:
            self.search_and_replace(node)

        # Search and replace blendShapes
        if blend_shape_lib.get_blend_shapes_from_shape_editor():
            for blend_shape in blend_shape_lib.get_blend_shapes_from_shape_editor():
                cmds.rename(blend_shape,
                            blend_shape.replace(cmds.textFieldGrp(self.search_for, query=True, text=True),
                                                cmds.textFieldGrp(self.replace_with, query=True, text=True)))

        # Search and replace targets of blendShapes
        if blend_shape_lib.get_targets_from_shape_editor():
            for blend_shape_and_target in blend_shape_lib.get_targets_from_shape_editor(as_index=False):
                blend_shape, target = blend_shape_and_target.split('.')
                blend_shape_lib.rename_target(blend_shape=blend_shape, target=target,
                                              new_name=target.replace(
                                                  cmds.textFieldGrp(self.search_for, query=True, text=True),
                                                  cmds.textFieldGrp(self.replace_with, query=True, text=True)))

    def search_and_replace_with_hierarchy_command(self, *args):
        """
        Search and replace names of the nodes selected with hierarchy
        """
        selection_list = [cmds.listRelatives(x, allDescendents=True, shapes=False, path=True)
                          for x in cmds.ls(selection=True, allPaths=True)][0]
        selection_list = [cmds.ls(x, uuid=True)[0] for x in selection_list]
        selection_list += (cmds.ls(selection=True, uuid=True))

        for node in selection_list:
            self.search_and_replace(node)

    def rename_command(self, *args):
        """
        Rename nodes selected
        """
        selection_list = cmds.ls(selection=True, uuid=True)

        rename = cmds.textFieldGrp(self.rename, query=True, text=True)
        prefix = cmds.textFieldGrp(self.prefix, query=True, text=True)
        suffix = cmds.textFieldGrp(self.suffix, query=True, text=True)
        increment = cmds.textFieldGrp(self.increment, query=True, text=True)

        for node in selection_list:
            node = cmds.ls(node, allPaths=True)[0]
            if rename:
                node = cmds.rename(node, cmds.textFieldGrp(self.rename, query=True, text=True))

            if increment:
                node = cmds.rename(node, '{}{}'.format(node, increment))
                increment = self.increment_string(increment)

            if prefix:
                node = cmds.rename(node, '{}{}'.format(prefix, node.split('|')[-1]))

            if suffix:
                cmds.rename(node, '{}{}'.format(node.split('|')[-1], suffix))

        # rename blendShapes
        if blend_shape_lib.get_blend_shapes_from_shape_editor():
            for blend_shape in blend_shape_lib.get_blend_shapes_from_shape_editor():
                if rename:
                    blend_shape = cmds.rename(blend_shape, cmds.textFieldGrp(self.rename, query=True, text=True))

                if increment:
                    blend_shape = cmds.rename(
                        blend_shape, "{}{}".format(blend_shape, increment)
                    )
                    increment = self.increment_string(increment)

                if prefix:
                    blend_shape = cmds.rename(
                        blend_shape, "{}{}".format(prefix, blend_shape.split("|")[-1])
                    )

                if suffix:
                    cmds.rename(
                        blend_shape, "{}{}".format(blend_shape.split("|")[-1], suffix)
                    )

        # rename targets of blendShapes
        if blend_shape_lib.get_targets_from_shape_editor():
            for blend_shape_and_target in blend_shape_lib.get_targets_from_shape_editor(as_index=False):
                blend_shape, target = blend_shape_and_target.split(".")
                if rename:
                    target = blend_shape_lib.rename_target(
                        blend_shape=blend_shape,
                        target=target,
                        new_name=cmds.textFieldGrp(self.rename, query=True, text=True)
                    )

                if increment:
                    target = blend_shape_lib.rename_target(
                        blend_shape=blend_shape,
                        target=target,
                        new_name="{}{}".format(target, increment)
                    )
                    increment = self.increment_string(increment)

                if prefix:
                    target = blend_shape_lib.rename_target(
                        blend_shape=blend_shape,
                        target=target,
                        new_name="{}{}".format(prefix, target.split("|")[-1]))

                if suffix:
                    target = blend_shape_lib.rename_target(
                        blend_shape=blend_shape,
                        target=target,
                        new_name="{}{}".format(target.split("|")[-1], suffix),
                    )

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


class ShapeManagerWindow(window_lib.Helper):
    def __init__(self, *args):
        """
        Create the Shape manager window
        :param title: str, title of the window
        :param size: list, width and height
        """
        super(ShapeManagerWindow, self).__init__(title='Shape Manager', size=(450, 510))

        self.shapes_path = r'{}/libs/spline_shapes'.format(module_utils.hidden_strings_path)

        # Shapes layout
        self.export_name = cmds.textFieldGrp(label='Export name: ', columnWidth=[(1, 70), (2, 170)])

        self.delete_button = cmds.button(label='Delete', width=100, command=self.delete_shape_command)

        self.export_button = cmds.button(label='Export', width=100, command=self.export_shape_command)

        self.shapes_layout = cmds.scrollLayout(width=375, height=250, backgroundColor=(0.2, 0.2, 0.2))
        self.shapes_items_layout()

        self.merge_button = cmds.button(label='Merge', width=100, command=self.merge_shape_command)

        self.transfer_button = cmds.button(label='Transfer', width=100, command=self.transfer_spline_command)

        # Color override layout
        self.color_override_layout = self.color_override_items_layout()
        self.default_color = cmds.button(label='Default', width=375,
                                         command=partial(spline_lib.set_override_color, color_key='default'))

        # --------------------------------------------------------------------------------------------------------------
        cmds.formLayout(self.main_layout, edit=True,
                        attachForm=[(self.export_name, 'top', 20),
                                    (self.export_name, 'left', 37.5),
                                    (self.export_button, 'top', 10),
                                    (self.export_button, 'right', 39),
                                    (self.delete_button, 'right', 39),
                                    (self.shapes_layout, 'left', 37.5),
                                    (self.merge_button, 'left', 39),
                                    (self.transfer_button, 'right', 39),
                                    (self.color_override_layout, 'left', 39),
                                    (self.default_color, 'left', 37.5)],

                        attachControl=[(self.export_button, 'left', 10, self.export_name),
                                       (self.delete_button, 'top', 5, self.export_button),
                                       (self.delete_button, 'left', 10, self.export_name),
                                       (self.shapes_layout, 'top', 25, self.export_name),
                                       (self.merge_button, 'top', 7.5, self.shapes_layout),
                                       (self.transfer_button, 'top', 7.5, self.shapes_layout),
                                       (self.color_override_layout, 'top', 10, self.merge_button),
                                       (self.default_color, 'top', 10, self.color_override_layout)])

    def bottom_layout(self, *args):
        """
        Override bottom layout
        """
        pass

    def shapes_items_layout(self, *args):
        """
        shapes layout
        """
        cmds.setParent(self.shapes_layout)

        file_list = [x for x in os.listdir(self.shapes_path) if x.endswith('.json')]

        items_layout = cmds.rowColumnLayout(numberOfColumns=5)
        for shape in file_list:
            cmds.rowColumnLayout(numberOfRows=2)
            shape_path = r'{}/images/{}'.format(self.shapes_path, shape.replace('.json', '.png'))
            cmds.iconTextButton(style='iconOnly',
                                image=shape_path,
                                width=69, height=69,
                                command=partial(self.import_shape, shape.split('.')[0]))
            cmds.text(shape.split('.')[0])
            cmds.setParent(items_layout)

        cmds.setParent(self.main_layout)

    def color_override_items_layout(self, *args):
        """
        Color override layout
        """
        color_override_layout = cmds.gridLayout(self.main_layout,
                                                numberOfRowsColumns=(3, 10), cellWidthHeight=(37.5, 37.5))

        for index in range(2, 32):  # Color index
            color_component = cmds.colorIndex(index, query=True)

            cmds.button(label='',
                        backgroundColor=(color_component[0], color_component[1], color_component[2]),
                        command=partial(spline_lib.set_override_color, color_key=index))

        cmds.setParent('..')

        return color_override_layout

    def import_shape(self, export_name):
        """
        If there is not a selection import the shape
        If there is a selection replace the shape
        :param export_name: str
        """
        node = cmds.ls(selection=True)

        shape_data = import_export_lib.import_data_from_json(file_name=export_name,
                                                             file_path=self.shapes_path,
                                                             relative_path=False)
        shape_imported = spline_lib.create_spl_from_data(spl_name=export_name, spl_data=shape_data)

        if len(node) == 0:
            cmds.select(shape_imported)
        else:
            node = node[0]

            # Get spline color
            spline_color = spline_lib.get_override_color(node)

            cmds.xform(shape_imported, worldSpace=True,
                       matrix=cmds.xform(node, query=True, worldSpace=True, matrix=True))

            node_temporal_name = cmds.rename(node, '{}_{}_{}'.format(export_name, side_lib.center, usage_lib.spline))
            spline_lib.replace_shape(node=node_temporal_name,
                                     shape_transform=shape_imported)
            cmds.rename(node_temporal_name, node)

            if spline_color:
                spline_lib.set_override_color(splines_list=[node], color_key=spline_color)

            cmds.select(node)

    def delete_shape_command(self, *args):
        """
        Delete shape name from folder (data and image)
        """
        export_name = cmds.textFieldGrp(self.export_name, query=True, text=True)

        self.is_shape_overwrite_locked(export_name)

        # Delete shape data
        if os.path.exists(r'{}/{}.json'.format(self.shapes_path, export_name)):
            os.remove(r'{}/{}.json'.format(self.shapes_path, export_name))
            # Delete shape image
            if os.path.exists(r'{}/images/{}.png'.format(self.shapes_path, export_name)):
                os.remove(r'{}/images/{}.png'.format(self.shapes_path, export_name))
        else:
            cmds.error('{} does not exists in the library'.format(export_name))

        self.refresh_shapes()

    @staticmethod
    def merge_shape_command(*args):
        """
        Merge all selected shapes into the first
        """
        selection_list = cmds.ls(selection=True)
        if len(selection_list) == 0 or not all(cmds.objectType(x) == 'transform' for x in selection_list):
            cmds.error('select two or more shapes')

        node = selection_list[0]
        for sel in selection_list:
            if sel != node:
                spline_lib.replace_shape(node=node, shape_transform=sel, keep_shapes=True)

        cmds.select(node)

    @staticmethod
    def transfer_spline_command(*args):
        """
        Transfer spline from source(selection 0) to target (selection 1)
        """
        selection_list = cmds.ls(selection=True)

        for node in selection_list:
            if node != selection_list[0]:
                spline_lib.transfer_shape(source=selection_list[0], target=node)

    def save_screenshot(self, *args):
        path = r'{}/images'.format(self.shapes_path)
        export_name = cmds.textFieldGrp(self.export_name, query=True, text=True)

        path_with_file = r'{}/{}.png'.format(path, export_name)

        cmds.viewFit()
        cmds.setAttr('defaultRenderGlobals.imageFormat', 8)

        cmds.playblast(completeFilename=path_with_file, forceOverwrite=True, format='image', width=200, height=200,
                       showOrnaments=False, startTime=1, endTime=1, viewer=False)

    def export_shape_command(self, *args):
        """
        Export selected spline data to a JSON
        """
        export_name = cmds.textFieldGrp(self.export_name, query=True, text=True)
        self.is_shape_overwrite_locked(export_name)
        shape_data = spline_lib.get_spl_data(spl=cmds.ls(selection=True)[0])

        spline_name = cmds.ls(selection=True)[0]
        cmds.rename(spline_name, '{}_{}_{}'.format(export_name, side_lib.center, usage_lib.spline))

        import_export_lib.export_data_to_json(data=shape_data,
                                              file_name=export_name,
                                              file_path=self.shapes_path,
                                              relative_path=False)
        self.save_screenshot()
        cmds.rename('{}_{}_{}'.format(export_name, side_lib.center, usage_lib.spline), spline_name)
        self.refresh_shapes()

    def refresh_shapes(self, *args):
        """
        Delete de shapes layout children and rebuilt it
        """
        shapes_layout_children = cmds.layout(self.shapes_layout, query=True, childArray=True)

        for child in shapes_layout_children:
            cmds.deleteUI(child)

        self.shapes_items_layout()

    @staticmethod
    def is_shape_overwrite_locked(export_name, *args):
        """
        Check if the spline shape can be overwritten or not, builder splines are locked
        :param export_name: str
        """
        shapes_locked_list = ['circle',
                              'cube',
                              'general',
                              'fourArrows',
                              'lollipop',
                              'lollipop02',
                              'sphere']

        if export_name in shapes_locked_list:
            cmds.error('This shape cannot be overwritten or deleted.')
