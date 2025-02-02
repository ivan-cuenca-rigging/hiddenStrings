# ----------------------------------------------------------------------------------------------------------------------
# transfer_shape.py - maya command plug-in - PYTHON script
#
#
# DESCRIPTION:
# It can be used to transfer the shape in objectSpace/worldSpace between:
# Meshes
# Nurbs
# Curves
# Lattices
# Both nodes must have the same number of components
#
#
# FLAGS:
# source, s = source node
# target, t = target node
# worldSpace, ws = bool
#
# REQUIRES:
# Load the plug-in from the plug-in manager
#
#
# USAGE:
# cmds.transferShape()
#
# cmds.transferShape(source='node1', target='node2', worldSpace=True)
#
# cmds.transferShape(s='node1', t='node2', ws=True)
#
#
# AUTHOR:
# Ivan Cuenca Ruiz
# Copyright 2023 Ivan Cuenca Ruiz - All Rights Reserved.
# You can find my contact email and more at https://github.com/ivan-cuenca-rigging
#
# VERSIONS:
# 1 - Feb 23, 2023 - Initial Release.
# 2 - Mar 24, 2024 - transfer shape between curves and nurbs updated.
#
# please... do not delete the text above
# ----------------------------------------------------------------------------------------------------------------------

# Imports
import sys


# Maya imports
from maya import cmds
from maya.api import OpenMaya


command_name = 'transferShape'

sourceFlag = '-s'
sourceFlagLong = '-source'

targetFlag = '-t'
targetFlagLong = '-target'

worldSpaceFlag = "-ws"
worldSpaceFlagLong = "-worldSpace"

helpFlag = "-h"
helpFlagLong = "-help"


