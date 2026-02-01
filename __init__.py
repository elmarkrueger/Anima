from .animagine_v4 import (AnimagineXL4_Prompt_Manager,
                           AnimagineXL4_Prompt_Styler)

NODE_CLASS_MAPPINGS = {
    "AnimagineXL4_Prompt_Styler": AnimagineXL4_Prompt_Styler,
    "AnimagineXL4_Prompt_Manager": AnimagineXL4_Prompt_Manager,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AnimagineXL4_Prompt_Styler": "Animagine XL 4.0 Prompt Styler (Advanced)",
    "AnimagineXL4_Prompt_Manager": "Animagine XL 4.0 Prompt Manager (Simple)",
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
