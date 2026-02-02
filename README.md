# ComfyUI Animagine XL 4.0 Prompt Styler

A custom node pack for [ComfyUI](https://github.com/comfyanonymous/ComfyUI) that optimizes prompts for **Animagine XL 4.0 Opt**, following the official guidelines from [Cagliostro Lab](https://cagliostrolab.net/posts/optimizing-animagine-xl-40-in-depth-guideline-and-update).

## Features

- **Automatic Tag Ordering**: Enforces the correct tag sequence critical for Animagine XL 4.0
- **Quality Tags at END**: Automatically appends `masterpiece, high score, great score, absurdres` at the end (as required)
- **Official Negative Prompt**: Built-in optimized negative prompt from Cagliostro Lab
- **Temporal Steering**: Year tags for different anime art era styles (2000s retro to 2025 modern)
- **Character & Series Support**: Dedicated inputs for character/series tags (important for accuracy)
- **Artist Tag Placement**: Correct early placement of artist tags (not at the end)
- **Composition Helpers**: Dropdowns for poses, framing, backgrounds, and art styles
- **Rating Tags**: Support for safe, sensitive, nsfw, explicit ratings
- **Creature Generator**: Specialized node for cyborgs, robots, monsters with 300+ unique tags

## Installation

1. Navigate to your ComfyUI custom nodes folder:
   ```
   cd ComfyUI/custom_nodes/
   ```

2. Clone this repository:
   ```
   git clone https://github.com/YOUR_USERNAME/ComfyUI-Animagine-Prompt-Styler.git
   ```
   
   Or manually copy the folder into `custom_nodes/`

3. Restart ComfyUI

4. Find the nodes under **Animagine > Prompting** and **Animagine > Creatures** in the node menu

## File Structure

```
Anima/
├── __init__.py              # Node registration & web directory config
├── animagine_v4.py          # Main node classes
├── characters.csv           # Character database (editable)
├── web/
│   └── js/
│       └── animagine_autofill.js  # Auto-fill extension
└── ...
```

## Nodes

### Animagine XL 4.0 Prompt Styler (Advanced)

The full-featured node with structured inputs for optimal prompt generation.

**Inputs:**
| Input | Type | Description |
|-------|------|-------------|
| `simple_prompt` | String | Your main prompt (features, clothing, expressions, etc.) |
| `subject_count` | Dropdown | Number/type of subjects (1girl, 2boys, etc.) |
| `character_name` | String | Character name (e.g., `hatsune miku`) |
| `series_name` | String | Series/copyright (e.g., `vocaloid`) - **Important for characters!** |
| `artist_tag` | String | Artist style tag (e.g., `ciloranko`) |
| `pose` | Dropdown | Character pose options |
| `framing` | Dropdown | Camera framing (portrait, full body, etc.) |
| `background` | Dropdown | Background/setting options |
| `art_style` | Dropdown | Art style modifiers |
| `rating` | Dropdown | Content rating (safe, sensitive, nsfw, explicit) |
| `year_style` | Dropdown | Temporal era for art style |
| `add_quality_tags` | Boolean | Append quality suffix (recommended: ON) |
| `enhance_negative` | Boolean | Use extended negative prompt |
| `additional_positive` | String | Extra positive tags |
| `additional_negative` | String | Extra negative tags |

**Outputs:**
- `positive_prompt` - Fully optimized positive prompt
- `negative_prompt` - Official Cagliostro negative prompt

### Animagine XL 4.0 Character Factory (Expert)

The ultimate builder node for constructing detailed characters and scenes without manual tagging.

**Features:**
- **Character Traits**: Dropdowns for hair style, length, color, eye color, expression, and skin type.
- **Detailed Attire**: Massive selection of costumes (school uniform, maid, armor, etc.) + custom field.
- **Scene Builder**: Dedicated controls for Location (Indoor/Outdoor), Time of Day, Weather, and Lighting.
- **Smart Assembly**: Automatically combines all elements into the strict Animagine XL 4.0 tag order.
- **Character Database**: Dropdown selectors for Character Name, Series Name, and Artist Tag loaded from `characters.csv`
- **Auto-Fill**: When selecting a character, series and artist are automatically populated!

| Input Category | Available Options |
|----------------|-------------------|
| **Character** | Gender, Hair (Style/Color/Length), Eyes, Skin, Expression |
| **Attire** | 40+ presets (Uniforms, Fantasy, Casual) + Custom input |
| **Scene** | Indoor/Outdoor locations, Time, Weather, Lighting |
| **Style** | Artist tag dropdown, Art Style, Year Style, Rating |
| **Identity** | Character Name dropdown (30+ characters), Series Name dropdown (22+ series) |

### Animagine XL 4.0 Creature Styler (Cyborg/Robot/Monster)

A specialized node for generating cyborgs, robots, monsters, and other creatures with unique visual aesthetics.

**Features:**
- **Creature Types**: 40+ creature options including cyborg, android, robot, mecha, gynoid, monster girl/boy, demon, succubus, angel, vampire, zombie, werewolf, ghost, alien, slime, dragon, lamia, harpy, eldritch/lovecraftian, golem, elemental
- **Mechanical Features**: Mechanical limbs, cyber eyes, exposed machinery, chrome body, LED lights, holographic displays, energy cores, weapon systems, damaged/rusted metal, neon accents
- **Monster Features**: Horns, wings (demon/angel/bat/insect), tails, claws, fangs, tentacles, scales, fur, multiple eyes/arms, auras, halos, unusual skin colors
- **Visual Styles**: Cyberpunk, synthwave, vaporwave, neon glow, holographic, glitch art, dark fantasy, gothic, eldritch, bioluminescent, celestial, steampunk, dieselpunk, biomechanical, post-apocalyptic
- **Creature Environments**: Cyberpunk city, space station, server room, junkyard, haunted mansion, hell/underworld, enchanted forest, floating islands, wasteland
- **Creature Attire**: Power armor, exosuit, plugsuit, space suit, dark armor, bone armor, eldritch robes, gothic dress
- **Weapons/Accessories**: Energy swords, laser guns, plasma rifles, scythes, magic staffs, grimoires, masks, visors, cloaks
- **Dynamic Poses**: Fighting stance, attacking, transformation, feeding, flying, roaring, channeling energy, powering up

| Input Category | Options Count |
|----------------|---------------|
| **Creature Types** | 40+ |
| **Mechanical Features** | 45+ |
| **Monster Features** | 55+ |
| **Visual Styles** | 80+ |
| **Environments** | 50+ |
| **Attire** | 40+ |
| **Weapons/Accessories** | 45+ |
| **Poses** | 35+ |

### Animagine XL 4.0 Prompt Manager (Simple)

A simpler node for quick prompting with just text input and year selection.

## Tag Ordering (Critical!)

Animagine XL 4.0 was trained with a specific tag order. This node automatically enforces:

1. **Subject count** (1girl, 1boy, etc.)
2. **Character name** (if applicable)
3. **Series/copyright name** (mandatory for character accuracy)
4. **Artist tag** (placed early, NOT at the end)
5. **General tags** (features, clothing, pose, setting)
6. **Rating tag** (safe, sensitive, nsfw, explicit)
7. **Year tags** (temporal styling)
8. **Quality tags at the END** ← This is mandatory!

## Example

**Input:**
- simple_prompt: `long hair, blue eyes, white dress, smiling`
- subject_count: `1girl`
- character_name: `hatsune miku`
- series_name: `vocaloid`
- rating: `safe`
- year_style: `2024-2025 (Modern)`

**Output:**
```
Positive: 1girl, hatsune miku, vocaloid, long hair, blue eyes, white dress, smiling, safe, year 2024, year 2025, masterpiece, high score, great score, absurdres

Negative: lowres, bad anatomy, bad hands, text, error, missing finger, extra digits, fewer digits, cropped, worst quality, low quality, low score, bad score, average score, signature, watermark, username, blurry
```

## Recommended Sampler Settings

For optimal results with Animagine XL 4.0 Opt:

| Setting | Recommended Value |
|---------|-------------------|
| Sampler | `euler_ancestral` or `euler_a` |
| Scheduler | `normal` or `sgm_uniform` |
| Steps | 25-28 |
| CFG Scale | 5.0 - 7.0 (start with 5.0) |
| Resolution | 1024x1024 (SDXL native) |

## Year Styles (Temporal Steering)

The model supports temporal tags to emulate different anime art eras:

| Style | Years | Aesthetic |
|-------|-------|-----------|
| Modern | 2024-2025 | Current digital art, volumetric lighting, high detail |
| Recent | 2020-2023 | Modern anime style |
| Mid-Era | 2015-2019 | Transitional digital era |
| Classic | 2010-2014 | Early HD anime style |
| Retro | 2005-2009 | Mid-2000s aesthetic, cell shading |
| Early Digital | 2000-2004 | Early digital anime art |

## Customizing the Character Database

You can add your own characters by editing `characters.csv`:

```csv
character_name,series_name,artist_tag
Your Character,Your Series,artist_name
```

After editing, also update `web/js/animagine_autofill.js` to include the new character in the `CHARACTER_MAPPING` object for auto-fill to work:

```javascript
"Your Character": { series: "Your Series", artist: "artist_name" },
```

Then restart ComfyUI.

## References

- [Animagine XL 4.0 on Hugging Face](https://huggingface.co/cagliostrolab/animagine-xl-4.0)
- [Cagliostro Lab Optimization Guide](https://cagliostrolab.net/posts/optimizing-animagine-xl-40-in-depth-guideline-and-update)
- [Animagine XL 4.0 on Civitai](https://civitai.com/models/animagine-xl-4)

## License

MIT License

## Credits

- **Animagine XL 4.0** by [Cagliostro Research Lab](https://cagliostrolab.net/)
- Optimization guidelines from official Cagliostro Lab documentation
