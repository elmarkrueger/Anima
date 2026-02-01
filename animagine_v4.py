import torch

class AnimagineXL4_Prompt_Manager:
    """
    A custom node for ComfyUI designed specifically for Animagine XL 4.0 Opt.
    It implements the optimization guidelines from Cagliostro Lab:
    1. Enforces the placement of quality tags at the END of the prompt.
    2. Injects the official static negative prompt.
    3. Provides temporal steering (Year tags) for style control.
    """
    
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        """
        Defines the input widgets. 
        'text_input': The main multiline text box for the user's simple prompt.
        'style_year': A dropdown to inject the powerful 'year' tags discussed in research.
        'add_quality': Toggle to enable/disable the mandatory suffix.
        """
        return {
            "required": {
                "text_input": ("STRING", {
                    "multiline": True, 
                    "default": "1girl, character name, series, general tags...", 
                    "dynamicPrompts": False
                }),
                "style_year": (,),
                "add_quality_tags": ("BOOLEAN", {"default": True}),
            },
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("positive_prompt", "negative_prompt")
    FUNCTION = "process_prompt"
    CATEGORY = "Animagine/Prompting"

    def process_prompt(self, text_input, style_year, add_quality_tags):
        # --- CONSTANTS DEFINED FROM DEEP RESEARCH ---
        # Source: https://cagliostrolab.net/posts/optimizing-animagine-xl-40-in-depth-guideline-and-update
        
        # The Mandatory Suffix for V4.0 Opt
        # Research indicates these MUST be at the end.
        QUALITY_SUFFIX = "masterpiece, high score, great score, absurdres"
        
        # The Official Negative Prompt
        # Explicitly negates 'average score' and 'low score' to bias high-quality latents.
        OFFICIAL_NEGATIVE = (
            "lowres, bad anatomy, bad hands, text, error, missing finger, "
            "extra digits, fewer digits, cropped, worst quality, low quality, "
            "low score, bad score, average score, signature, watermark, username, blurry"
        )
        
        # --- LOGIC ---
        
        # 1. Clean the user input
        clean_prompt = text_input.strip()
        if clean_prompt.endswith(","):
            clean_prompt = clean_prompt[:-1]
            
        # 2. Handle Temporal Tags (Year)
        # Research shows inserting these can drastically alter style.
        # We append them before the quality tags but after the content.
        year_string = ""
        if style_year == "2024-2025 (Modern)":
            year_string = ", year 2024, year 2025"
        elif style_year == "2015-2018 (Mid-Era)":
            year_string = ", year 2015, year 2016, year 2017, year 2018"
        elif style_year == "2005-2010 (Retro)":
            year_string = ", year 2005, year 2006, year 2007"
            
        # 3. Construct Final Positive Prompt
        # Order: [User Content] + +
        final_positive = clean_prompt
        
        if year_string:
            final_positive += year_string
            
        if add_quality_tags:
            # Check to avoid double commas
            if final_positive:
                final_positive += f", {QUALITY_SUFFIX}"
            else:
                final_positive = QUALITY_SUFFIX

        return (final_positive, OFFICIAL_NEGATIVE)

# Node Mapping for ComfyUI
NODE_CLASS_MAPPINGS = {
    "AnimagineXL4_Prompt_Manager": AnimagineXL4_Prompt_Manager
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AnimagineXL4_Prompt_Manager": "Animagine XL 4.0 Prompt Manager"
}
