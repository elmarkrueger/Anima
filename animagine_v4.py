"""
Animagine XL 4.0 Prompt Styler for ComfyUI
==========================================
Implements the official optimization guidelines from Cagliostro Lab:
https://cagliostrolab.net/posts/optimizing-animagine-xl-40-in-depth-guideline-and-update

Tag Ordering Method (critical for optimal results):
1. Subject count (1girl, 1boy, etc.)
2. Character name (if applicable)
3. Series/copyright name (mandatory for character accuracy)
4. Artist tag (placed early, NOT at the end)
5. General tags (features, clothing, pose, setting)
6. Rating tag (safe, sensitive, nsfw, explicit)
7. Quality tags at the END (masterpiece, high score, great score, absurdres)
"""


class AnimagineXL4_Prompt_Styler:
    """
    An advanced prompt styler for Animagine XL 4.0 Opt that transforms simple prompts
    into fully optimized positive and negative prompts following Cagliostro Lab guidelines.
    """
    
    # --- CONSTANTS FROM CAGLIOSTRO LAB GUIDELINES ---
    QUALITY_SUFFIX = "masterpiece, high score, great score, absurdres"
    
    OFFICIAL_NEGATIVE = (
        "lowres, bad anatomy, bad hands, text, error, missing finger, "
        "extra digits, fewer digits, cropped, worst quality, low quality, "
        "low score, bad score, average score, signature, watermark, username, blurry"
    )
    
    SUBJECT_COUNTS = [
        "None",
        "1girl",
        "2girls", 
        "3girls",
        "4girls",
        "5girls",
        "6+girls",
        "multiple girls",
        "1boy",
        "2boys",
        "3boys",
        "4boys",
        "5boys",
        "6+boys",
        "multiple boys",
        "1girl, 1boy",
        "2girls, 1boy",
        "1girl, 2boys",
        "1other",
        "multiple others",
        "no humans",
    ]
    
    RATING_TAGS = [
        "None",
        "safe",
        "sensitive",
        "nsfw",
        "explicit",
    ]
    
    YEAR_STYLES = [
        "None",
        "2024-2025 (Modern)",
        "2020-2023 (Recent)",
        "2015-2019 (Mid-Era)",
        "2010-2014 (Classic)",
        "2005-2009 (Retro)",
        "2000-2004 (Early Digital)",
    ]
    
    # Common anime art styles/aesthetics
    ART_STYLES = [
        "None",
        "anime coloring",
        "flat color",
        "cel shading",
        "soft shading",
        "gradient shading",
        "painterly",
        "watercolor (medium)",
        "faux traditional media",
        "sketch",
        "lineart",
        "monochrome",
        "greyscale",
        "sepia",
        "limited palette",
        "high contrast",
        "soft focus",
        "depth of field",
        "chromatic aberration",
        "film grain",
        "vignetting",
    ]
    
    # Common poses
    POSES = [
        "None",
        "standing",
        "sitting",
        "kneeling",
        "lying",
        "walking",
        "running",
        "jumping",
        "flying",
        "crouching",
        "leaning forward",
        "leaning back",
        "arms up",
        "arms behind back",
        "hands on hips",
        "crossed arms",
        "peace sign",
        "v",
        "thumbs up",
        "waving",
        "pointing",
        "salute",
        "fighting stance",
        "action pose",
    ]
    
    # Camera angles/framing
    FRAMING = [
        "None",
        "portrait",
        "upper body",
        "cowboy shot",
        "full body",
        "wide shot",
        "close-up",
        "extreme close-up",
        "from above",
        "from below",
        "from side",
        "from behind",
        "dutch angle",
        "fish-eye",
        "pov",
        "first-person view",
    ]
    
    # Background/setting options
    BACKGROUNDS = [
        "None",
        "simple background",
        "white background",
        "grey background",
        "black background",
        "gradient background",
        "abstract background",
        "detailed background",
        "blurry background",
        "outdoors",
        "indoors",
        "cityscape",
        "nature",
        "sky",
        "night sky",
        "starry sky",
        "sunset",
        "sunrise",
        "cloudy sky",
        "forest",
        "beach",
        "ocean",
        "mountain",
        "field",
        "garden",
        "park",
        "street",
        "classroom",
        "bedroom",
        "living room",
        "kitchen",
        "bathroom",
        "office",
        "library",
        "cafe",
        "restaurant",
        "train station",
        "school",
        "rooftop",
        "balcony",
        "ruins",
        "fantasy",
        "sci-fi",
        "cyberpunk",
    ]
    
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                # Core prompt input
                "simple_prompt": ("STRING", {
                    "multiline": True, 
                    "default": "Enter your simple prompt here...\n(features, clothing, actions, expressions, etc.)", 
                    "dynamicPrompts": False
                }),
            },
            "optional": {
                # Character identification (Tag Ordering: comes first)
                "subject_count": (cls.SUBJECT_COUNTS, {"default": "1girl"}),
                "character_name": ("STRING", {
                    "default": "",
                    "placeholder": "e.g., hatsune miku, shiroko (blue archive)"
                }),
                "series_name": ("STRING", {
                    "default": "",
                    "placeholder": "e.g., vocaloid, blue archive (IMPORTANT for characters!)"
                }),
                
                # Artist styling (placed after character/series, NOT at end)
                "artist_tag": ("STRING", {
                    "default": "",
                    "placeholder": "e.g., ciloranko, wlop, sakimichan"
                }),
                
                # Composition helpers
                "pose": (cls.POSES, {"default": "None"}),
                "framing": (cls.FRAMING, {"default": "None"}),
                "background": (cls.BACKGROUNDS, {"default": "None"}),
                "art_style": (cls.ART_STYLES, {"default": "None"}),
                
                # Rating and quality control
                "rating": (cls.RATING_TAGS, {"default": "safe"}),
                "year_style": (cls.YEAR_STYLES, {"default": "2024-2025 (Modern)"}),
                
                # Toggles
                "add_quality_tags": ("BOOLEAN", {"default": True}),
                "enhance_negative": ("BOOLEAN", {"default": False}),
                
                # Additional custom inputs
                "additional_positive": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "Additional tags to append (before quality tags)"
                }),
                "additional_negative": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "Additional negative tags to append"
                }),
            },
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("positive_prompt", "negative_prompt")
    FUNCTION = "build_optimized_prompts"
    CATEGORY = "Animagine/Prompting"
    
    def _clean_tag(self, tag: str) -> str:
        """Clean a single tag by stripping whitespace and removing trailing commas."""
        tag = tag.strip()
        while tag.endswith(","):
            tag = tag[:-1].strip()
        while tag.startswith(","):
            tag = tag[1:].strip()
        return tag
    
    def _clean_prompt(self, prompt: str) -> str:
        """Clean and normalize a prompt string."""
        if not prompt:
            return ""
        # Remove extra whitespace and normalize commas
        prompt = " ".join(prompt.split())
        prompt = prompt.replace(" ,", ",").replace(",  ", ", ").replace(",,", ",")
        prompt = self._clean_tag(prompt)
        return prompt
    
    def _get_year_tags(self, year_style: str) -> str:
        """Convert year style selection to appropriate tags."""
        year_mappings = {
            "2024-2025 (Modern)": "year 2024, year 2025",
            "2020-2023 (Recent)": "year 2020, year 2021, year 2022, year 2023",
            "2015-2019 (Mid-Era)": "year 2015, year 2016, year 2017, year 2018, year 2019",
            "2010-2014 (Classic)": "year 2010, year 2011, year 2012, year 2013, year 2014",
            "2005-2009 (Retro)": "year 2005, year 2006, year 2007, year 2008, year 2009",
            "2000-2004 (Early Digital)": "year 2000, year 2001, year 2002, year 2003, year 2004",
        }
        return year_mappings.get(year_style, "")
    
    def _get_enhanced_negative(self) -> str:
        """Return an enhanced negative prompt with additional quality controls."""
        enhanced_additions = (
            "jpeg artifacts, compression artifacts, pixelated, "
            "deformed, distorted, disfigured, mutation, mutated, "
            "ugly, duplicate, morbid, out of frame, poorly drawn face, "
            "poorly drawn hands, extra limbs, extra arms, extra legs, "
            "malformed limbs, fused fingers, too many fingers, "
            "long neck, amateur, poorly drawn, bad proportions, "
            "gross proportions, cloned face, body out of frame, "
            "cut off, censored, mosaic censoring"
        )
        return f"{self.OFFICIAL_NEGATIVE}, {enhanced_additions}"

    def build_optimized_prompts(
        self,
        simple_prompt: str,
        subject_count: str = "1girl",
        character_name: str = "",
        series_name: str = "",
        artist_tag: str = "",
        pose: str = "None",
        framing: str = "None",
        background: str = "None",
        art_style: str = "None",
        rating: str = "safe",
        year_style: str = "2024-2025 (Modern)",
        add_quality_tags: bool = True,
        enhance_negative: bool = False,
        additional_positive: str = "",
        additional_negative: str = "",
    ):
        """
        Build optimized positive and negative prompts following Cagliostro Lab guidelines.
        
        Tag Order (critical for Animagine XL 4.0):
        1. Subject count (1girl, 1boy, etc.)
        2. Character name
        3. Series/copyright name
        4. Artist tag (early placement, NOT at end)
        5. General tags (from simple_prompt + composition options)
        6. Rating tag
        7. Year tags (temporal styling)
        8. Quality tags (MUST be at the END)
        """
        
        # Build positive prompt parts in correct order
        prompt_parts = []
        
        # 1. Subject count
        if subject_count and subject_count != "None":
            prompt_parts.append(subject_count)
        
        # 2. Character name
        character_name = self._clean_prompt(character_name)
        if character_name:
            prompt_parts.append(character_name)
        
        # 3. Series/copyright name (important for character accuracy!)
        series_name = self._clean_prompt(series_name)
        if series_name:
            prompt_parts.append(series_name)
        
        # 4. Artist tag (placed after character/series, NOT at end)
        artist_tag = self._clean_prompt(artist_tag)
        if artist_tag:
            # Ensure proper formatting for artist tags
            if not artist_tag.startswith("artist:") and not artist_tag.startswith("("):
                prompt_parts.append(artist_tag)
            else:
                prompt_parts.append(artist_tag)
        
        # 5. General tags from simple prompt
        simple_prompt = self._clean_prompt(simple_prompt)
        # Remove placeholder text if present
        if simple_prompt and "Enter your simple prompt" not in simple_prompt:
            prompt_parts.append(simple_prompt)
        
        # 5b. Composition options
        if framing and framing != "None":
            prompt_parts.append(framing)
        
        if pose and pose != "None":
            prompt_parts.append(pose)
            
        if background and background != "None":
            prompt_parts.append(background)
            
        if art_style and art_style != "None":
            prompt_parts.append(art_style)
        
        # 5c. Additional positive tags
        additional_positive = self._clean_prompt(additional_positive)
        if additional_positive:
            prompt_parts.append(additional_positive)
        
        # 6. Rating tag (before quality tags)
        if rating and rating != "None":
            prompt_parts.append(rating)
        
        # 7. Year tags (temporal styling)
        year_tags = self._get_year_tags(year_style)
        if year_tags:
            prompt_parts.append(year_tags)
        
        # 8. Quality tags at the END (mandatory for optimal results)
        if add_quality_tags:
            prompt_parts.append(self.QUALITY_SUFFIX)
        
        # Combine all parts
        final_positive = ", ".join(part for part in prompt_parts if part)
        
        # Build negative prompt
        if enhance_negative:
            final_negative = self._get_enhanced_negative()
        else:
            final_negative = self.OFFICIAL_NEGATIVE
        
        # Add additional negative tags
        additional_negative = self._clean_prompt(additional_negative)
        if additional_negative:
            final_negative = f"{final_negative}, {additional_negative}"
        
        return (final_positive, final_negative)