class PluginCommand(OpenMaya.MPxCommand):
    """
    TransferShape pluginCommand class

    Transfer the shape of a mesh, nurbs, curve or lattice from first selection to the second selection.
    Both nodes must have the same number of components

    source, s (str): source node
    target, t (str): target node
    worldSpace, ws (bool): True == worldSpace, False == objectSpace
    help, h (bool): help information
    """
    def __init__(self):
        OpenMaya.MPxCommand.__init__(self)

        self.source = None
        self.target = None

        self.help = False

        self.world_space = False
        self.om_space = None

        self.source_object_type = None
        self.target_object_type = None
        self.target_points_store = None


    def parse_arguments(self, *args):
        """
        Get data from the flags and store them
        """
        args_data = OpenMaya.MArgDatabase(self.syntax(), *args)

        if args_data.isFlagSet(helpFlag):
            self.help = args_data.flagArgumentBool(helpFlag, 0)

        if self.help:
            self.print_help()
            return
        
        if args_data.isFlagSet(sourceFlag):
            self.source = args_data.flagArgumentString(sourceFlag, 0)
        else:
            if len(cmds.ls(selection=True)) == 0:
                cmds.error('Nothing selected')
            self.source = cmds.ls(selection=True)[0]

        if args_data.isFlagSet(targetFlag):
            self.target = args_data.flagArgumentString(targetFlag, 0)
        else:
            if len(cmds.ls(selection=True)) == 0:
                cmds.error('Nothing selected')
            self.target = cmds.ls(selection=True)[-1]

        if args_data.isFlagSet(worldSpaceFlag):
            self.world_space = args_data.flagArgumentBool(worldSpaceFlag, 0)


    def doIt(self, *args):
        """
        Command script
        """
        self.parse_arguments(*args)
        
        if self.help:
            return
        
        if self.world_space:
            self.om_space = OpenMaya.MSpace.kWorld
        else:
            self.om_space = OpenMaya.MSpace.kObject

        # get object type
        self.source_object_type = cmds.objectType(cmds.listRelatives(self.source, children=True, shapes=True,
                                                                     noIntermediate=True, path=True)[0])
        self.target_object_type = cmds.objectType(cmds.listRelatives(self.target, children=True, shapes=True,
                                                                     noIntermediate=True, path=True)[0])

        cmds.select(self.source, self.target)
        selection_list = OpenMaya.MGlobal.getActiveSelectionList()

        self.source = selection_list.getDagPath(0)
        self.target = selection_list.getDagPath(1)

        # Check both objects have same object type
        if self.source_object_type != self.target_object_type:
            cmds.error('Select two meshes, two nurbs, two curves or two lattices')

        # Transfer depending on the object type
        if self.source_object_type == 'mesh':
            self.transfer_mesh_shape()
        if self.source_object_type == 'nurbsSurface':
            self.transfer_nurbs_shape()
        if self.source_object_type == 'nurbsCurve':
            self.transfer_curve_shape()
        if self.source_object_type == 'lattice':
            self.transfer_lattice_shape()


    def redoIt(self):
        """
        Re-do the command

        press "G" in maya
        """
        self.doIt()


    def undoIt(self):
        """
        Un-do the command
        
        press "Ctrl+Z" in maya
        """
        if self.source_object_type == 'mesh':
            self.transfer_mesh_shape(source_points=self.target_points_store)
        if self.source_object_type == 'nurbsSurface':
            self.transfer_nurbs_shape(source_points=self.target_points_store)
        if self.source_object_type == 'nurbsCurve':
            self.transfer_curve_shape(source_points=self.target_points_store)
        if self.source_object_type == 'lattice':
            self.transfer_lattice_shape(source_points=self.target_points_store)


    def isUndoable(self):
        """
        Without this, the above redoIt and undoIt will not be called
        """
        return True


    def transfer_mesh_shape(self, source_points=None):
        """
        Transfer mesh shape

        Args:
            source_points (bool): for the undo feature, I store the points position before we apply the transfer. Defaults to None
        """
        source = OpenMaya.MFnMesh(self.source)
        target = OpenMaya.MFnMesh(self.target)

        if not source_points:
            source_points = source.getPoints(self.om_space)
            self.target_points_store = target.getPoints(self.om_space)

        target.setPoints(source_points, self.om_space)

        source.updateSurface()
        target.updateSurface()



    def transfer_nurbs_shape(self, source_points=None):
        """
        Transfer nurbs shape

        Args:
            source_points (bool): for the undo feature, I store the points position before we apply the transfer. Defaults to None
        """
        # I've tried with OpenMaya but it seems it does not work when working with blendshapes in edit mode
        if self.world_space:
            world_space = True
            object_space = False
        else:
            world_space = False
            object_space = True

        # Get lattice points positions
        source_point_list = cmds.ls(f'{self.source}.cv[*][*]', flatten=True)
        target_point_list = cmds.ls(f'{self.target}.cv[*][*]', flatten=True)

        if not source_points:
            source_points = dict()
            self.target_points_store = dict()

            for point_name in source_point_list:
                point = point_name.split('.')[-1]
                source_points[point] = cmds.xform(point_name, query=True,
                                                worldSpace=world_space, objectSpace=object_space,
                                                translation=True)

            for point_name in target_point_list:
                point = point_name.split('.')[-1]
                self.target_points_store[point] = cmds.xform(point_name, query=True,
                                                            worldSpace=world_space, objectSpace=object_space,
                                                            translation=True)
        # Set nurbs points positions
        for key, value in source_points.items():
            cmds.xform(f'{self.target}.{key}',
                    worldSpace=world_space, objectSpace=object_space, translation=value)

    def transfer_curve_shape(self, source_points=None):
        """
        Transfer curve shape

        Args:
            source_points (bool): for the undo feature, I store the points position before we apply the transfer. Defaults to None
        """
        # I've tried with OpenMaya but it seems it does not work when working with blendshapes in edit mode
        if self.world_space:
            world_space = True
            object_space = False
        else:
            world_space = False
            object_space = True

        # Get lattice points positions
        source_point_list = cmds.ls(f'{self.source}.cv[*]', flatten=True)
        target_point_list = cmds.ls(f'{self.target}.cv[*]', flatten=True)

        if not source_points:
            source_points = dict()
            self.target_points_store = dict()

            for point_name in source_point_list:
                point = point_name.split('.')[-1]
                source_points[point] = cmds.xform(point_name, query=True,
                                                worldSpace=world_space, objectSpace=object_space,
                                                translation=True)

            for point_name in target_point_list:
                point = point_name.split('.')[-1]
                self.target_points_store[point] = cmds.xform(point_name, query=True,
                                                            worldSpace=world_space, objectSpace=object_space,
                                                            translation=True)
        # Set curve points positions
        for key, value in source_points.items():
            cmds.xform(f'{self.target}.{key}',
                    worldSpace=world_space, objectSpace=object_space, translation=value)

    def transfer_lattice_shape(self, source_points=None):
        """
        Transfer lattice shape

        Args:
            source_points (bool): undo feature argument, I use this to apply the shape stored. Defaults to None
        """
        if self.world_space:
            world_space = True
            object_space = False
        else:
            world_space = False
            object_space = True

        # Get lattice points positions
        source_point_list = cmds.ls(f'{self.source}.pt[*][*][*]', flatten=True)
        target_point_list = cmds.ls(f'{self.target}.pt[*][*][*]', flatten=True)

        if not source_points:
            source_points = dict()
            self.target_points_store = dict()

            for point_name in source_point_list:
                point = point_name.split('.')[-1]
                source_points[point] = cmds.xform(point_name, query=True,
                                                worldSpace=world_space, objectSpace=object_space,
                                                translation=True)

            for point_name in target_point_list:
                point = point_name.split('.')[-1]
                self.target_points_store[point] = cmds.xform(point_name, query=True,
                                                            worldSpace=world_space, objectSpace=object_space,
                                                            translation=True)
        # Set lattices points positions
        for key, value in source_points.items():
            cmds.xform(f'{self.target}.{key}',
                    worldSpace=world_space, objectSpace=object_space, translation=value)

    @staticmethod
    def print_help():
        print('--------------------------------------------------------------------------------')
        print('--------------------------------------------------------------------------------')
        print(' ')
        print('Transfer the shape of a mesh, nurbs, curve or lattice')
        print('If source/target are not provided')
        print('the transfer will occur from the first selection to the second selection.')
        print('Both nodes must have the same number of components')
        print(" ")
        print('--------------------------------------------------------------------------------')
        print(" ")
        print('source, s : string')
        print('target, t : string')
        print('worldSpace, ws : Bool')
        print('help, h : Bool')
        print(" ")
        print('--------------------------------------------------------------------------------')
        print('--------------------------------------------------------------------------------')


