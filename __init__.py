# Imports
from pathlib import Path
import types
import sys
import os

# Maya imports
from maya import cmds

# Project imports
from hiddenStrings.ui import markingMenu


create_userSetup_bool = True

load_markingMenu_bool = True
markingMenu_click_input = 3  # 1 -> left click, 2 -> middle click, 3 -> right click

load_hotkeys_bool = True

load_plugins_bool = True


hidden_strings_name = 'hiddenStrings'
hidden_strings_path = os.path.dirname(__file__)


def reload(*args):
    """
    Reload the given module and all children
    """
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
        print('re-loading {}'.format(key))
        new_module = __import__(key)
        old_module = loaded_modules[key]
        old_module.__dict__.clear()
        old_module.__dict__.update(new_module.__dict__)

    # Print in the command line
    print(end='hiddenStrings reloaded\n')


def set_user_setup():
    """
    create and set the userSetup.py
    """
    scripts_path = os.path.dirname(os.path.dirname(__file__))
    user_setup_file_path = Path(r'{}\userSetup.py'.format(scripts_path))

    # ---------- Check if module is in userSetup.py ----------
    module_in_user_setup = False
    if user_setup_file_path.is_file():
        user_setup_file = open(user_setup_file_path, 'r')
        if hidden_strings_name in user_setup_file.read():
            module_in_user_setup = True
        user_setup_file.close()

    # ---------- Edit userSetup.py ----------
    if not module_in_user_setup:
        user_setup_file = open(user_setup_file_path, 'a')

        user_setup_file.write('\n')
        user_setup_file.write('from maya import cmds\n')
        user_setup_file.write('\n')
        user_setup_file.write('\n')
        user_setup_file.write('cmds.evalDeferred("import hiddenStrings")\n')

        user_setup_file.close()


def load_hotkeys():
    """
    Load the hotkeys
    """
    hotkeys_path = r'{}\prefs\hotkeys\hiddenStrings.mhk'.format(os.path.dirname(__file__))

    hotkeys_set_list = cmds.hotkeySet(query=True, hotkeySetArray=True)
    if hidden_strings_name not in hotkeys_set_list:
        cmds.hotkeySet(edit=True, ip=hotkeys_path)  # ip == import
    else:
        cmds.warning('{} hotkeys are already loaded'.format(hidden_strings_name))


def unload_hotkeys():
    """
    Unload the hotkeys
    """
    hotkeys_set_list = cmds.hotkeySet(query=True, hotkeySetArray=True)
    if hidden_strings_name in hotkeys_set_list:
        cmds.hotkeySet(hidden_strings_name, edit=True, delete=True)
    else:
        cmds.warning('{} hotkeys are not loaded'.format(hidden_strings_name))


def load_markingMenu():
    """
    load marking menu
    """
    markingMenu.MarkingMenu(markingMenu_click_input)


def unload_markingMenu():
    """
    Unload marking menu
    """
    markingMenu.MarkingMenu(markingMenu_click_input).delete()


def load_plugins():
    """
    Load all project's plugins
    """
    plugins_path = r'{}\plugins'.format(os.path.dirname(__file__))

    plugins_list = os.listdir(plugins_path)
    plugins_list.remove('__init__.py')
    for plugin_name in plugins_list:

        if not cmds.pluginInfo(plugin_name, query=True, loaded=True):
            cmds.loadPlugin(r'{}\{}'.format(plugins_path, plugin_name))
        else:
            cmds.warning('{} is already loaded'.format(plugin_name))


def unload_plugins():
    """
    unload all project's plugins
    """
    plugins_path = r'{}\plugins'.format(os.path.dirname(__file__))

    plugins_list = os.listdir(plugins_path)

    for plugin_name in plugins_list:
        if cmds.pluginInfo(plugin_name, query=True, loaded=True):
            cmds.unloadPlugin(plugin_name)
        else:
            cmds.warning('{} is not loaded'.format(plugin_name))


# ----------------------------------------------------------------------------------------------------------------------
if create_userSetup_bool:
    set_user_setup()

if load_markingMenu_bool:
    load_markingMenu()

if load_hotkeys_bool:
    load_hotkeys()

if load_plugins_bool:
    load_plugins()