# Legacy node for backwards compatibility
class AnimagineXL4_Prompt_Manager:
    """
    Legacy simple prompt manager. Use AnimagineXL4_Prompt_Styler for full features.
    """
    
    QUALITY_SUFFIX = "masterpiece, high score, great score, absurdres"
    OFFICIAL_NEGATIVE = (
        "lowres, bad anatomy, bad hands, text, error, missing finger, "
        "extra digits, fewer digits, cropped, worst quality, low quality, "
        "low score, bad score, average score, signature, watermark, username, blurry"
    )
    
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text_input": ("STRING", {
                    "multiline": True, 
                    "default": "1girl, character name, series, general tags...", 
                    "dynamicPrompts": False
                }),
                "style_year": ([
                    "None",
                    "2024-2025 (Modern)",
                    "2015-2018 (Mid-Era)",
                    "2005-2010 (Retro)",
                ], {"default": "None"}),
                "add_quality_tags": ("BOOLEAN", {"default": True}),
            },
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("positive_prompt", "negative_prompt")
    FUNCTION = "process_prompt"
    CATEGORY = "Animagine/Prompting"

    def process_prompt(self, text_input, style_year, add_quality_tags):
        # Clean the user input
        clean_prompt = text_input.strip()
        if clean_prompt.endswith(","):
            clean_prompt = clean_prompt[:-1]
            
        # Handle Temporal Tags (Year)
        year_string = ""
        if style_year == "2024-2025 (Modern)":
            year_string = ", year 2024, year 2025"
        elif style_year == "2015-2018 (Mid-Era)":
            year_string = ", year 2015, year 2016, year 2017, year 2018"
        elif style_year == "2005-2010 (Retro)":
            year_string = ", year 2005, year 2006, year 2007"
            
        # Construct Final Positive Prompt
        final_positive = clean_prompt
        
        if year_string:
            final_positive += year_string
            
        if add_quality_tags:
            if final_positive:
                final_positive += f", {self.QUALITY_SUFFIX}"
            else:
                final_positive = self.QUALITY_SUFFIX

        return (final_positive, self.OFFICIAL_NEGATIVE)


# Node Mapping for ComfyUI
NODE_CLASS_MAPPINGS = {
    "AnimagineXL4_Prompt_Styler": AnimagineXL4_Prompt_Styler,
    "AnimagineXL4_Prompt_Manager": AnimagineXL4_Prompt_Manager,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AnimagineXL4_Prompt_Styler": "Animagine XL 4.0 Prompt Styler (Advanced)",
    "AnimagineXL4_Prompt_Manager": "Animagine XL 4.0 Prompt Manager (Simple)",
}
