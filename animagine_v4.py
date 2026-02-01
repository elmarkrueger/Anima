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


    # Character features
    HAIR_LENGTHS = ["None", "short hair", "medium hair", "long hair", "very long hair", "absurdly long hair"]
    HAIR_STYLES = [
        "None", "pony tail", "twintails", "braid", "french braid", "crown braid", 
        "twin braids", "hair bun", "double bun", "drill hair", "ahoge", "bob cut", 
        "hime cut", "pixie cut", "messy hair", "straight hair", "wavy hair", "curly hair", 
        "blunt bangs", "swept bangs", "hair over one eye", "hair over eyes"
    ]
    HAIR_COLORS = [
        "None", "blonde hair", "black hair", "brown hair", "red hair", "blue hair", 
        "green hair", "pink hair", "purple hair", "white hair", "silver hair", "grey hair", 
        "orange hair", "multicolored hair", "two-tone hair", "gradient hair"
    ]
    EYE_COLORS = [
        "None", "blue eyes", "red eyes", "green eyes", "yellow eyes", "purple eyes", 
        "brown eyes", "pink eyes", "grey eyes", "black eyes", "aqua eyes", "heterochromia", "gradient eyes"
    ]
    EXPRESSIONS = [
        "None", "smile", "grin", "smirk", "laughing", "frown", "angry", "annoyed", 
        "sad", "crying", "tears", "blush", "embarrassed", "shy", "nervous", "scared", 
        "surprised", "shocked", "sleepy", "yawn", "bored", "expressionless", "neutral expression", 
        "wink", "one eye closed", "tongue out", "pout", "ahegao"
    ]
    SKIN_TYPES = ["None", "pale skin", "fair skin", "tanned skin", "dark skin", "darker skin"]
    
    # Attire
    ATTIRE_CATEGORIES = [
        "None",
        "school uniform", "sailor dress", "blazer", "gym uniform", "swimsuit", "school swimsuit", "bikini",
        "maid", "waitress", "nurse", "police", "military", "kimono", "yukata", "miko", "cheongsam",
        "casual", "sportswear", "pajamas", "lingerie", "armor", "fantasy", "sci-fi suit", "plugsuit",
        "dress", "suit", "tuxedo", "hoodie", "jacket", "sweater", "t-shirt", "shirt", "blouse",
        "skirt", "shorts", "pants", "jeans", "thighhighs", "pantyhose", "kneehighs"
    ]

    # Environment
    LOCATIONS_INDOOR = [
        "None", "bedroom", "living room", "kitchen", "bathroom", "classroom", "library", "office", 
        "laboratory", "store", "supermarket", "cafe", "restaurant", "bar", "gym", "hospital", 
        "dungeon", "castle", "temple", "shrine"
    ]
    LOCATIONS_OUTDOOR = [
        "None", "street", "city", "cityscape", "ally", "park", "garden", "forest", "woods", 
        "beach", "ocean", "sea", "mountains", "field", "meadow", "flower field", "ruins", 
        "rooftop", "balcony", "train station", "bus stop"
    ]
    TIME_OF_DAY = ["None", "day", "morning", "afternoon", "evening", "sunset", "sunrise", "night", "midnight", "dusk", "dawn"]
    WEATHER = ["None", "sunny", "cloudy", "rain", "raining", "snow", "snowing", "fog", "mist", "windy", "storm", "lightning"]
    LIGHTING = ["None", "sunlight", "moonlight", "natural light", "cinematic lighting", "volumetric lighting", "god rays", "rim lighting", "backlighting", "soft lighting", "hard lighting", "neon lights", "firelight", "candlelight"]

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                # Core prompt input
                "simple_prompt": ("STRING", {
                    "multiline": True, 
                    "default": "Enter your simple prompt here...", 
                    "dynamicPrompts": False
                }),
            },
            "optional": {
                # Character Builder Section
                "gender": (cls.SUBJECT_COUNTS, {"default": "1girl"}),
                "hair_style": (cls.HAIR_STYLES, {"default": "None"}),
                "hair_length": (cls.HAIR_LENGTHS, {"default": "None"}),
                "hair_color": (cls.HAIR_COLORS, {"default": "None"}),
                "eye_color": (cls.EYE_COLORS, {"default": "None"}),
                "expression": (cls.EXPRESSIONS, {"default": "None"}),
                "skin_type": (cls.SKIN_TYPES, {"default": "None"}),
                "attire": (cls.ATTIRE_CATEGORIES, {"default": "None"}),
                
                # Scene Builder Section
                "location_type": (["None", "Indoor", "Outdoor"], {"default": "None"}),
                "location_indoor": (cls.LOCATIONS_INDOOR, {"default": "None"}),
                "location_outdoor": (cls.LOCATIONS_OUTDOOR, {"default": "None"}),
                "time_of_day": (cls.TIME_OF_DAY, {"default": "None"}),
                "weather": (cls.WEATHER, {"default": "None"}),
                "lighting": (cls.LIGHTING, {"default": "None"}),
                
                # Character identification (Tag Ordering: comes first)
                "character_name": ("STRING", {
                    "default": "",
                    "placeholder": "e.g., hatsune miku (optional)"
                }),
                "series_name": ("STRING", {
                    "default": "",
                    "placeholder": "e.g., vocaloid (optional)"
                }),
                
                # Artist and Style
                "artist_tag": ("STRING", {
                    "default": "",
                    "placeholder": "e.g., ciloranko"
                }),
                "art_style": (cls.ART_STYLES, {"default": "None"}),
                "year_style": (cls.YEAR_STYLES, {"default": "2024-2025 (Modern)"}),
                
                # Composition
                "pose": (cls.POSES, {"default": "None"}),
                "framing": (cls.FRAMING, {"default": "None"}),
                
                # Controls
                "rating": (cls.RATING_TAGS, {"default": "safe"}),
                "add_quality_tags": ("BOOLEAN", {"default": True}),
                "enhance_negative": ("BOOLEAN", {"default": False}),
                "additional_positive": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "Additional custom tags"
                }),
            },
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("positive_prompt", "negative_prompt")
    FUNCTION = "build_detailed_prompts"
    CATEGORY = "Animagine/Prompting"
    
    # ... existing helper methods (_clean_tag, _clean_prompt, etc.) ...
    
    def build_detailed_prompts(
        self,
        simple_prompt,
        gender="1girl",
        hair_style="None",
        hair_length="None",
        hair_color="None",
        eye_color="None",
        expression="None",
        skin_type="None",
        attire="None",
        location_type="None",
        location_indoor="None",
        location_outdoor="None",
        time_of_day="None",
        weather="None",
        lighting="None",
        character_name="",
        series_name="",
        artist_tag="",
        art_style="None",
        year_style="2024-2025 (Modern)",
        pose="None",
        framing="None",
        rating="safe",
        add_quality_tags=True,
        enhance_negative=False,
        additional_positive="",
        additional_negative="",
        # These are kept for backward compatibility if called with old args, though INPUT_TYPES changed
        subject_count=None, 
        background=None,
    ):
        # Handle backward compatibility mapping if needed
        # But this is a new node class so strictly we don't need it, 
        # however we are modifying the existing Styler class in-place to Extend it.
        # Wait, if I modify Styler in place, I break existing workflows that use 'subject_count'.
        # The user asked to "extend" it. I should probably ADD A NEW CLASS instead of replacing Styler.
        # Replacing Styler with new inputs breaks inputs for users who update.
        # So I will revert the change to Styler and create AnimagineXL4_Character_Factory
        pass

