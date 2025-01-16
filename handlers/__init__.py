from .start_handler import register_start_handler
from .level_selection_handler import register_level_selection_handler
from .theory_handler import register_theory_handler, register_explanation_handler
from .translate_handler import register_translate_handler


def register_handlers():
    register_start_handler()
    register_level_selection_handler()
    register_theory_handler()
    register_explanation_handler()
    register_translate_handler()
