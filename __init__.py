from .animagine_v4 import (AnimagineXL4_Character_Factory,
                           AnimagineXL4_Prompt_Manager,
                           AnimagineXL4_Prompt_Styler)

NODE_CLASS_MAPPINGS = {
    "AnimagineXL4_Prompt_Styler": AnimagineXL4_Prompt_Styler,
    "AnimagineXL4_Prompt_Manager": AnimagineXL4_Prompt_Manager,
    "AnimagineXL4_Character_Factory": AnimagineXL4_Character_Factory,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AnimagineXL4_Prompt_Styler": "Animagine XL 4.0 Prompt Styler (Standard)",
    "AnimagineXL4_Prompt_Manager": "Animagine XL 4.0 Prompt Manager (Simple)",
    "AnimagineXL4_Character_Factory": "Animagine XL 4.0 Character Factory (Expert)",
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