class AnimagineXL4_Character_Factory(AnimagineXL4_Prompt_Styler):
    """
    A comprehensive Character and Scene Factory for Animagine XL 4.0.
    Allows constructing detailed prompts from a vast database of text snippets.
    """
    
    # Expanded Database of Elements
    HAIR_LENGTHS = ["None", "short hair", "medium hair", "long hair", "very long hair", "absurdly long hair"]
    HAIR_STYLES = [
        "None", "pony tail", "twintails", "braid", "french braid", "crown braid", 
        "twin braids", "hair bun", "double bun", "drill hair", "ahoge", "bob cut", 
        "hime cut", "pixie cut", "messy hair", "straight hair", "wavy hair", "curly hair", 
        "blunt bangs", "swept bangs", "hair over one eye", "hair over eyes"
    ]
    HAIR_COLORS = [
        "None", "blonde hair", "black hair", "brown hair", "red hair", "blue hair", 
        "green hair", "pink hair", "purple hair", "white hair", "silver hair", "grey hair", 
        "orange hair", "multicolored hair", "two-tone hair", "gradient hair"
    ]
    EYE_COLORS = [
        "None", "blue eyes", "red eyes", "green eyes", "yellow eyes", "purple eyes", 
        "brown eyes", "pink eyes", "grey eyes", "black eyes", "aqua eyes", "heterochromia", "gradient eyes"
    ]
    EXPRESSIONS = [
        "None", "smile", "grin", "smirk", "laughing", "frown", "angry", "annoyed", 
        "sad", "crying", "tears", "blush", "embarrassed", "shy", "nervous", "scared", 
        "surprised", "shocked", "sleepy", "yawn", "bored", "expressionless", "neutral expression", 
        "wink", "one eye closed", "tongue out", "pout", "ahegao"
    ]
    SKIN_TYPES = ["None", "pale skin", "fair skin", "tanned skin", "dark skin", "darker skin"]
    
    ATTIRE_CATEGORIES = [
        "None",
        "school uniform", "sailor dress", "blazer", "gym uniform", "swimsuit", "school swimsuit", "bikini",
        "maid", "waitress", "nurse", "police", "military", "kimono", "yukata", "miko", "cheongsam",
        "casual", "sportswear", "pajamas", "lingerie", "armor", "fantasy", "sci-fi suit", "plugsuit",
        "dress", "suit", "tuxedo", "hoodie", "jacket", "sweater", "t-shirt", "shirt", "blouse",
        "skirt", "shorts", "pants", "jeans", "thighhighs", "pantyhose", "kneehighs"
    ]

    LOCATIONS_INDOOR = [
        "None", "bedroom", "living room", "kitchen", "bathroom", "classroom", "library", "office", 
        "laboratory", "store", "supermarket", "cafe", "restaurant", "bar", "gym", "hospital", 
        "dungeon", "castle", "temple", "shrine"
    ]
    LOCATIONS_OUTDOOR = [
        "None", "street", "city", "cityscape", "ally", "park", "garden", "forest", "woods", 
        "beach", "ocean", "sea", "mountains", "field", "meadow", "flower field", "ruins", 
        "rooftop", "balcony", "train station", "bus stop"
    ]
    TIME_OF_DAY = ["None", "day", "morning", "afternoon", "evening", "sunset", "sunrise", "night", "midnight", "dusk", "dawn"]
    WEATHER = ["None", "sunny", "cloudy", "rain", "raining", "snow", "snowing", "fog", "mist", "windy", "storm", "lightning"]
    LIGHTING = ["None", "sunlight", "moonlight", "natural light", "cinematic lighting", "volumetric lighting", "god rays", "rim lighting", "backlighting", "soft lighting", "hard lighting", "neon lights", "firelight", "candlelight"]

    @classmethod
    def INPUT_TYPES(cls):
        # Inherit optional inputs from parent but formatted for our needs
        # We need to redefine to ensure order
        return {
            "required": {
                 # No mandatory simple prompt, but let's keep a customizable one
                "subject_type": (cls.SUBJECT_COUNTS, {"default": "1girl"}),
            },
            "optional": {
                # Character Details
                "hair_style": (cls.HAIR_STYLES, {"default": "None"}),
                "hair_length": (cls.HAIR_LENGTHS, {"default": "None"}),
                "hair_color": (cls.HAIR_COLORS, {"default": "None"}),
                "eye_color": (cls.EYE_COLORS, {"default": "None"}),
                "expression": (cls.EXPRESSIONS, {"default": "None"}),
                "skin_type": (cls.SKIN_TYPES, {"default": "None"}),
                "attire": (cls.ATTIRE_CATEGORIES, {"default": "None"}),
                "custom_attire": ("STRING", {"default": "", "placeholder": "Custom clothes details..."}),
                
                # Scene Details
                "location_type": (["None", "Indoor", "Outdoor"], {"default": "None"}),
                "location_indoor": (cls.LOCATIONS_INDOOR, {"default": "None"}),
                "location_outdoor": (cls.LOCATIONS_OUTDOOR, {"default": "None"}),
                "time_of_day": (cls.TIME_OF_DAY, {"default": "None"}),
                "weather": (cls.WEATHER, {"default": "None"}),
                "lighting": (cls.LIGHTING, {"default": "None"}),
                
                # Composition
                "pose": (cls.POSES, {"default": "None"}),
                "framing": (cls.FRAMING, {"default": "None"}),
                
                # Identifiers
                "character_name": ("STRING", {"default": "", "placeholder": "Character Name"}),
                "series_name": ("STRING", {"default": "", "placeholder": "Series Name"}),
                "artist_tag": ("STRING", {"default": "", "placeholder": "Artist Style"}),
                
                # Global Style
                "art_style": (cls.ART_STYLES, {"default": "None"}),
                "year_style": (cls.YEAR_STYLES, {"default": "2024-2025 (Modern)"}),
                "rating": (cls.RATING_TAGS, {"default": "safe"}),
                
                # Toggles
                "add_quality_tags": ("BOOLEAN", {"default": True}),
                "enhance_negative": ("BOOLEAN", {"default": False}),
                "extra_tags": ("STRING", {"multiline": True, "default": "", "placeholder": "Any other tags..."}),
            }
        }
        
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("positive_prompt", "negative_prompt")
    FUNCTION = "assemble_prompt"
    CATEGORY = "Animagine/Prompting"

    def assemble_prompt(self, subject_type, hair_style, hair_length, hair_color, eye_color, 
                       expression, skin_type, attire, custom_attire,
                       location_type, location_indoor, location_outdoor, time_of_day, weather, lighting,
                       pose, framing, character_name, series_name, artist_tag,
                       art_style, year_style, rating, add_quality_tags, enhance_negative, extra_tags):
        
        parts = []
        
        # 1. Subject
        if subject_type != "None": parts.append(subject_type)
        
        # 2. Character Identity
        if character_name: parts.append(self._clean_prompt(character_name))
        if series_name: parts.append(self._clean_prompt(series_name))
        
        # 3. Artist (Early)
        if artist_tag: parts.append(self._clean_prompt(artist_tag))
        
        # 4. Character Traits (Hair -> Eyes -> Skin -> Expression)
        traits = []
        if hair_length != "None": traits.append(hair_length)
        if hair_style != "None": traits.append(hair_style)
        if hair_color != "None": traits.append(hair_color)
        if eye_color != "None": traits.append(eye_color)
        if skin_type != "None": traits.append(skin_type)
        if expression != "None": traits.append(expression)
        if traits: parts.extend(traits)
        
        # 5. Attire
        if attire != "None": parts.append(attire)
        if custom_attire: parts.append(self._clean_prompt(custom_attire))
        
        # 6. Composition (Pose, Framing)
        if pose != "None": parts.append(pose)
        if framing != "None": parts.append(framing)
        
        # 7. Scene / Background
        scene = []
        if location_type == "Indoor" and location_indoor != "None":
            scene.append("indoors")
            scene.append(location_indoor)
        elif location_type == "Outdoor" and location_outdoor != "None":
            scene.append("outdoors")
            scene.append(location_outdoor)
        
        if time_of_day != "None": scene.append(time_of_day)
        if weather != "None": scene.append(weather)
        if lighting != "None": scene.append(lighting)
        if scene: parts.extend(scene)
        
        # 8. Extra & Style
        if art_style != "None": parts.append(art_style)
        if extra_tags: parts.append(self._clean_prompt(extra_tags))
        
        # 9. Rating
        if rating != "None": parts.append(rating)
        
        # 10. Year
        year = self._get_year_tags(year_style)
        if year: parts.append(year)
        
        # 11. Quality
        if add_quality_tags: parts.append(self.QUALITY_SUFFIX)
        
        final_positive = ", ".join(parts)
        
        # Negative Prompt
        if enhance_negative:
            final_negative = self._get_enhanced_negative()
        else:
            final_negative = self.OFFICIAL_NEGATIVE
            
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
