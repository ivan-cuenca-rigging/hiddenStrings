# Imports
import os
import logging
import importlib


# Maya imports
from maya import cmds

# Project imports
from hiddenStrings import module_utils
from hiddenStrings import config as hiddenStrings_config
from hiddenStrings.libs import (guide_lib, blend_shape_lib, skeleton_lib, connection_lib, skin_lib,
                                import_export_lib, trigger_lib, reference_lib, side_lib, usage_lib, scene_lib)

from hiddenStrings.ui.windows import blend_shape_windows, connections_windows, skin_windows, tools_windows

builder_exists = os.path.exists(r'{}/builder'.format(module_utils.hidden_strings_path))
if builder_exists:
    from hiddenStrings.builder.modules.body import column, leg, root, arm, neck
    from hiddenStrings.builder.modules.face import (brows, eyes, eye, ear, cheek, cheekbone, tongue, nose,
                                                    teeth, eyelid, eyeline, mouth, squash)

    from hiddenStrings.ui.windows import body_windows
    from hiddenStrings.ui.windows import face_windows

logging = logging.getLogger(__name__)


class MarkingMenu(object):
    """
    Create the hiddenStrings marking Menu

    Args:
        click_input (int): click button input. 1 -> left click, 2 -> middle click, 3 -> right click
    """

    def __init__(self, click_input):
        """
        Initializes an instance of MarkinMenu

        Args:
            click_input (int): click button input. 1 -> left click, 2 -> middle click, 3 -> right click
        """
        self.menu_name = module_utils.hidden_strings_name
        self.icon_path = r'{}/icons/hiddenStrings_white.png'.format(module_utils.hidden_strings_path)

        self.click_input = click_input

        self.delete()
        self.build()

    def build(self, *args):
        """
        Build the marking menu
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
        Delete the marking menu
        """
        if cmds.popupMenu(self.menu_name, exists=True):
            cmds.deleteUI(self.menu_name)

    def marking_menu_config(self):
        """
        Create the marking menu items
        """
        # ---------- North ----------
        self.deformation_menu(menu_parent=self.menu_name, radial_position='N')

        # ---------- West ----------
        self.connections_menu(menu_parent=self.menu_name, radial_position='W')

        # ---------- South ----------
        self.maya_editors_menu(menu_parent=self.menu_name, radial_position='S')

        # ---------- South List ----------
        cmds.menuItem(parent=self.menu_name, label='           Tools', enable=False)
        cmds.menuItem(parent=self.menu_name, divider=True)

        cmds.menuItem(parent=self.menu_name, label='Copy matrix', command=self.export_matrix)

        cmds.menuItem(parent=self.menu_name, label='Paste matrix', command=self.import_matrix)

        cmds.menuItem(parent=self.menu_name, divider=True)

        cmds.menuItem(parent=self.menu_name, label='Save selection', command=self.export_selection)

        cmds.menuItem(parent=self.menu_name, label='Load selection', command=self.import_selection)

        cmds.menuItem(parent=self.menu_name, divider=True)

        cmds.menuItem(parent=self.menu_name, label='Renamer', command=tools_windows.RenamerWindow)

        cmds.menuItem(parent=self.menu_name, label='Shape manager', command=tools_windows.ShapeManagerWindow)

        local_rotation_axis_hierarchy = cmds.menuItem(parent=self.menu_name, label='Local rotation axis', subMenu=True)

        cmds.menuItem(parent=local_rotation_axis_hierarchy, label='Show',
                      command=self.show_local_rotation_axis)
        cmds.menuItem(parent=local_rotation_axis_hierarchy, label='Show with hierarchy',
                      command=self.show_local_rotation_axis_with_hierarchy)

        cmds.menuItem(parent=local_rotation_axis_hierarchy, divider=True)

        cmds.menuItem(parent=local_rotation_axis_hierarchy, label='Hide',
                      command=self.hide_local_rotation_axis)
        cmds.menuItem(parent=local_rotation_axis_hierarchy, label='Hide with hierarchy',
                      command=self.hide_local_rotation_axis_with_hierarchy)

        if hiddenStrings_config.dev_mode:
            cmds.menuItem(parent=self.menu_name, divider=True)
            cmds.menuItem(parent=self.menu_name, label='Reload modules', command=module_utils.reload)

        # ---------- East ----------
        if builder_exists:
            self.builder_menu()

    def deformation_menu(self, menu_parent, radial_position):
        """
        Create the deformation menu items

        Args:
            menu_parent (str): name of the menu parent
            radial_position (str): radial position. 'N', 'NE', 'E', 'SE', 'S', 'SW', 'W' or 'NW'.
        """
        deformation_menu = cmds.menuItem(parent=menu_parent, label='Deformation', radialPosition=radial_position,
                                         subMenu=True)

        cmds.menuItem(parent=deformation_menu, label='Shape Editor', radialPosition='NE',
                      command=cmds.ShapeEditor)

        self.blend_shapes_menu(menu_parent=deformation_menu, radial_position='E')

        cmds.menuItem(parent=deformation_menu, label='Transfer shape', radialPosition='N',
                      command=self.transfer_shape_command)

        cmds.menuItem(parent=deformation_menu, label='Paint Skin Weights', radialPosition='NW',
                      command=cmds.ArtPaintSkinWeightsToolOptions)

        self.skins_menu(menu_parent=deformation_menu, radial_position='W')

        # ---- south ----
        cmds.menuItem(parent=deformation_menu, label='          Triggers', enable=False)
        cmds.menuItem(parent=deformation_menu, divider=True)

        cmds.menuItem(parent=deformation_menu, label='Pose Reader: Angle', command=self.create_default_angle_reader)
        cmds.menuItem(parent=deformation_menu, optionBox=True, command=blend_shape_windows.CreateAngleWindow)

        cmds.menuItem(parent=deformation_menu, label='Pose Reader: Bary', command=self.create_default_bary)
        cmds.menuItem(parent=deformation_menu, optionBox=True, command=blend_shape_windows.CreateBaryWindow)

    def blend_shapes_menu(self, menu_parent, radial_position):
        """
        Create the shapes menu items

        Args:
            menu_parent (str): name of the menu parent
            radial_position (str): radial position. 'N', 'NE', 'E', 'SE', 'S', 'SW', 'W' or 'NW'.
        """
        blend_shape_menu = cmds.menuItem(parent=menu_parent, label='Blendshapes', radialPosition=radial_position,
                                         subMenu=True)

        cmds.menuItem(parent=blend_shape_menu, label='           blendShapes Utils', enable=False)
        cmds.menuItem(parent=blend_shape_menu, divider=True)

        cmds.menuItem(parent=blend_shape_menu, label='Rename all blendShapes',
                      command=self.rename_all_blend_shapes)

        cmds.menuItem(parent=blend_shape_menu, divider=True)

        cmds.menuItem(parent=blend_shape_menu, label='Edit Blendshape / In-Between',
                      command=blend_shape_lib.edit_target_or_in_between)

        cmds.menuItem(parent=blend_shape_menu, label='Multiply vertex values',
                      command=blend_shape_windows.MultiplyVertexValues)

        cmds.menuItem(parent=blend_shape_menu, divider=True)

        cmds.menuItem(parent=blend_shape_menu, label='Mirror targets',
                      command=self.mirror_targets)

        cmds.menuItem(parent=blend_shape_menu, label='Copy target connection',
                      command=blend_shape_lib.copy_target_connection)

        cmds.menuItem(parent=blend_shape_menu, label='Copy Blendshape connections',
                      command=blend_shape_lib.copy_blendshape_connections)

        cmds.menuItem(parent=blend_shape_menu, divider=True)

        cmds.menuItem(parent=blend_shape_menu, label='Transfer Blendshape targets',
                      command=blend_shape_lib.transfer_blend_shape)

        cmds.menuItem(parent=blend_shape_menu, label='Automatic Correctives',
                      command=blend_shape_windows.AutomaticCorrectiveWindow)

        cmds.menuItem(parent=blend_shape_menu, divider=True)
        cmds.menuItem(parent=blend_shape_menu, label='              Import/Export', enable=False)
        cmds.menuItem(parent=blend_shape_menu, divider=True)

        cmds.menuItem(parent=blend_shape_menu, label='Import BlendShapes',
                      command=blend_shape_windows.ImportBlendShapeWindow)

        cmds.menuItem(parent=blend_shape_menu, label='Export BlendShapes',
                      command=self.export_blend_shapes)
        cmds.menuItem(parent=blend_shape_menu, optionBox=True,
                      command=blend_shape_windows.ExportBlendShapeWindow)

    def skins_menu(self, menu_parent, radial_position):
        """
        Create the skins menu items

        Args:
            menu_parent (str): name of the menu parent
            radial_position (str): radial position. 'N', 'NE', 'E', 'SE', 'S', 'SW', 'W' or 'NW'.
        """
        skin_menu = cmds.menuItem(parent=menu_parent, label='Skins', radialPosition=radial_position,
                                  subMenu=True)

        cmds.menuItem(parent=skin_menu, label='             Skins Utils', enable=False)
        cmds.menuItem(parent=skin_menu, divider=True)

        cmds.menuItem(parent=skin_menu, label='Rename all skinClusters',
                      command=self.rename_all_skin_clusters)

        cmds.menuItem(parent=skin_menu, divider=True)

        cmds.menuItem(parent=skin_menu, label='Set Labels',
                      command=self.set_labels)

        cmds.menuItem(parent=skin_menu, divider=True)

        cmds.menuItem(parent=skin_menu, label='Push joint',
                      command=skin_windows.PushJointWindow)

        cmds.menuItem(parent=skin_menu, divider=True)

        cmds.menuItem(parent=skin_menu, label='Transfer Skin',
                      command=self.transfer_skin)
        cmds.menuItem(parent=skin_menu, optionBox=True,
                      command=skin_windows.TransferSkinWindow)

        cmds.menuItem(parent=skin_menu, divider=True)
        cmds.menuItem(parent=skin_menu, label='          Import/Export', enable=False)
        cmds.menuItem(parent=skin_menu, divider=True)

        cmds.menuItem(parent=skin_menu, label='Import Skins', command=skin_windows.ImportSkinWindow)

        cmds.menuItem(parent=skin_menu, label='Export Skins',
                      command=self.export_skin_clusters)
        cmds.menuItem(parent=skin_menu, optionBox=True, command=skin_windows.ExportSkinWindow)

    def reference_menu(self, menu_parent, radial_position):
        """
        Create the reference menu items

        Args:
            menu_parent (str): name of the menu parent
            radial_position (str): radial position. 'N', 'NE', 'E', 'SE', 'S', 'SW', 'W' or 'NW'.
        """
        reference_menu = cmds.menuItem(parent=menu_parent, label='Reference', radialPosition=radial_position,
                                       subMenu=True)

        cmds.menuItem(parent=reference_menu, label='Reference Editor', radialPosition='N',
                      command=cmds.ReferenceEditor)

        cmds.menuItem(parent=reference_menu, label='Reload reference', radialPosition='S',
                      command=reference_lib.reload_reference)

        cmds.menuItem(parent=reference_menu, label='Replace reference', radialPosition='E',
                      command=reference_lib.replace_reference_window)

        cmds.menuItem(parent=reference_menu, label='Remove reference', radialPosition='W',
                      command=reference_lib.remove_reference)

    def connections_menu(self, menu_parent, radial_position):
        """
        Create the connection menu items

        Args:
            menu_parent (str): name of the menu parent
            radial_position (str): radial position. 'N', 'NE', 'E', 'SE', 'S', 'SW', 'W' or 'NW'.
        """
        connections_menu = cmds.menuItem(parent=menu_parent, label='Connections', radialPosition=radial_position,
                                         subMenu=True)

        cmds.menuItem(parent=connections_menu, label='Connection Editor', radialPosition='W',
                      command=cmds.ConnectionEditor)

        cmds.menuItem(parent=connections_menu, label='             Connections Utils', enable=False)

        cmds.menuItem(parent=connections_menu, divider=True)

        cmds.menuItem(parent=connections_menu, label='Connect Translate Rotate Scale',
                      command=self.connect_translate_rotate_scale)
        cmds.menuItem(parent=connections_menu, optionBox=True,
                      command=connections_windows.ConnectTranslateRotateScaleWindow)

        cmds.menuItem(parent=connections_menu, label='Connect Translate',
                      command=self.connect_translate)
        cmds.menuItem(parent=connections_menu, optionBox=True,
                      command=connections_windows.ConnectTranslateWindow)

        cmds.menuItem(parent=connections_menu, label='Connect Rotate',
                      command=self.connect_rotate)
        cmds.menuItem(parent=connections_menu, optionBox=True,
                      command=connections_windows.ConnectRotateWindow)

        cmds.menuItem(parent=connections_menu, label='Connect Scale',
                      command=self.connect_scale)
        cmds.menuItem(parent=connections_menu, optionBox=True,
                      command=connections_windows.ConnectScaleWindow)

        cmds.menuItem(parent=connections_menu, divider=True)
        cmds.menuItem(parent=connections_menu, label='                    Matrices', enable=False)
        cmds.menuItem(parent=connections_menu, divider=True)

        cmds.menuItem(parent=connections_menu, label='Connect OffsetParentMatrix',
                      command=self.connect_offset_parent_matrix)
        cmds.menuItem(parent=connections_menu, optionBox=True,
                      command=connections_windows.ConnectOffsetParentMatrixWindow)

        cmds.menuItem(parent=connections_menu, label='Transform to offsetParentMatrix',
                      command=self.transform_to_offset_parent_matrix)

        cmds.menuItem(parent=connections_menu, label='OffsetParentMatrix to transform',
                      command=self.offset_parent_matrix_to_transform)

        cmds.menuItem(parent=connections_menu, divider=True)
        cmds.menuItem(parent=connections_menu, label='                       UvPin', enable=False)
        cmds.menuItem(parent=connections_menu, divider=True)

        cmds.menuItem(parent=connections_menu, label='Create nurbs UvPin', command=connections_windows.CreateNurbsUvPin)
        
        cmds.menuItem(parent=connections_menu, divider=True)
        cmds.menuItem(parent=connections_menu, label='                Import/Export', enable=False)
        cmds.menuItem(parent=connections_menu, divider=True)

        cmds.menuItem(parent=connections_menu, label='Import nodes and connections',
                      command=connections_windows.ImportNodesAndConnectionsWindow)
        cmds.menuItem(parent=connections_menu, label='Export nodes and connections',
                      command=connections_windows.ExportNodesAndConnectionsWindow)

    def maya_editors_menu(self, menu_parent, radial_position):
        """
        Create the maya editors menu items

        Args:
            menu_parent (str): name of the menu parent
            radial_position (str): radial position. 'N', 'NE', 'E', 'SE', 'S', 'SW', 'W' or 'NW'.
        """
        maya_editors_menu = cmds.menuItem(parent=menu_parent, label='Maya editors', radialPosition=radial_position,
                                          subMenu=True)

        cmds.menuItem(parent=maya_editors_menu, label='Shape Editor', radialPosition='NE',
                      command=cmds.ShapeEditor)

        cmds.menuItem(parent=maya_editors_menu, label='Paint Skin Weights', radialPosition='NW',
                      command=cmds.ArtPaintSkinWeightsToolOptions)

        cmds.menuItem(parent=maya_editors_menu, label='Connection Editor', radialPosition='W',
                      command=cmds.ConnectionEditor)

        cmds.menuItem(parent=maya_editors_menu, label='Graph Editor', radialPosition='E',
                      command=cmds.GraphEditor)

        self.reference_menu(menu_parent=maya_editors_menu, radial_position='N')

        cmds.menuItem(parent=maya_editors_menu, label='Component Editor', radialPosition='SW',
                      command=cmds.ComponentEditor)

        cmds.menuItem(parent=maya_editors_menu, label='Set Driven Key Editor', radialPosition='SE',
                      command=cmds.SetDrivenKey)

        cmds.menuItem(parent=maya_editors_menu, label='Node Editor', radialPosition='S',
                      command=cmds.NodeEditorWindow)

    # Builder
    def builder_menu(self):
        """
        Create the builder menu items
        """
        builder_menu = cmds.menuItem(parent=self.menu_name, label='Builder', radialPosition='E', subMenu=True)

        # ----- Build  -----
        cmds.menuItem(parent=builder_menu, label='Build', radialPosition='N', command=self.build_rig)

        # ----- Body guides Menu -----
        self.body_menu(menu_parent=builder_menu, radial_position='SW')

        # ----- Templates Guides Menu -----
        self.templates_menu(menu_parent=builder_menu, radial_position='S')

        # ----- Face guides Menu -----
        self.face_menu(builder_menu, radial_position='SE')

        # ----- Builder utils -----
        cmds.menuItem(parent=builder_menu, label='             Builder utils             ', enable=False)
        cmds.menuItem(parent=builder_menu, divider=True)

        cmds.menuItem(parent=builder_menu, label='Snap Fk Ik', command=self.snap_fk_ik)

        cmds.menuItem(parent=builder_menu, divider=True)

        cmds.menuItem(parent=builder_menu, label='Skin Pose', command=skin_lib.set_skin_pose)

        cmds.menuItem(parent=builder_menu, divider=True)

        cmds.menuItem(parent=builder_menu, label='Delete guides', command=guide_lib.delete_guides)

        cmds.menuItem(parent=builder_menu, label='Show guides drawlabel', command=self.show_guides_draw_label)
        cmds.menuItem(parent=builder_menu, label='Hide guides drawlabel', command=self.hide_guides_draw_label)

        cmds.menuItem(parent=builder_menu, divider=True)

        cmds.menuItem(parent=builder_menu, label='Show skeleton', command=skeleton_lib.show_skeleton)
        cmds.menuItem(parent=builder_menu, label='Hide skeleton', command=skeleton_lib.hide_skeleton)

        cmds.menuItem(parent=builder_menu, divider=True)

        cmds.menuItem(parent=builder_menu, label='toggle Hidden in outliner', 
                      command=scene_lib.togle_hidden_in_outliner)

    def body_menu(self, menu_parent, radial_position):
        """
        Create the body menu items

        Args:
            menu_parent (str): name of the menu parent
            radial_position (str): radial position. 'N', 'NE', 'E', 'SE', 'S', 'SW', 'W' or 'NW'.
        """
        body_guides_menu = cmds.menuItem(parent=menu_parent, label='Body Guides', radialPosition=radial_position,
                                         subMenu=True)

        cmds.menuItem(parent=body_guides_menu, label='             Body             ', enable=False)
        cmds.menuItem(parent=body_guides_menu, divider=True)

        # Root guides
        cmds.menuItem(parent=body_guides_menu, label='Root', command=self.create_root_guides)
        cmds.menuItem(optionBox=True, command=body_windows.RootWindow)

        # Spine guides
        cmds.menuItem(parent=body_guides_menu, label='Spine', command=self.create_column_guides)
        cmds.menuItem(optionBox=True, command=body_windows.SpineWindow)

        # Neck guides
        cmds.menuItem(parent=body_guides_menu, label='Neck', command=self.create_neck_guides)
        cmds.menuItem(optionBox=True, command=body_windows.NeckWindow)

        # Arms guides
        cmds.menuItem(parent=body_guides_menu, label='Arms', command=self.create_arms_guides)
        cmds.menuItem(optionBox=True, command=body_windows.ArmWindow)

        # Legs guides
        cmds.menuItem(parent=body_guides_menu, label='Legs', command=self.create_legs_guides)
        cmds.menuItem(optionBox=True, command=body_windows.LegWindow)

    def face_menu(self, menu_parent, radial_position):
        """
        Create the face menu items

        Args:
            menu_parent (str): name of the menu parent
            radial_position (str): radial position. 'N', 'NE', 'E', 'SE', 'S', 'SW', 'W' or 'NW'.
        """
        face_guides_menu = cmds.menuItem(parent=menu_parent, label='Face Guides', radialPosition=radial_position,
                                         subMenu=True, enable=True)

        cmds.menuItem(parent=face_guides_menu, label='             Face             ', enable=False)
        cmds.menuItem(parent=face_guides_menu, divider=True)

        # Eyes guides
        cmds.menuItem(parent=face_guides_menu, label='Eyes', command=self.create_eyes_guides)
        cmds.menuItem(optionBox=True, command=face_windows.EyesWindow)

        # Eye guides
        cmds.menuItem(parent=face_guides_menu, label='Eye', command=self.create_eye_guides)
        cmds.menuItem(optionBox=True, command=face_windows.EyeWindow)

        # Brows guides
        cmds.menuItem(parent=face_guides_menu, label='Brows', command=self.create_brows_guides)
        cmds.menuItem(optionBox=True, command=face_windows.BrowsWindow)

        # Eyelid guides
        cmds.menuItem(parent=face_guides_menu, label='Eyelids', command=self.create_eyelids_guides)
        cmds.menuItem(optionBox=True, command=face_windows.EyelidWindow)

        # Eyelines guides
        cmds.menuItem(parent=face_guides_menu, label='Eyelines', command=self.create_eyelines_guides)
        cmds.menuItem(optionBox=True, command=face_windows.EyelineWindow)

        # Nose guides
        cmds.menuItem(parent=face_guides_menu, label='Nose', command=self.create_nose_guides)
        cmds.menuItem(optionBox=True, command=face_windows.NoseWindow)

        # Cheekbone guides
        cmds.menuItem(parent=face_guides_menu, label='Cheekbones', command=self.create_cheekbones_guides)
        cmds.menuItem(optionBox=True, command=face_windows.CheekboneWindow)

        # Cheeks guides
        cmds.menuItem(parent=face_guides_menu, label='Cheeks', command=self.create_cheeks_guides)
        cmds.menuItem(optionBox=True, command=face_windows.CheekWindow)

        # Ears guides
        cmds.menuItem(parent=face_guides_menu, label='Ears', command=self.create_ears_guides)
        cmds.menuItem(optionBox=True, command=face_windows.EarWindow)

        # Mouth guides
        cmds.menuItem(parent=face_guides_menu, label='Mouth', command=self.create_mouth_guides)
        cmds.menuItem(optionBox=True, command=face_windows.MouthWindow)

        # Tongue guides
        cmds.menuItem(parent=face_guides_menu, label='Tongue', command=self.create_tongue_guides)
        cmds.menuItem(optionBox=True, command=face_windows.TongueWindow)

        # Teeth guides
        cmds.menuItem(parent=face_guides_menu, label='Teeth', command=self.create_teeth_guides)
        cmds.menuItem(optionBox=True, command=face_windows.TeethWindow)

        # Squash guides
        cmds.menuItem(parent=face_guides_menu, label='Squash', command=self.create_squash_guides)
        cmds.menuItem(optionBox=True, command=face_windows.SquashWindow)

    def templates_menu(self, menu_parent, radial_position):
        """
        Create the templates menu items

        Args:
            menu_parent (str): name of the menu parent
            radial_position (str): radial position. 'N', 'NE', 'E', 'SE', 'S', 'SW', 'W' or 'NW'.
        """
        template_guides_menu = cmds.menuItem(parent=menu_parent, label='Templates Guides',
                                             radialPosition=radial_position, subMenu=True)

        cmds.menuItem(parent=template_guides_menu, label='             Templates             ', enable=False)
        cmds.menuItem(parent=template_guides_menu, divider=True)

        cmds.menuItem(parent=template_guides_menu, label='Biped', command=self.create_biped_guides)

        cmds.menuItem(parent=template_guides_menu, divider=True)

        cmds.menuItem(parent=template_guides_menu, label='Face', command=self.create_face_guides)

    def build_rig(self, *args):
        """
        Look for the guides' groups and create the rig
        """
        guides_grp = 'guides_c_grp'

        if not cmds.objExists(guides_grp):
            logging.warning(f'"{guides_grp}" not found to build the rig')

        else:
            logging.info('--------------------------------------------------')
            logging.info('---------------- BUILDING THE RIG ----------------')
            logging.info('--------------------------------------------------')

            # For each module create the rig with the guides
            guides_groups = cmds.listRelatives(guides_grp, children=True)
            for guide_group in guides_groups:
                descriptor = guide_group.split('Guides')[0]
                side = guide_group.split('_')[1]

                module_name = cmds.getAttr(f'{guide_group}.moduleName')
                root_path = r'{}/builder/modules'.format(module_utils.hidden_strings_path)

                for i in os.scandir(root_path):
                    if i.is_dir():
                        for file in os.listdir(i):
                            if file == f'{module_name.lower()}.py':
                                file = file.split('.py')[0]
                                file_capitalize = file.capitalize()
                                file_path = i.path.split(module_utils.hidden_strings_name)[-1]  # Get relative path
                                file_path = os.path.normpath(file_path).split(os.sep)  # split path

                                rig_module = importlib.import_module('{}{}.{}'.format(module_utils.hidden_strings_name,
                                                                                    '.'.join(file_path),
                                                                                    file))
                                rig_module = getattr(rig_module, file_capitalize)
                                rig_module = rig_module(descriptor=descriptor, side=side)

                                rig_module.run()
            cmds.delete(guides_grp)

            logging.info('--------------------------------------------------')
            logging.info('------------------- RIG FINISH -------------------')


    def create_biped_guides(self, *args):
        """
        Create the biped guides template
        """
        self.create_root_guides()
        self.create_column_guides()
        self.create_neck_guides()
        self.create_arms_guides()
        self.create_legs_guides()

    def create_face_guides(self, *args):
        """
        Create the face guides template
        """
        self.create_brows_guides()
        self.create_eyelids_guides()
        self.create_eyelines_guides()
        self.create_eyes_guides()
        self.create_ears_guides()
        self.create_nose_guides()
        self.create_cheekbones_guides()
        self.create_cheeks_guides()
        self.create_mouth_guides()
        self.create_tongue_guides()
        self.create_teeth_guides()
        self.create_squash_guides(descriptor='squashSup')
        self.create_squash_guides(descriptor='squashInf')

    @staticmethod
    def create_root_guides(*args):
        """
        Create the root guides command
        """
        root_module = root.Root()
        root_module.create_guides()

    @staticmethod
    def create_column_guides(*args):
        """
        Create the column guides command
        """
        column_module = column.Column()
        column_module.create_guides()

    @staticmethod
    def create_neck_guides(*args):
        """
        Create the neck guides command
        """
        neck_module = neck.Neck()
        neck_module.create_guides()

    @staticmethod
    def create_arms_guides(*args):
        """
        Create the arm guides command
        """
        arm_l_module = arm.Arm(side=side_lib.left)
        arm_r_module = arm.Arm(side=side_lib.right)

        arm_l_module.create_guides()
        arm_r_module.create_guides(connect_to_opposite_value=True)

    @staticmethod
    def create_legs_guides(*args):
        """
        Create the leg guides command
        """
        leg_l_module = leg.Leg(side=side_lib.left)
        leg_r_module = leg.Leg(side=side_lib.right)

        leg_l_module.create_guides()
        leg_r_module.create_guides(connect_to_opposite_value=True)

    @staticmethod
    def create_brows_guides(*args):
        """
        Create the brows guides command
        """
        brows_module = brows.Brows()
        brows_module.create_guides()

    @staticmethod
    def create_eyelids_guides(*args):
        """
        Create the eyelid guides command
        """
        eyelid_l_module = eyelid.Eyelid(side=side_lib.left)
        eyelid_l_module.create_guides()

        eyelid_r_module = eyelid.Eyelid(side=side_lib.right)
        eyelid_r_module.create_guides(connect_to_opposite_value=True)

    @staticmethod
    def create_eyelines_guides(*args):
        """
        Create the eyeline guides command
        """
        eyeline_l_module = eyeline.Eyeline(side=side_lib.left)
        eyeline_l_module.create_guides()

        eyeline_r_module = eyeline.Eyeline(side=side_lib.right)
        eyeline_r_module.create_guides(connect_to_opposite_value=True)

    @staticmethod
    def create_eyes_guides(*args):
        """
        Create the eyes guides command
        """
        eyes_module = eyes.Eyes()
        eyes_module.create_guides()

    @staticmethod
    def create_eye_guides(*args):
        """
        Create the eye guides command
        """
        eye_module = eye.Eye()
        eye_module.create_guides()

    @staticmethod
    def create_ears_guides(*args):
        """
        Create the ears guides command
        """
        ear_l_module = ear.Ear(side=side_lib.left)
        ear_r_module = ear.Ear(side=side_lib.right)

        ear_l_module.create_guides()
        ear_r_module.create_guides(connect_to_opposite_value=True)

    @staticmethod
    def create_cheeks_guides(*args):
        """
        Create the cheeks guides command
        """
        cheek_l_module = cheek.Cheek(side=side_lib.left)
        cheek_r_module = cheek.Cheek(side=side_lib.right)

        cheek_l_module.create_guides()
        cheek_r_module.create_guides(connect_to_opposite_value=True)

    @staticmethod
    def create_nose_guides(*args):
        """
        Create the nose guides command
        """
        nose_module = nose.Nose()

        nose_module.create_guides()

    @staticmethod
    def create_cheekbones_guides(*args):
        """
        Create the cheekbones guides command
        """
        cheekbone_l_module = cheekbone.Cheekbone(side=side_lib.left)
        cheekbone_r_module = cheekbone.Cheekbone(side=side_lib.right)

        cheekbone_l_module.create_guides()
        cheekbone_r_module.create_guides(connect_to_opposite_value=True)

    @staticmethod
    def create_mouth_guides(*args):
        """
        Create the mouth guides command
        """
        mouth_module = mouth.Mouth()
        mouth_module.create_guides()

    @staticmethod
    def create_tongue_guides(*args):
        """
        Create the tongue guides command
        """
        tongue_module = tongue.Tongue()
        tongue_module.create_guides()

    @staticmethod
    def create_teeth_guides(*args):
        """
        Create the teeth guides command
        """
        teeth_module = teeth.Teeth()
        teeth_module.create_guides()

    @staticmethod
    def create_squash_guides(*args, descriptor='squash', side=side_lib.center, ):
        """
        Create the squash guides command
        """
        squash_module = squash.Squash(descriptor, side)
        squash_module.create_guides()

    # ---------- methods ----------

    @staticmethod
    def set_labels(*args):
        """
        Set joints labelling
        """
        skin_lib.set_labels()

    @staticmethod
    def rename_all_skin_clusters(*args):
        """
        Rename all the skiNClusters of the scene
        """
        skin_lib.rename_all_skin_clusters()

    @staticmethod
    def rename_all_blend_shapes(*args):
        """
        Rename all the blendshape of the scene
        """
        blend_shape_lib.rename_all_blend_shapes()

    @staticmethod
    def transfer_skin(*args):
        """
        Transfer skinCluster
        """
        if len(cmds.ls(selection=True)) != 2:
            cmds.error('Select two nodes')

        skin_lib.transfer_skin(source=cmds.ls(selection=True)[0],
                               target=cmds.ls(selection=True)[-1],
                               source_skin_index=1,
                               target_skin_index=1,
                               surface_association='closestPoint')

    @staticmethod
    def export_skin_clusters(*args):
        """
        Export the skinClusters of the selected nodes
        """
        import_export_lib.export_skin_clusters(node_list=cmds.ls(selection=True),
                                               path='{}/skinClusters'.format(os.path.dirname(cmds.file(
                                                   query=True,
                                                   sceneName=True))),
                                               skin_index=None)

    @staticmethod
    def export_blend_shapes(*args):
        """
        Export the blendshapes of the selected nodes
        """
        import_export_lib.export_blend_shapes(node_list=cmds.ls(selection=True),
                                              path='{}/blendShapes'.format(os.path.dirname(cmds.file(query=True,
                                                                                                     sceneName=True))))

    @staticmethod
    def connect_translate_rotate_scale(*args):
        """
        Connect translate rotate scale
        """
        sel = cmds.ls(selection=True)
        if len(sel) != 2:
            cmds.error('Connect translate rotate scale: You must select two nodes ')

        connection_lib.connect_translate_rotate_scale(driver=sel[0],
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

        connection_lib.connect_translate(driver=sel[0],
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

        connection_lib.connect_rotate(driver=sel[0],
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

        connection_lib.connect_scale(driver=sel[0],
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

        connection_lib.connect_offset_parent_matrix(driver=sel[0],
                                                    driven=sel[1])

        cmds.select(sel)

    @staticmethod
    def transform_to_offset_parent_matrix(*args):
        """
        Set matrix in the offsetParentMatrix and set transform to default
        """
        for node in cmds.ls(sl=True):
            connection_lib.transform_to_offset_parent_matrix(node=node)

    @staticmethod
    def offset_parent_matrix_to_transform(*args):
        """
        Set matrix in the transform and set offsetParentMatrix to default
        """
        for node in cmds.ls(sl=True):
            connection_lib.offset_parent_matrix_to_transform(node=node)

    @staticmethod
    def transfer_shape_command(*args):
        """
        TransferShape command plugin command
        """
        cmds.transferShape()

    @staticmethod
    def mirror_targets(*args):
        """
        Mirror blendShape targets
        """
        target_list = blend_shape_lib.get_targets_from_shape_editor(as_index=False)
        for target in target_list:
            blend_shape, target = target.split('.')
            blend_shape_lib.mirror_target(blend_shape=blend_shape, target=target)

    @staticmethod
    def create_default_angle_reader(*args):
        """
        Create a default angle pose reader
        """
        trigger_lib.create_angle_trigger(parent_node=cmds.ls(selection=True)[0], driver_node=cmds.ls(selection=True)[1])

    @staticmethod
    def create_default_bary(*args):
        """
        Create a default bary pose reader
        """
        trigger_lib.create_bary_trigger()

    @staticmethod
    def export_selection(*args):
        """
        Export selection
        """
        import_export_lib.export_selection(file_name='selection_data',
                                           path=r'{}/temp'.format(module_utils.hidden_strings_path))

    @staticmethod
    def import_selection(*args):
        """
        Import selection
        """
        import_export_lib.import_selection(path=r'{}/temp/selection_data.json'.format(module_utils.hidden_strings_path))

    @staticmethod
    def export_matrix(*args):
        """
        Export matrix
        """
        import_export_lib.export_matrix(file_name='matrix_data',
                                        path=r'{}/temp'.format(module_utils.hidden_strings_path))

    @staticmethod
    def import_matrix(*args):
        """
        Import matrix
        """
        import_export_lib.import_matrix(path=r'{}/temp/matrix_data.json'.format(module_utils.hidden_strings_path))

    @staticmethod
    def show_local_rotation_axis(hierarchy=False, *args):
        """
        Show the local rotation axis of the selection
        
        Args:
            hierarchy (bool): show/hide LRA all all the hierarchy. Defaults to False.
        """
        if hierarchy:
            cmds.select(hierarchy=True)
        selection_list = cmds.ls(sl=True)

        for node in selection_list:
            if cmds.attributeQuery('displayLocalAxis', node=node, exists=True):
                cmds.setAttr(f'{node}.displayLocalAxis', True)

    def show_local_rotation_axis_with_hierarchy(self, *args):
        """
        Show the local rotation axis of the selection with hierarchy
        """
        selection_list = cmds.ls(selection=True)
        self.show_local_rotation_axis(hierarchy=True)
        cmds.select(selection_list)

    @staticmethod
    def hide_local_rotation_axis(hierarchy=False, *args):
        """
        Hide the local rotation axis of the selection

        Args:
            hierarchy (bool): show/hide LRA all all the hierarchy. Defaults to False.
        """
        if hierarchy:
            cmds.select(hierarchy=True)
        selection_list = cmds.ls(sl=True)

        for node in selection_list:
            if cmds.attributeQuery('displayLocalAxis', node=node, exists=True):
                cmds.setAttr(f'{node}.displayLocalAxis', False)

    def hide_local_rotation_axis_with_hierarchy(self, *args):
        """
        Hide the local rotation axis of the selection with hierarchy
        """
        selection_list = cmds.ls(selection=True)
        self.hide_local_rotation_axis(hierarchy=True)
        cmds.select(selection_list)

    @staticmethod
    def show_guides_draw_label(*args):
        """
        Show the drawlabel of the guides
        """
        for guide in cmds.ls(f'*{usage_lib.guide}'):
            cmds.setAttr(f'{guide}.drawLabel', True)

    @staticmethod
    def hide_guides_draw_label(*args):
        """
        Hide the drawlabel of the guides
        """
        for guide in cmds.ls(f'*{usage_lib.guide}'):
            cmds.setAttr(f'{guide}.drawLabel', False)

    def snap_fk_ik(self, *args):
        node_list = cmds.ls(selection=True)
        if node_list:
            for node in node_list:
                module_grp = [x for x in cmds.listRelatives(node, fullPath=True)[0].split('|') if 'Module' in x][-1]
                
                if 'Arm' in cmds.getAttr(f'{module_grp}.moduleName') \
                        or 'Leg' in cmds.getAttr(f'{module_grp}.moduleName'):
                    namespace = self.get_namespace()
                    limb = cmds.getAttr(f'{module_grp}.moduleName').lower()
                    side = node.split('_')[-2]

                    self.snap_fk_ik_script(namespace=namespace, limb=limb, side=side)
    
    @staticmethod
    def snap_fk_ik_script(namespace=None, limb='arm', side='l', * args):
        end_name = 'hand' if limb == 'arm' else 'foot'

        snap_info = {'start': {'fk_control': f'{namespace}up{limb.capitalize()}Fk_{side}_ctr',
                               'ik_control': None,
                               'fk_snap': f'{namespace}up{limb.capitalize()}_{side}_jnt',
                               'ik_snap': None,
                               'snap_xform': None
                               },
                     'mid': {'fk_control': f'{namespace}low{limb.capitalize()}Fk_{side}_ctr',
                             'ik_control': f'{namespace}{limb}PoleVector_{side}_ctr',
                             'fk_snap': f'{namespace}low{limb.capitalize()}_{side}_jnt',
                              'ik_snap': f'{namespace}{limb}PoleVector_{side}_snap',
                             'snap_xform': None
                             },
                     'end': {'fk_control': f'{namespace}{end_name}{limb.capitalize()}Fk_{side}_ctr',
                             'ik_control': f'{namespace}{end_name}{limb.capitalize()}Ik_{side}_ctr',
                               'fk_snap': f'{namespace}{end_name}{limb.capitalize()}_{side}_skn',
                             'ik_snap': f'{namespace}{end_name}{limb.capitalize()}_{side}_skn',
                                 'snap_xform': None
                             }
                     }

        settings_control = f'{namespace}{limb}Settings_{side}_ctr'
        state = cmds.getAttr(f'{settings_control}.fkIk')  # 0 == Fk; 1 == Ik

        snap_value = 'ik_snap' if state == 0 else 'fk_snap'
        control_value = 'ik_control' if state == 0 else 'fk_control'

        for key in snap_info.keys():
            if snap_info[key][control_value]:
                snap_info[key]['snap_xform'] = cmds.xform(snap_info[key][snap_value],
                                                          query=True, worldSpace=True, matrix=True)

        new_state = 1 if state == 0 else 0
        cmds.setAttr(f'{settings_control}.fkIk', new_state)

        for key in snap_info.keys():
            if snap_info[key][control_value]:
                cmds.xform(snap_info[key][control_value], worldSpace=True, matrix=snap_info[key]['snap_xform'])
    
    def get_namespace(*args):
        selection = cmds.ls(selection=True)
        namespace = None
        if len(selection) >= 1:
            selection = selection[0]
            if ':' in selection:
                namespace = f"{':'.join(selection.split(':')[:-1])}:"
            else:
                namespace = ''
        else:
            namespace = ''

        return namespace
