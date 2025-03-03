from .start import get_start_handlers
from .help import get_help_handlers
from .settings import get_settings_handlers
from .handlers import get_menu_handlers

def get_base_handlers():
    """Return all base handlers"""
    handlers = []
    handlers.extend(get_start_handlers())
    handlers.extend(get_help_handlers())
    handlers.extend(get_settings_handlers())
    handlers.extend(get_menu_handlers())
    return handlers
