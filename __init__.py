# Project Imports
from hiddenStrings import module_utils, config


# UserSetup
if config.create_userSetup_bool:
    module_utils.set_user_setup()

# MarkingMenu
if config.load_markingMenu_bool:
    module_utils.load_markingMenu(click_input=config.markingMenu_click_input)

# HotKeys
if config.load_hotkeys_bool:
    module_utils.load_hotkeys()

# Plugins
if config.load_plugins_bool:
    module_utils.load_plugins()
