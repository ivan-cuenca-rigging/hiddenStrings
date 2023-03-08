# Imports
import hiddenStrings
import os
from functools import partial

# Maya imports
from maya import cmds

# Project imports
from hiddenStrings.libs import shapeLib, jsonLib, sideLib, usageLib
from hiddenStrings.libs.helpers import windowHelper


class ShapeManagerWindow(windowHelper.WindowHelper):
    def __init__(self, *args):
        """
        Create the Shape manager window
        :param title: str, title of the window
        :param size: list, width and height
        """
        super().__init__(title='Shape Manager', size=(450, 500))

        self.shapes_path = r'{}\libs\shapes'.format(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

        # Shapes layout
        self.shape_name = cmds.textFieldGrp(label='Shape name:')

        self.shapes_layout = cmds.scrollLayout(width=375, height=250, backgroundColor=(0.2, 0.2, 0.2))
        self.shapes_items_layout()

        self.delete_button = cmds.button(label='Delete', width=100, command=self.delete_shape_command)
        self.merge_button = cmds.button(label='Merge', width=100, command=self.merge_shape_command)
        self.export_button = cmds.button(label='Export', width=100, command=self.export_shape_command)

        # Color override layout
        self.color_override_layout = self.color_override_items_layout()
        self.default_color = cmds.button(label='Default', width=375,
                                         command=partial(shapeLib.override_color, color_key='default'))

        # --------------------------------------------------------------------------------------------------------------
        cmds.formLayout(self.main_layout, edit=True,
                        attachForm=[(self.shape_name, 'top', 20),
                                    (self.shapes_layout, 'left', 37.5),
                                    (self.delete_button, 'left', 39),
                                    (self.export_button, 'right', 39),
                                    (self.color_override_layout, 'left', 39),
                                    (self.default_color, 'left', 37.5)],

                        attachControl=[(self.shapes_layout, 'top', 10, self.shape_name),
                                       (self.delete_button, 'top', 2.5, self.shapes_layout),
                                       (self.merge_button, 'top', 2.5, self.shapes_layout),
                                       (self.merge_button, 'left', 30, self.delete_button),
                                       (self.merge_button, 'right', 30, self.export_button),
                                       (self.export_button, 'top', 2.5, self.shapes_layout),
                                       (self.color_override_layout, 'top', 10, self.export_button),
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
            shape_path = r'{}\images\{}'.format(self.shapes_path, shape.replace('.json', '.png'))
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
                        command=partial(shapeLib.override_color, color_key=index))

        cmds.setParent('..')

        return color_override_layout

    def import_shape(self, shape_name):
        """
        If there is not a selection import the shape
        If there is a selection replace the shape
        :param shape_name: str
        """
        node = cmds.ls(selection=True)
        shape_data = jsonLib.import_data_from_json(file_name=shape_name, file_path=self.shapes_path,
                                                   relative_path=False)
        shape_imported = shapeLib.create_spl_from_data(spl_name=shape_name, spl_data=shape_data)
        if len(node) == 0:
            cmds.select(shape_imported)
        else:
            node = node[0]
            cmds.xform(shape_imported, worldSpace=True,
                       matrix=cmds.xform(node, query=True, worldSpace=True, matrix=True))

            node_temporal_name = cmds.rename(node, '{}_{}_{}'.format(shape_name, sideLib.center, usageLib.spline))
            shapeLib.replace_shape(node=node_temporal_name,
                                   shape_transform=shape_imported)
            cmds.rename(node_temporal_name, node)
            cmds.select(node)

        cmds.textFieldGrp(self.shape_name, edit=True, text=shape_name)

    def delete_shape_command(self, *args):
        """
        Delete shape name from folder (data and image)
        """
        shape_name = cmds.textFieldGrp(self.shape_name, query=True, text=True)

        self.is_shape_overwrite_locked(shape_name)

        # Delete shape data
        if os.path.exists(r'{}\{}.json'.format(self.shapes_path, shape_name)):
            os.remove(r'{}\{}.json'.format(self.shapes_path, shape_name))

        # Delete shape image
        if os.path.exists(r'{}\images\{}.png'.format(self.shapes_path, shape_name)):
            os.remove(r'{}\images\{}.png'.format(self.shapes_path, shape_name))

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
        for sel in selection_list[1:]:
            node_temporal_name = cmds.rename(node, 'temp_{}_{}'.format(sideLib.center, usageLib.spline))
            shapeLib.replace_shape(node=node_temporal_name, shape_transform=sel, keep_shapes=True)
            node = cmds.rename(node_temporal_name, node)
        cmds.select(node)

    def save_screenshot(self, *args):
        path = r'{}\libs\shapes\images'.format(hiddenStrings.hidden_strings_path)
        shape_name = cmds.textFieldGrp(self.shape_name, query=True, text=True)

        path_with_file = r'{}\{}.png'.format(path, shape_name)

        cmds.viewFit()
        cmds.setAttr('defaultRenderGlobals.imageFormat', 8)

        cmds.playblast(completeFilename=path_with_file, forceOverwrite=True, format='image', width=200, height=200,
                       showOrnaments=False, startTime=1, endTime=1, viewer=False)

    def export_shape_command(self, *args):
        """
        Export selected spline data to a JSON
        """
        shape_name = cmds.textFieldGrp(self.shape_name, query=True, text=True)
        self.is_shape_overwrite_locked(shape_name)
        shape_data = shapeLib.get_spl_data(spl=cmds.ls(selection=True)[0])

        spline_name = cmds.ls(selection=True)[0]
        cmds.rename(spline_name, '{}_{}_{}'.format(shape_name, sideLib.center, usageLib.spline))

        jsonLib.export_data_to_json(data=shape_data,
                                    file_name=shape_name,
                                    file_path=self.shapes_path,
                                    relative_path=False)
        self.save_screenshot()
        cmds.rename('{}_{}_{}'.format(shape_name, sideLib.center, usageLib.spline), spline_name)
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
    def is_shape_overwrite_locked(shape_name, *args):
        """
        Check if the spline shape can be overwritten or not, builder splines are locked
        :param shape_name: str
        """
        shapes_locked_list = ['circle',
                              'cube',
                              'general',
                              'fourArrows',
                              'lollipop',
                              'lollipop2',
                              'sphere']

        if shape_name in shapes_locked_list:
            cmds.error('This shape cannot be overwritten or deleted.')


