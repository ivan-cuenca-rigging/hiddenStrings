# Imports
import os
import sys
import types
import logging

# Maya imports
from maya import cmds


hidden_strings_path = os.path.dirname(__file__)
hidden_strings_name = os.path.basename(hidden_strings_path)

logging = logging.getLogger(hidden_strings_name)


def reload(*args):
    """
    Reload the given module and all children
    """
    previous_logging = logging
    previous_logging.info('--------------------------------------------------')
    previous_logging.info('--------------------------------------------------')
    # Get a reference to each loaded module
    loaded_modules = dict([(key, value) for key, value in sys.modules.items()
                           if key.startswith(hidden_strings_name) and
                           isinstance(value, types.ModuleType)])

    # Delete references to these loaded modules from sys.modules
    for key in loaded_modules:
        del sys.modules[key]

    # Load each of the modules again
    # Make old modules share state with new modules
    for key in loaded_modules:
        new_module = __import__(key)
        old_module = loaded_modules[key]
        old_module.__dict__.clear()
        old_module.__dict__.update(new_module.__dict__)

    # Print in the command line
    previous_logging.info('--------------------------------------------------')
    previous_logging.info('---------------- Module Reloaded -----------------')
    


def set_user_setup():
    """
    create and set the userSetup.py
    """
    maya_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    maya_version = cmds.about(version=True)

    user_setup_file_path = r'{}/{}/scripts/userSetup.py'.format(maya_path, maya_version)
    # Check if the userSetup.py exists
    if not os.path.exists(user_setup_file_path):
        with open(user_setup_file_path, 'w'):
            pass

    # ---------- Edit userSetup.py ----------
    with open(user_setup_file_path, 'r+') as user_setup_file:
        content = user_setup_file.read()
        # Move file pointer to the beginning of a file
        user_setup_file.seek(0)
        # Empty the file
        user_setup_file.truncate()

        # Maya import
        if 'maya' not in content or 'cmds' not in content:
            user_setup_file.write('from maya import cmds\n')
            user_setup_file.write('\n')

        # File content
        if content:
            user_setup_file.write(content)

        # hiddenStrings import
        if hidden_strings_name not in content:
            user_setup_file.write('\n')
            user_setup_file.write('# hiddenStrings import\n')
            user_setup_file.write('cmds.evalDeferred("import hiddenStrings")\n')


def load_hotkeys():
    """
    Load the hotkeys
    """
    hotkeys_path = r'{}/prefs/hotkeys/hiddenStrings.mhk'.format(hidden_strings_path)

    hotkeys_set_list = cmds.hotkeySet(query=True, hotkeySetArray=True)
    if hidden_strings_name not in hotkeys_set_list:
        cmds.hotkeySet(edit=True, ip=hotkeys_path)  # ip == import
    else:
        logging.warning('Hotkeys are already loaded')


def unload_hotkeys():
    """
    Unload the hotkeys
    """
    hotkeys_set_list = cmds.hotkeySet(query=True, hotkeySetArray=True)
    if hidden_strings_name in hotkeys_set_list:
        cmds.hotkeySet(hidden_strings_name, edit=True, delete=True)
    else:
        logging.warning('Hotkeys are not loaded')


def load_markingMenu(click_input):
    """
    load marking menu

    Args:
        click_input (int): click input. 1 -> left click, 2 -> middle click, 3 -> right click
    """
    from hiddenStrings.ui import marking_menu

    marking_menu.MarkingMenu(click_input)


def unload_markingMenu(click_input):
    """
    Unload marking menu

    Args:
        click_input (int): click input. 1 -> left click, 2 -> middle click, 3 -> right click
    """
    from hiddenStrings.ui import marking_menu

    marking_menu.MarkingMenu(click_input).delete()


def load_plugins():
    """
    Load all project's plugins
    """
    plugins_path = r'{}/plugins'.format(hidden_strings_path)

    plugins_list = os.listdir(plugins_path)
    plugins_list.remove('__init__.py')
    for plugin_name in plugins_list:

        if not cmds.pluginInfo(plugin_name, query=True, loaded=True):
            cmds.loadPlugin(r'{}/{}'.format(plugins_path, plugin_name))
        else:
            logging.warning('{} is already loaded'.format(plugin_name))


def unload_plugins():
    """
    unload all project's plugins
    """
    plugins_path = r'{}/plugins'.format(hidden_strings_path)

    plugins_list = os.listdir(plugins_path)

    for plugin_name in plugins_list:
        if cmds.pluginInfo(plugin_name, query=True, loaded=True):
            cmds.unloadPlugin(plugin_name)
        else:
            logging.warning('{} is not loaded'.format(plugin_name))
