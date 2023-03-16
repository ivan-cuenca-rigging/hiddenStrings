# Imports
import os
import logging

# Maya imports
from maya import cmds

# Project imports
from hiddenStrings import module_utils
from hiddenStrings.ui import marking_menu


# -------------------- Settings --------------------

create_userSetup_bool = True

load_markingMenu_bool = True
markingMenu_click_input = 3  # 1 -> left click, 2 -> middle click, 3 -> right click

load_hotkeys_bool = True

load_plugins_bool = True

# --------------------------------------------------

logging = logging.getLogger(__name__)


def set_user_setup():
    """
    create and set the userSetup.py
    """
    scripts_path = os.path.dirname(os.path.dirname(__file__))
    user_setup_file_path = r'{}/userSetup.py'.format(scripts_path)
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
        if module_utils.hidden_strings_name not in content:
            user_setup_file.write('\n')
            user_setup_file.write('# hiddenStrings import\n')
            user_setup_file.write('cmds.evalDeferred("import hiddenStrings")\n')


def load_hotkeys():
    """
    Load the hotkeys
    """
    hotkeys_path = r'{}/prefs/hotkeys/hiddenStrings.mhk'.format(module_utils.hidden_strings_path)

    hotkeys_set_list = cmds.hotkeySet(query=True, hotkeySetArray=True)
    if module_utils.hidden_strings_name not in hotkeys_set_list:
        cmds.hotkeySet(edit=True, ip=hotkeys_path)  # ip == import
    else:
        logging.warning('Hotkeys are already loaded')


def unload_hotkeys():
    """
    Unload the hotkeys
    """
    hotkeys_set_list = cmds.hotkeySet(query=True, hotkeySetArray=True)
    if module_utils.hidden_strings_name in hotkeys_set_list:
        cmds.hotkeySet(module_utils.hidden_strings_name, edit=True, delete=True)
    else:
        logging.warning('Hotkeys are not loaded')


def load_markingMenu():
    """
    load marking menu
    """
    marking_menu.MarkingMenu(markingMenu_click_input)


def unload_markingMenu():
    """
    Unload marking menu
    """
    marking_menu.MarkingMenu(markingMenu_click_input).delete()


def load_plugins():
    """
    Load all project's plugins
    """
    plugins_path = r'{}/plugins'.format(module_utils.hidden_strings_path)

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
    plugins_path = r'{}/plugins'.format(module_utils.hidden_strings_path)

    plugins_list = os.listdir(plugins_path)

    for plugin_name in plugins_list:
        if cmds.pluginInfo(plugin_name, query=True, loaded=True):
            cmds.unloadPlugin(plugin_name)
        else:
            logging.warning('{} is not loaded'.format(plugin_name))


# ----------------------------------------------------------------------------------------------------------------------
if create_userSetup_bool:
    set_user_setup()

if load_markingMenu_bool:
    load_markingMenu()

if load_hotkeys_bool:
    load_hotkeys()

if load_plugins_bool:
    load_plugins()