def command_creator():
    """
    Create the command
    """
    return PluginCommand()


def syntax_creator():
    """
    Add flags to the maya command
    """
    syntax = OpenMaya.MSyntax()

    # Add flags to the command
    syntax.addFlag(sourceFlag, sourceFlagLong, OpenMaya.MSyntax.kString)
    syntax.addFlag(targetFlag, targetFlagLong, OpenMaya.MSyntax.kString)
    syntax.addFlag(worldSpaceFlag, worldSpaceFlagLong, OpenMaya.MSyntax.kBoolean)
    syntax.addFlag(helpFlag, helpFlagLong, OpenMaya.MSyntax.kBoolean)

    return syntax


def maya_useNewAPI():
    """
    The presence of this function tells Maya that the plugin produces, and
    expects to be passed, objects created using the Maya Python API 2.0.

    some hours wasted because of this :)
    """
    pass


def initializePlugin(plugin):
    """
    Try to load the plug-in, with:
    command_name: name of the command, E.G. cmds.transferShape()
    command_creator: class that the command will call
    syntax_creator: create the syntax/flags for the command
    """
    author = 'Ivan Cuenca'
    version = '1.0.0'

    m_plugin = OpenMaya.MFnPlugin(plugin, author, version)

    try:
        m_plugin.registerCommand(command_name, command_creator, syntax_creator)
    except:  # noqa: E722
        sys.stderr.write(f'Failed to register command: {command_name}')


def uninitializePlugin(plugin):
    """
    Unload the plugin
    """
    m_plugin = OpenMaya.MFnPlugin(plugin)
    try:
        m_plugin.deregisterCommand(command_name)
    except:  # noqa: E722
        sys.stderr.write(f'Failed to de-register command: {command_name}')
