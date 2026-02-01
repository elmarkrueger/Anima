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
        simple_prompt,
        subject_count="1girl",
        character_name="",
        series_name="",
        artist_tag="",
        pose="None",
        framing="None",
        background="None",
        art_style="None",
        rating="safe",
        year_style="2024-2025 (Modern)",
        add_quality_tags=True,
        enhance_negative=False,
        additional_positive="",
        additional_negative="",
    ):
        """Build optimized prompts following Cagliostro Lab tag ordering."""
        parts = []
        
        # 1. Subject count
        if subject_count != "None":
            parts.append(subject_count)
        
        # 2. Character name
        if character_name:
            parts.append(self._clean_prompt(character_name))
        
        # 3. Series name
        if series_name:
            parts.append(self._clean_prompt(series_name))
        
        # 4. Artist tag (early position)
        if artist_tag:
            parts.append(self._clean_prompt(artist_tag))
        
        # 5. General tags (user prompt)
        if simple_prompt:
            cleaned = self._clean_prompt(simple_prompt)
            if cleaned and cleaned != "Enter your simple prompt here...\n(features, clothing, actions, expressions, etc.)":
                parts.append(cleaned)
        
        # Composition
        if pose != "None":
            parts.append(pose)
        if framing != "None":
            parts.append(framing)
        if background != "None":
            parts.append(background)
        if art_style != "None":
            parts.append(art_style)
        
        # Additional positive tags
        if additional_positive:
            parts.append(self._clean_prompt(additional_positive))
        
        # 6. Rating
        if rating != "None":
            parts.append(rating)
        
        # Year tags
        year_tags = self._get_year_tags(year_style)
        if year_tags:
            parts.append(year_tags)
        
        # 7. Quality tags at the END
        if add_quality_tags:
            parts.append(self.QUALITY_SUFFIX)
        
        final_positive = ", ".join(parts)
        
        # Negative prompt
        if enhance_negative:
            final_negative = self._get_enhanced_negative()
        else:
            final_negative = self.OFFICIAL_NEGATIVE
        
        if additional_negative:
            final_negative = f"{final_negative}, {self._clean_prompt(additional_negative)}"
        
        return (final_positive, final_negative)


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



