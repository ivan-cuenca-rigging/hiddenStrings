# Imports
import os
import sys
import types
import logging


logging = logging.getLogger(__name__)


hidden_strings_path = os.path.dirname(__file__)
hidden_strings_name = os.path.basename(hidden_strings_path)


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
        new_module = __import__(key)
        old_module = loaded_modules[key]
        old_module.__dict__.clear()
        old_module.__dict__.update(new_module.__dict__)

    # Print in the command line
    logging.info('Module reloaded')
