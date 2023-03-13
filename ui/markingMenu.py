# Imports
import importlib
import os
from functools import partial

# Maya imports
from maya import cmds

# Project imports
import hiddenStrings
from hiddenStrings.libs import guideLib, blendShapeLib, connectionLib, skinLib, importExportLib
from hiddenStrings.ui.blendShapesWindows import importBlendShapeWindow, exportBlendShapeWindow
from hiddenStrings.ui.connectionWindows import (connectOffsetParentMatrixWindow, connectTranslateRotateScaleWindow,
                                                connectTranslateWindow, connectRotateWindow, connectScaleWindow)
from hiddenStrings.ui.skinsWindows import importSkinWindow, exportSkinWindow, transferSkinWindow
from hiddenStrings.ui.toolsWindows import shapeManagerWindow, renamerWindow

builder_exists = os.path.exists(r'{}\builder'.format(os.path.dirname(os.path.dirname(__file__))))

if builder_exists:
    from hiddenStrings.builder.modules.body import column, leg, root, arm, neck
    from hiddenStrings.ui.bodyWindows import (rootWindow,
                                              neckWindow, spineWindow,
                                              legWindow, armWindow)


class MarkingMenu(object):
    def __init__(self, click_input):
        self.menu_name = "hiddenStrings"
        self.icon_path = r'{}//icons//hiddenStrings_white.png'.format(os.path.dirname(os.path.dirname(__file__)))

        self.click_input = click_input

        self.delete()
        self.build()

    def build(self, *args):
        """
        Build marking menu
        """
        self.delete()

        cmds.popupMenu(self.menu_name, markingMenu=True, allowOptionBoxes=True, parent="viewPanes",
                       button=self.click_input,
                       ctrlModifier=False,
                       altModifier=True,
                       shiftModifier=True)

        self.marking_menu_config()

    def delete(self):
        """
        Delete marking menu
        """
        if cmds.popupMenu(self.menu_name, exists=True):
            cmds.deleteUI(self.menu_name)

    def marking_menu_config(self):
        """
        Create the marking menu items
        """
        # ---------- North ----------
        self.blend_shapes_menu(menu_parent=self.menu_name, radial_position='N')

        # ---------- North-West ----------
        self.skins_menu(menu_parent=self.menu_name, radial_position='NW')

        # ---------- West ----------
        self.connections_menu(menu_parent=self.menu_name, radial_position='W')

        # ---------- South ----------
        self.maya_editors_menu(menu_parent=self.menu_name, radial_position='S')

        # ---------- South List ----------
        cmds.menuItem(parent=self.menu_name, label='                Tools', enable=False)
        cmds.menuItem(parent=self.menu_name, divider=True)

        cmds.menuItem(parent=self.menu_name, label='Save selection', command=importExportLib.export_selection)
        cmds.menuItem(parent=self.menu_name, label='Load selection', command=importExportLib.import_selection)

        cmds.menuItem(parent=self.menu_name, divider=True)

        cmds.menuItem(parent=self.menu_name, label='Renamer', command=renamerWindow.RenamerWindow)

        cmds.menuItem(parent=self.menu_name, label='Shape manager', command=shapeManagerWindow.ShapeManagerWindow)

        local_rotation_axis_hierarchy = cmds.menuItem(parent=self.menu_name, label='Local rotation axis', subMenu=True)

        cmds.menuItem(parent=local_rotation_axis_hierarchy, label='Show',
                      command=self.show_local_rotation_axis)
        cmds.menuItem(parent=local_rotation_axis_hierarchy, label='Show with hierarchy',
                      command=partial(self.show_local_rotation_axis, hierarchy=True))

        cmds.menuItem(parent=local_rotation_axis_hierarchy, divider=True)

        cmds.menuItem(parent=local_rotation_axis_hierarchy, label='Hide',
                      command=self.hide_local_rotation_axis)
        cmds.menuItem(parent=local_rotation_axis_hierarchy, label='Hide with hierarchy',
                      command=partial(self.hide_local_rotation_axis, hierarchy=True))

        cmds.menuItem(parent=self.menu_name, divider=True)
        cmds.menuItem(parent=self.menu_name, label='          Module utils', enable=False)
        cmds.menuItem(parent=self.menu_name, divider=True)

        cmds.menuItem(parent=self.menu_name, label='     Reload hiddenStrings',
                      image=self.icon_path, command=hiddenStrings.reload)

        # ---------- East ----------
        if builder_exists:
            self.builder_menu()

    def blend_shapes_menu(self, menu_parent, radial_position):
        """
        Create the shapes menu items
        """
        blend_shape_menu = cmds.menuItem(parent=menu_parent, label='BlendShapes', radialPosition=radial_position,
                                         subMenu=True)

        cmds.menuItem(parent=blend_shape_menu, label='Shape Editor', radialPosition='N',
                      command=cmds.ShapeEditor)

        cmds.menuItem(parent=blend_shape_menu, label='             blendShapes Utils', enable=False)
        cmds.menuItem(parent=blend_shape_menu, divider=True)

        cmds.menuItem(parent=blend_shape_menu, label='Edit Blendshape / In-Between',
                      command=blendShapeLib.edit_target_or_in_between)

        cmds.menuItem(parent=blend_shape_menu, label='Sculpt tool',
                      command=self.set_mesh_bulge_tool)

        cmds.menuItem(parent=blend_shape_menu, divider=True)

        cmds.menuItem(parent=blend_shape_menu, label='Rename all blendShapes',
                      command=self.rename_all_blend_shapes)

        cmds.menuItem(parent=blend_shape_menu, divider=True)

        cmds.menuItem(parent=blend_shape_menu, label='Trigger', enable=False)
        cmds.menuItem(parent=blend_shape_menu, label='Copy target connection',
                      command=blendShapeLib.copy_target_connection)

        cmds.menuItem(parent=blend_shape_menu, divider=True)

        cmds.menuItem(parent=blend_shape_menu, label='Import BlendShapes',
                      command=importBlendShapeWindow.ImportBlendShapeWindow)
        cmds.menuItem(parent=blend_shape_menu, label='Export BlendShapes',
                      command=exportBlendShapeWindow.ExportBlendShapeWindow)

        cmds.menuItem(parent=blend_shape_menu, divider=True)

        cmds.menuItem(parent=blend_shape_menu, label='Import BlendShapes connections', enable=False)
        cmds.menuItem(parent=blend_shape_menu, label='Export BlendShapes connections', enable=False)

    def skins_menu(self, menu_parent, radial_position):
        """
        Create the skins menu items
        """
        skin_menu = cmds.menuItem(parent=menu_parent, label='Skins', radialPosition=radial_position,
                                  subMenu=True)

        cmds.menuItem(parent=skin_menu, label='Paint Skin Weights', radialPosition='NW',
                      command=cmds.ArtPaintSkinWeightsToolOptions)

        cmds.menuItem(parent=skin_menu, label='             Skins Utils             ', enable=False)
        cmds.menuItem(parent=skin_menu, divider=True)

        cmds.menuItem(parent=skin_menu, label='Set Labels',
                      command=self.set_labels)

        cmds.menuItem(parent=skin_menu, label='Rename all skinClusters',
                      command=self.rename_all_skin_clusters)

        cmds.menuItem(parent=skin_menu, divider=True)

        cmds.menuItem(parent=skin_menu, label='Push joint',
                      enable=False)

        cmds.menuItem(parent=skin_menu, divider=True)

        cmds.menuItem(parent=skin_menu, label='Transfer Skin',
                      command=self.transfer_skin)
        cmds.menuItem(parent=skin_menu, optionBox=True,
                      command=transferSkinWindow.TransferSkinWindow)

        cmds.menuItem(parent=skin_menu, divider=True)

        cmds.menuItem(parent=skin_menu, label='Import Skins', command=importSkinWindow.ImportSkinWindow)
        cmds.menuItem(parent=skin_menu, label='Export Skins', command=exportSkinWindow.ExportSkinWindow)

    def connections_menu(self, menu_parent, radial_position):
        """
        Create the connection menu items
        """
        connections_menu = cmds.menuItem(parent=menu_parent, label='Connections', radialPosition=radial_position,
                                         subMenu=True)

        cmds.menuItem(parent=connections_menu, label='Connection Editor', radialPosition='W',
                      command=cmds.ConnectionEditor)

        cmds.menuItem(parent=connections_menu, label='           Connections Utils', enable=False)

        cmds.menuItem(parent=connections_menu, divider=True)

        cmds.menuItem(parent=connections_menu, label='Connect Translate Rotate Scale',
                      command=self.connect_translate_rotate_scale)
        cmds.menuItem(parent=connections_menu, optionBox=True,
                      command=connectTranslateRotateScaleWindow.ConnectTranslateRotateScaleWindow)

        cmds.menuItem(parent=connections_menu, label='Connect Translate',
                      command=self.connect_translate)
        cmds.menuItem(parent=connections_menu, optionBox=True,
                      command=connectTranslateWindow.ConnectTranslateWindow)

        cmds.menuItem(parent=connections_menu, label='Connect Rotate',
                      command=self.connect_rotate)
        cmds.menuItem(parent=connections_menu, optionBox=True,
                      command=connectRotateWindow.ConnectRotateWindow)

        cmds.menuItem(parent=connections_menu, label='Connect Scale',
                      command=self.connect_scale)
        cmds.menuItem(parent=connections_menu, optionBox=True,
                      command=connectScaleWindow.ConnectScaleWindow)

        cmds.menuItem(parent=connections_menu, divider=True)
        cmds.menuItem(parent=connections_menu, label='                   Matrices', enable=False)
        cmds.menuItem(parent=connections_menu, divider=True)

        cmds.menuItem(parent=connections_menu, label='Connect OffsetParentMatrix',
                      command=self.connect_offset_parent_matrix)
        cmds.menuItem(parent=connections_menu, optionBox=True,
                      command=connectOffsetParentMatrixWindow.ConnectOffsetParentMatrixWindow)

        cmds.menuItem(parent=connections_menu, label='Transform to offsetParentMatrix',
                      command=connectionLib.transform_to_offset_parent_matrix)

        cmds.menuItem(parent=connections_menu, label='offsetParentMatrix to transform',
                      command=connectionLib.offset_parent_matrix_to_transform)

    @staticmethod
    def maya_editors_menu(menu_parent, radial_position):
        """
        Create the maya editors menu items
        """
        maya_editors_menu = cmds.menuItem(parent=menu_parent, label='Maya editors', radialPosition=radial_position,
                                          subMenu=True)

        cmds.menuItem(parent=maya_editors_menu, label='Shape Editor', radialPosition='N',
                      command=cmds.ShapeEditor)

        cmds.menuItem(parent=maya_editors_menu, label='Paint Skin Weights', radialPosition='NW',
                      command=cmds.ArtPaintSkinWeightsToolOptions)

        cmds.menuItem(parent=maya_editors_menu, label='Connection Editor', radialPosition='W',
                      command=cmds.ConnectionEditor)

        cmds.menuItem(parent=maya_editors_menu, label='Graph Editor', radialPosition='E',
                      command=cmds.GraphEditor)

        cmds.menuItem(parent=maya_editors_menu, label='Reference Editor', radialPosition='NE',
                      command=cmds.ReferenceEditor)

        cmds.menuItem(parent=maya_editors_menu, label='Component Editor', radialPosition='SW',
                      command=cmds.ComponentEditor)

        cmds.menuItem(parent=maya_editors_menu, label='Set Driven Key Editor', radialPosition='SE',
                      command=cmds.SetDrivenKey)

        cmds.menuItem(parent=maya_editors_menu, label='Node Editor', radialPosition='S',
                      command=cmds.NodeEditorWindow)

    # ---------- methods ----------
    @staticmethod
    def set_labels(*args):
        """
        Set joints labelling
        """
        skinLib.set_labels()

    @staticmethod
    def rename_all_skin_clusters(*args):
        skinLib.rename_all_skin_clusters()

    @staticmethod
    def rename_all_blend_shapes(*args):
        blendShapeLib.rename_all_blend_shapes()

    @staticmethod
    def transfer_skin(*args):
        """
        Transfer skinCluster
        """
        if len(cmds.ls(selection=True)) != 2:
            cmds.error('Select two nodes')

        skinLib.transfer_skin(source=cmds.ls(selection=True)[0],
                              target=cmds.ls(selection=True)[-1],
                              source_skin_index=1,
                              target_skin_index=1,
                              surface_association='closestPoint')

    @staticmethod
    def connect_translate_rotate_scale(*args):
        """
        Connect translate rotate scale
        """
        sel = cmds.ls(selection=True)
        if len(sel) != 2:
            cmds.error('Connect translate rotate scale: You must select two nodes ')

        connectionLib.connect_translate_rotate_scale(driver=sel[0],
                                                     driven=sel[1])

        cmds.select(sel)

    @staticmethod
    def connect_translate(*args):
        """
        Connect translate
        """
        sel = cmds.ls(selection=True)
        if len(sel) != 2:
            cmds.error('Connect translate: You must select two nodes ')

        connectionLib.connect_translate(driver=sel[0],
                                        driven=sel[1])

        cmds.select(sel)

    @staticmethod
    def connect_rotate(*args):
        """
        Connect rotate
        """
        sel = cmds.ls(selection=True)
        if len(sel) != 2:
            cmds.error('Connect rotate: You must select two nodes ')

        connectionLib.connect_rotate(driver=sel[0],
                                     driven=sel[1])

        cmds.select(sel)

    @staticmethod
    def connect_scale(*args):
        """
        Connect scale
        """
        sel = cmds.ls(selection=True)
        if len(sel) != 2:
            cmds.error('Connect scale: You must select two nodes ')

        connectionLib.connect_scale(driver=sel[0],
                                    driven=sel[1])

        cmds.select(sel)

    @staticmethod
    def connect_offset_parent_matrix(*args):
        """
        Connect offset parent matrix
        """
        sel = cmds.ls(selection=True)
        if len(sel) != 2:
            cmds.error('Connect offset parent matrix: You must select two nodes ')

        connectionLib.connect_offset_parent_matrix(driver=sel[0],
                                                   driven=sel[1])

        cmds.select(sel)

    @staticmethod
    def set_mesh_bulge_tool(*args):
        """
        Set mesh bulge tool
        """
        cmds.SetMeshBulgeTool()

    @staticmethod
    def transfer_shape_command(*args):
        """
        Transfer shape command plugin command
        """
        cmds.transferShape()

    @staticmethod
    def show_local_rotation_axis(hierarchy=False, *args):
        if hierarchy:
            cmds.select(hierarchy=True)
        selection_list = cmds.ls(sl=True)

        for node in selection_list:
            if cmds.attributeQuery('displayLocalAxis', node=node, exists=True):
                cmds.setAttr('{}.displayLocalAxis'.format(node), True)

    @staticmethod
    def hide_local_rotation_axis(hierarchy=False, *args):
        if hierarchy:
            cmds.select(hierarchy=True)
        selection_list = cmds.ls(sl=True)

        for node in selection_list:
            if cmds.attributeQuery('displayLocalAxis', node=node, exists=True):
                cmds.setAttr('{}.displayLocalAxis'.format(node), False)

    # Builder
    def builder_menu(self):
        builder_menu = cmds.menuItem(parent=self.menu_name, label='Builder', radialPosition='E', subMenu=True)

        # ----- Build  -----
        cmds.menuItem(parent=builder_menu, label='Build', radialPosition='N', command=self.build_rig)

        # ----- Body guides Menu -----
        self.body_menu(menu_parent=builder_menu, radial_position='SW')

        # ----- Templates Guides Menu -----
        self.templates_menu(menu_parent=builder_menu, radial_position='S')

        # ----- Face guides Menu -----
        self.face_menu(builder_menu, radial_position='SE')

        # ----- Delete guides -----
        cmds.menuItem(parent=builder_menu, label='             Builder utils             ', enable=False)
        cmds.menuItem(parent=builder_menu, divider=True)

        cmds.menuItem(parent=builder_menu, label='Skin Pose', command=skinLib.set_skin_pose)

        cmds.menuItem(parent=builder_menu, divider=True)

        cmds.menuItem(parent=builder_menu, label='Delete guides', command=guideLib.delete_guides)

    def body_menu(self, menu_parent, radial_position):
        """
        Create the body menu items
        """
        body_guides_menu = cmds.menuItem(parent=menu_parent, label='Body Guides', radialPosition=radial_position,
                                         subMenu=True)

        cmds.menuItem(parent=body_guides_menu, label='             Body             ', enable=False)
        cmds.menuItem(parent=body_guides_menu, divider=True)

        # Root guides
        cmds.menuItem(parent=body_guides_menu, label='Root', command=self.create_root_guides)
        cmds.menuItem(optionBox=True, command=rootWindow.RootWindow)

        # Spine guides
        cmds.menuItem(parent=body_guides_menu, label='Spine', command=self.create_column_guides)
        cmds.menuItem(optionBox=True, command=spineWindow.SpineWindow)

        # Neck guides
        cmds.menuItem(parent=body_guides_menu, label='Neck', command=self.create_neck_guides)
        cmds.menuItem(optionBox=True, command=neckWindow.NeckWindow)

        # Arms guides
        cmds.menuItem(parent=body_guides_menu, label='Arms', command=self.create_arm_guides)
        cmds.menuItem(optionBox=True, command=armWindow.ArmWindow)

        # Legs guides
        cmds.menuItem(parent=body_guides_menu, label='Legs', command=self.create_leg_guides)
        cmds.menuItem(optionBox=True, command=legWindow.LegWindow)

    @staticmethod
    def face_menu(menu_parent, radial_position):
        """
        Create the face menu items
        """
        face_guides_menu = cmds.menuItem(parent=menu_parent, label='Face Guides', radialPosition=radial_position,
                                         subMenu=True, enable=False)

        cmds.menuItem(parent=face_guides_menu, label='             Face             ', enable=False)
        cmds.menuItem(parent=face_guides_menu, divider=True)

        # Brows guides
        cmds.menuItem(parent=face_guides_menu, label='Brows', enable=False)
        cmds.menuItem(optionBox=True, enable=False)

        # Eyelids guides
        cmds.menuItem(parent=face_guides_menu, label='Eyelids', enable=False)
        cmds.menuItem(optionBox=True, enable=False)

        # Cheeks Up guides
        cmds.menuItem(parent=face_guides_menu, label='Cheeks Up', enable=False)
        cmds.menuItem(optionBox=True, enable=False)

        # Cheeks guides
        cmds.menuItem(parent=face_guides_menu, label='Cheeks', enable=False)
        cmds.menuItem(optionBox=True, enable=False)

        # Ears guides
        cmds.menuItem(parent=face_guides_menu, label='Ears', enable=False)
        cmds.menuItem(optionBox=True, enable=False)

        # Mouth guides
        cmds.menuItem(parent=face_guides_menu, label='Mouth', enable=False)
        cmds.menuItem(optionBox=True, enable=False)

    def templates_menu(self, menu_parent, radial_position):
        """
        Create the templates menu items
        """
        template_guides_menu = cmds.menuItem(parent=menu_parent, label='Templates Guides',
                                             radialPosition=radial_position, subMenu=True)

        cmds.menuItem(parent=template_guides_menu, label='             Templates             ', enable=False)
        cmds.menuItem(parent=template_guides_menu, divider=True)

        cmds.menuItem(parent=template_guides_menu, label='Biped', command=self.create_biped_guides)

        cmds.menuItem(parent=template_guides_menu, label='Quadruped', enable=False)

        cmds.menuItem(parent=template_guides_menu, label='Bird', enable=False)

        cmds.menuItem(parent=template_guides_menu, divider=True)

        cmds.menuItem(parent=template_guides_menu, label='Face', enable=False)

    @staticmethod
    def build_rig(*args):
        """
        Look for the guides' groups and create the rig
        """
        guides_grp = 'guides_c_grp'
        guides_groups = cmds.listRelatives(guides_grp, children=True)
        for guide_group in guides_groups:
            descriptor = guide_group.split('Guides')[0]
            side = guide_group.split('_')[1]

            module_name = cmds.getAttr('{}.moduleName'.format(guide_group))
            root_path = r'{}\builder\modules'.format(hiddenStrings.hidden_strings_path)

            for i in os.scandir(root_path):
                if i.is_dir():
                    for file in os.listdir(i):
                        if file == '{}.py'.format(module_name.lower()):
                            file = file.split('.py')[0]
                            file_capitalize = file.capitalize()

                            file_path = i.path.split(hiddenStrings.hidden_strings_name)[-1]  # Get relative path
                            file_path = file_path.split(os.sep)  # split path

                            rig_module = importlib.import_module('{}{}.{}'.format(hiddenStrings.hidden_strings_name,
                                                                                  '.'.join(file_path),
                                                                                  file))
                            rig_module = getattr(rig_module, file_capitalize)
                            rig_module = rig_module(descriptor=descriptor, side=side)

                            rig_module.run()

        cmds.delete(guides_grp)

    def create_biped_guides(self, *args):
        """
        Biped guides template
        """
        self.create_root_guides()
        self.create_column_guides()
        self.create_neck_guides()
        self.create_arm_guides()
        self.create_leg_guides()

    @staticmethod
    def create_root_guides(*args):
        """
        Create root guides command
        """
        root_module = root.Root()
        root_module.create_guides()

    @staticmethod
    def create_column_guides(*args):
        """
        Create column guides command
        """
        column_module = column.Column()
        column_module.create_guides()

    @staticmethod
    def create_neck_guides(*args):
        """
        Create neck guides command
        """
        neck_module = neck.Neck()
        neck_module.create_guides()

    @staticmethod
    def create_arm_guides(*args):
        """
        Create arm guides command
        """
        arm_l_module = arm.Arm(side='l')
        arm_r_module = arm.Arm(side='r')

        arm_l_module.create_guides()
        arm_r_module.create_guides(connect_to_opposite_value=True)

    @staticmethod
    def create_leg_guides(*args):
        """
        Create leg guides command
        """
        leg_l_module = leg.Leg(side='l')
        leg_r_module = leg.Leg(side='r')

        leg_l_module.create_guides()
        leg_r_module.create_guides(connect_to_opposite_value=True)