class AnimagineXL4_Creature_Styler:
    """
    Specialized Creature & Style Generator for Animagine XL 4.0
    Create cyborgs, robots, monsters, and apply unique visual aesthetics.
    """
    
    QUALITY_SUFFIX = "masterpiece, high score, great score, absurdres"
    OFFICIAL_NEGATIVE = (
        "lowres, bad anatomy, bad hands, text, error, missing finger, "
        "extra digits, fewer digits, cropped, worst quality, low quality, "
        "low score, bad score, average score, signature, watermark, username, blurry"
    )
    
    # === CREATURE TYPES ===
    CREATURE_TYPES = [
        "None",
        # Humanoid
        "1girl", "1boy", "1other",
        # Mechanical
        "android", "cyborg", "robot", "mecha", "mecha musume", "gynoid", "combat android",
        "humanoid robot", "battle android", "robot girl", "robot boy",
        # Monsters & Creatures
        "monster", "monster girl", "monster boy", "creature", "beast", "chimera",
        "demon", "demon girl", "succubus", "incubus", "devil",
        "angel", "fallen angel", "cherub", "seraph",
        "vampire", "vampire girl", "nosferatu",
        "zombie", "undead", "lich", "skeleton", "revenant",
        "werewolf", "wolfgirl", "kemonomimi", "nekomimi", "kitsune", "inumimi",
        "ghost", "wraith", "specter", "phantom", "spirit",
        "alien", "extraterrestrial", "xenomorph-like",
        "slime", "slime girl", "dryad", "nymph", "fairy", "pixie",
        "dragon", "dragonkin", "half-dragon", "lamia", "harpy", "centaur", "mermaid",
        "eldritch", "lovecraftian", "cosmic horror", "aberration",
        "golem", "elemental", "fire elemental", "water elemental", "shadow creature",
    ]
    
    # === MECHANICAL FEATURES (Cyborgs/Robots) ===
    MECHANICAL_FEATURES = [
        "None",
        "mechanical arms", "mechanical legs", "mechanical body", "mechanical wings",
        "robotic limbs", "robotic eyes", "robotic tail", "cybernetic implants",
        "cyber eye", "glowing eyes", "scanner visor", "targeting reticle",
        "exposed machinery", "visible gears", "visible circuits", "wire frame",
        "chrome body", "metallic skin", "polished metal", "brushed steel",
        "LED lights", "glowing panels", "holographic displays", "data streams",
        "cables", "wires", "tubes", "hydraulics", "pistons",
        "antenna", "sensor array", "satellite dish", "radar dome",
        "energy core", "power cell", "reactor core", "glowing chest",
        "exhaust vents", "cooling fans", "steam vents", "heat sinks",
        "weapon systems", "built-in weapons", "arm cannon", "laser emitter",
        "force field", "energy shield", "barrier generator",
        "damaged machinery", "battle damage", "rust", "patina", "aged metal",
        "neon accents", "light trails", "energy lines", "circuit patterns",
    ]
    
    # === MONSTER FEATURES ===
    MONSTER_FEATURES = [
        "None",
        # Body Parts
        "horns", "demon horns", "ram horns", "dragon horns", "antlers",
        "wings", "demon wings", "bat wings", "angel wings", "feathered wings", "insect wings", "mechanical wings",
        "tail", "demon tail", "dragon tail", "cat tail", "wolf tail", "snake tail", "scorpion tail",
        "claws", "sharp claws", "talons", "elongated nails",
        "fangs", "sharp teeth", "multiple rows of teeth", "tusks",
        "forked tongue", "long tongue", "serpent tongue",
        "pointed ears", "elf ears", "long ears", "bat ears",
        "multiple eyes", "third eye", "compound eyes", "no eyes", "glowing eyes", "heterochromia",
        "multiple arms", "multiple limbs", "extra arms", "tentacles", "tentacle hair",
        "scales", "dragon scales", "snake scales", "armored skin",
        "fur", "fluffy", "fuzzy", "feathers", "shell", "exoskeleton", "carapace",
        "spikes", "bone spikes", "dorsal spines", "quills",
        "aura", "dark aura", "fire aura", "energy aura", "miasma", "shadow tendrils",
        "halo", "broken halo", "dark halo", "multiple halos",
        "ethereal", "translucent body", "ghostly", "spectral", "incorporeal",
        "stitches", "scars", "exposed bone", "rotting flesh",
        "unusual skin color", "pale skin", "grey skin", "blue skin", "green skin", "red skin", "purple skin",
    ]
    
    # === VISUAL AESTHETICS/STYLES ===
    VISUAL_STYLES = [
        "None",
        # Cyberpunk/Tech
        "cyberpunk", "synthwave", "vaporwave", "retrowave", "outrun aesthetic",
        "neon", "neon lights", "neon glow", "neon city", "neon signs",
        "holographic", "iridescent", "chromatic", "prismatic",
        "glitch art", "pixel glitch", "data moshing", "databend",
        "matrix code", "digital rain", "binary", "circuit board aesthetic",
        "wireframe", "low poly", "vector art", "geometric",
        # Dark/Gothic
        "dark fantasy", "gothic", "victorian gothic", "dark academia",
        "eldritch", "lovecraftian", "cosmic horror", "body horror",
        "macabre", "grim dark", "dark souls aesthetic", "bloodborne aesthetic",
        "horror", "creepy", "unsettling", "nightmare fuel",
        # Ethereal/Magical
        "ethereal", "dreamy", "surreal", "otherworldly", "mystical",
        "magical", "arcane", "occult", "witchy aesthetic",
        "bioluminescent", "phosphorescent", "glowing", "radiant",
        "celestial", "astral", "cosmic", "starry", "galaxy",
        "aurora", "northern lights", "plasma", "energy",
        # Industrial/Mechanical
        "steampunk", "dieselpunk", "clockpunk", "atompunk",
        "industrial", "brutalist", "utilitarian", "militaristic",
        "post-apocalyptic", "wasteland", "rusted", "decayed",
        "biopunk", "organic machinery", "biomechanical", "giger-esque",
        # Artistic Styles
        "art nouveau", "art deco", "ukiyo-e", "traditional japanese",
        "impressionistic", "expressionistic", "surrealist", "abstract",
        "minimalist", "maximalist", "baroque", "rococo",
        "stained glass", "mosaic", "fresco", "mural",
        # Color Themes
        "monochrome", "high contrast", "desaturated", "oversaturated",
        "warm colors", "cool colors", "pastel colors", "neon colors",
        "color splash", "selective color", "duotone", "tritone",
        # Lighting/Atmosphere
        "dramatic lighting", "chiaroscuro", "tenebrism", "rim lighting",
        "god rays", "crepuscular rays", "volumetric light", "atmospheric",
        "foggy", "misty", "hazy", "smoky", "dusty particles",
    ]
    
    # === ENVIRONMENTS ===
    CREATURE_ENVIRONMENTS = [
        "None",
        # Tech/Sci-fi
        "cyberpunk city", "neon-lit streets", "futuristic cityscape", "megacity",
        "space station", "spaceship interior", "spacecraft bridge", "cryo chamber",
        "server room", "data center", "laboratory", "research facility",
        "factory", "assembly line", "manufacturing plant", "power plant",
        "junkyard", "scrapyard", "robot graveyard", "tech wasteland",
        # Dark/Horror
        "dark forest", "dead forest", "corrupted forest", "haunted woods",
        "graveyard", "cemetery", "crypt", "mausoleum", "catacombs",
        "haunted mansion", "abandoned asylum", "ruined castle", "dark cathedral",
        "hell", "hellscape", "inferno", "underworld", "abyss", "void",
        "limbo", "purgatory", "spirit realm", "shadow realm",
        # Fantasy
        "enchanted forest", "fairy realm", "magical kingdom", "crystal cave",
        "floating islands", "sky realm", "cloud city", "celestial palace",
        "underwater kingdom", "ocean depths", "coral reef", "sunken ruins",
        "volcanic lair", "dragon's den", "demon realm", "eldritch dimension",
        # Wasteland/Post-Apocalyptic
        "wasteland", "desert ruins", "nuclear wasteland", "post-apocalyptic city",
        "overgrown ruins", "abandoned city", "flooded city", "frozen wasteland",
    ]
    
    # === CLOTHING/ARMOR ===
    CREATURE_ATTIRE = [
        "None",
        # Mechanical/Tech
        "power armor", "exosuit", "mech suit", "combat armor", "tactical gear",
        "plugsuit", "bodysuit", "latex suit", "rubber suit", "wetsuit",
        "space suit", "pilot suit", "containment suit", "hazmat suit",
        "cyberpunk outfit", "tech wear", "utility vest", "tactical harness",
        "holographic clothing", "energy clothes", "hard light outfit",
        # Monster/Fantasy
        "dark armor", "demon armor", "corrupted armor", "bone armor", "chitin armor",
        "eldritch robes", "cultist robes", "ritual garments", "ceremonial dress",
        "tattered clothes", "ragged clothes", "bandages", "wrappings",
        "chains", "shackles", "collar", "restraints",
        "regal attire", "royal dress", "noble outfit", "aristocratic clothes",
        "tribal outfit", "primitive clothes", "fur clothing", "leather armor",
        "gothic dress", "victorian dress", "witch outfit", "dark priestess",
        "angelic robes", "divine garments", "holy vestments", "celestial dress",
        "naked", "nude", "minimal clothing", "strategic covering",
    ]
    
    # === WEAPONS/ACCESSORIES ===
    WEAPONS_ACCESSORIES = [
        "None",
        # Ranged
        "laser gun", "plasma rifle", "energy weapon", "blaster", "ray gun",
        "sniper rifle", "assault rifle", "submachine gun", "handgun", "revolver",
        # Melee
        "energy sword", "beam saber", "plasma blade", "laser blade",
        "katana", "longsword", "greatsword", "dual blades", "dagger",
        "scythe", "war scythe", "death scythe",
        "axe", "battle axe", "halberd", "spear", "trident",
        "claws", "gauntlets", "brass knuckles", "spiked fists",
        # Magic/Fantasy
        "staff", "magic staff", "wizard staff", "scepter", "wand",
        "grimoire", "spellbook", "tome", "scroll",
        "orb", "crystal ball", "magic orb", "soul gem",
        # Accessories
        "visor", "helmet", "mask", "gas mask", "oni mask", "skull mask",
        "goggles", "cyber goggles", "steampunk goggles",
        "headphones", "earpiece", "neural interface",
        "cape", "cloak", "hooded cloak", "tattered cape",
        "jewelry", "amulet", "pendant", "choker", "collar", "circlet", "crown", "tiara",
    ]
    
    # === POSES/ACTIONS ===
    CREATURE_POSES = [
        "None",
        "standing", "floating", "hovering", "levitating",
        "sitting", "kneeling", "crouching", "lying down",
        "walking", "running", "charging", "lunging",
        "fighting stance", "battle stance", "combat pose", "action pose",
        "attacking", "slashing", "shooting", "casting spell",
        "defensive pose", "blocking", "guarding", "shielding",
        "intimidating pose", "menacing", "looming", "towering over",
        "transformation", "transforming", "emerging", "awakening",
        "feeding", "hunting", "stalking", "prowling",
        "flying", "soaring", "diving", "descending",
        "screaming", "roaring", "howling", "shrieking",
        "praying", "meditating", "channeling energy", "summoning",
        "damaged", "injured", "wounded", "dying",
        "powering up", "charging energy", "releasing energy", "energy burst",
    ]
    
    # === FRAMING ===
    FRAMING_OPTIONS = [
        "None",
        "portrait", "bust", "upper body", "cowboy shot", "full body",
        "close-up", "extreme close-up", "face focus", "eye focus",
        "from above", "from below", "from side", "from behind",
        "dutch angle", "tilted frame", "dynamic angle",
        "wide shot", "establishing shot", "panoramic",
        "pov", "first person view", "over shoulder",
        "symmetrical", "centered", "rule of thirds", "golden ratio",
    ]
    
    # === RATINGS ===
    RATING_TAGS = ["None", "safe", "sensitive", "nsfw", "explicit"]
    
    # === YEAR STYLES ===
    YEAR_STYLES = [
        "None",
        "2024-2025 (Modern)",
        "2020-2023 (Recent)",
        "2015-2019 (Mid-Era)",
        "2010-2014 (Classic)",
    ]
    
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "creature_type": (cls.CREATURE_TYPES, {"default": "cyborg"}),
            },
            "optional": {
                # Visual Style
                "visual_style": (cls.VISUAL_STYLES, {"default": "cyberpunk"}),
                "secondary_style": (cls.VISUAL_STYLES, {"default": "None"}),
                
                # Creature Features
                "mechanical_features": (cls.MECHANICAL_FEATURES, {"default": "None"}),
                "secondary_mech_feature": (cls.MECHANICAL_FEATURES, {"default": "None"}),
                "monster_features": (cls.MONSTER_FEATURES, {"default": "None"}),
                "secondary_monster_feature": (cls.MONSTER_FEATURES, {"default": "None"}),
                
                # Appearance
                "attire": (cls.CREATURE_ATTIRE, {"default": "None"}),
                "weapon_accessory": (cls.WEAPONS_ACCESSORIES, {"default": "None"}),
                
                # Scene
                "environment": (cls.CREATURE_ENVIRONMENTS, {"default": "None"}),
                
                # Composition
                "pose": (cls.CREATURE_POSES, {"default": "None"}),
                "framing": (cls.FRAMING_OPTIONS, {"default": "None"}),
                
                # Artist/Style Override
                "artist_tag": ("STRING", {
                    "default": "",
                    "placeholder": "e.g., wlop, sakimichan, greg rutkowski"
                }),
                
                # Custom Tags
                "custom_features": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "Additional creature features..."
                }),
                "custom_scene": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "Additional scene details..."
                }),
                
                # Controls
                "year_style": (cls.YEAR_STYLES, {"default": "2024-2025 (Modern)"}),
                "rating": (cls.RATING_TAGS, {"default": "safe"}),
                "add_quality_tags": ("BOOLEAN", {"default": True}),
                "enhance_negative": ("BOOLEAN", {"default": True}),
            }
        }
    
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("positive_prompt", "negative_prompt")
    FUNCTION = "generate_creature_prompt"
    CATEGORY = "Animagine/Creatures"
    
    def _clean_tag(self, tag: str) -> str:
        tag = tag.strip()
        while tag.endswith(","):
            tag = tag[:-1].strip()
        while tag.startswith(","):
            tag = tag[1:].strip()
        return tag
    
    def _clean_prompt(self, prompt: str) -> str:
        if not prompt:
            return ""
        prompt = " ".join(prompt.split())
        prompt = prompt.replace(" ,", ",").replace(",  ", ", ").replace(",,", ",")
        prompt = self._clean_tag(prompt)
        return prompt
    
    def _get_year_tags(self, year_style: str) -> str:
        year_mappings = {
            "2024-2025 (Modern)": "year 2024, year 2025",
            "2020-2023 (Recent)": "year 2020, year 2022, year 2023",
            "2015-2019 (Mid-Era)": "year 2016, year 2018",
            "2010-2014 (Classic)": "year 2011, year 2013",
        }
        return year_mappings.get(year_style, "")
    
    def _get_enhanced_negative(self) -> str:
        creature_negative = (
            "jpeg artifacts, compression artifacts, pixelated, "
            "deformed, distorted, disfigured, mutation, mutated, "
            "ugly, duplicate, morbid, out of frame, poorly drawn face, "
            "poorly drawn hands, extra limbs, malformed limbs, "
            "fused fingers, too many fingers, long neck, amateur, "
            "poorly drawn, bad proportions, gross proportions, "
            "cloned face, body out of frame, cut off, censored, "
            "mosaic censoring, asymmetric, unfinished, draft"
        )
        return f"{self.OFFICIAL_NEGATIVE}, {creature_negative}"
    
    def generate_creature_prompt(
        self,
        creature_type,
        visual_style="None",
        secondary_style="None",
        mechanical_features="None",
        secondary_mech_feature="None",
        monster_features="None",
        secondary_monster_feature="None",
        attire="None",
        weapon_accessory="None",
        environment="None",
        pose="None",
        framing="None",
        artist_tag="",
        custom_features="",
        custom_scene="",
        year_style="2024-2025 (Modern)",
        rating="safe",
        add_quality_tags=True,
        enhance_negative=True,
    ):
        parts = []
        
        # 1. Creature Type (Subject)
        if creature_type != "None":
            parts.append(creature_type)
        
        # 2. Artist (Early position per guidelines)
        if artist_tag:
            parts.append(self._clean_prompt(artist_tag))
        
        # 3. Visual Styles
        if visual_style != "None":
            parts.append(visual_style)
        if secondary_style != "None":
            parts.append(secondary_style)
        
        # 4. Creature Features
        if mechanical_features != "None":
            parts.append(mechanical_features)
        if secondary_mech_feature != "None":
            parts.append(secondary_mech_feature)
        if monster_features != "None":
            parts.append(monster_features)
        if secondary_monster_feature != "None":
            parts.append(secondary_monster_feature)
        
        # 5. Custom Features
        if custom_features:
            parts.append(self._clean_prompt(custom_features))
        
        # 6. Attire & Accessories
        if attire != "None":
            parts.append(attire)
        if weapon_accessory != "None":
            parts.append(weapon_accessory)
        
        # 7. Composition
        if pose != "None":
            parts.append(pose)
        if framing != "None":
            parts.append(framing)
        
        # 8. Environment/Scene
        if environment != "None":
            parts.append(environment)
        if custom_scene:
            parts.append(self._clean_prompt(custom_scene))
        
        # 9. Rating
        if rating != "None":
            parts.append(rating)
        
        # 10. Year Style
        year_tags = self._get_year_tags(year_style)
        if year_tags:
            parts.append(year_tags)
        
        # 11. Quality Tags (End)
        if add_quality_tags:
            parts.append(self.QUALITY_SUFFIX)
        
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
    "AnimagineXL4_Character_Factory": AnimagineXL4_Character_Factory,
    "AnimagineXL4_Creature_Styler": AnimagineXL4_Creature_Styler,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AnimagineXL4_Prompt_Styler": "Animagine XL 4.0 Prompt Styler (Advanced)",
    "AnimagineXL4_Prompt_Manager": "Animagine XL 4.0 Prompt Manager (Simple)",
    "AnimagineXL4_Character_Factory": "Animagine XL 4.0 Character Factory",
    "AnimagineXL4_Creature_Styler": "Animagine XL 4.0 Creature Styler (Cyborg/Robot/Monster)",
}
