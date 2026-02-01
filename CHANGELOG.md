# Changelog

All notable changes to ComfyUI Animagine XL 4.0 Prompt Styler will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.3.0] - 2026-02-01

### Added
- **New Node: AnimagineXL4_Creature_Styler (Cyborg/Robot/Monster)**
  - Specialized creature generator for non-human and hybrid characters
  - 40+ creature types: cyborg, android, robot, mecha, gynoid, monster girl/boy, demon, succubus, angel, vampire, zombie, werewolf, ghost, alien, slime, dragon, lamia, harpy, eldritch/lovecraftian, golem, elemental
  - 45+ mechanical features: mechanical limbs, cyber eyes, chrome body, LED lights, holographic displays, energy cores, weapon systems, neon accents
  - 55+ monster features: horns, wings, tails, claws, fangs, tentacles, scales, multiple eyes/arms, auras, halos
  - 80+ visual styles: cyberpunk, synthwave, vaporwave, dark fantasy, gothic, eldritch, bioluminescent, steampunk, dieselpunk, biomechanical
  - 50+ creature-specific environments: cyberpunk city, space station, haunted mansion, hell/underworld, enchanted forest
  - 40+ creature attire options: power armor, exosuit, plugsuit, dark armor, bone armor, eldritch robes
  - 45+ weapons/accessories: energy swords, laser guns, scythes, magic staffs, grimoires, masks
  - 35+ dynamic poses: fighting stance, transformation, channeling energy, powering up
  - Secondary feature slots for combining mechanical + monster traits
  - Custom feature and scene text inputs for flexibility
  - Located under **Animagine > Creatures** category

### Changed
- Updated node mappings to include all four node classes
- Added creature-specific enhanced negative prompt option

## [1.2.0] - 2026-02-01

### Added
- **New Node: AnimagineXL4_Character_Factory (Expert)**
  - Comprehensive character builder with specific dropdowns for hair, eyes, skin, and expression
  - Detailed attire selector with 40+ presets and custom override
  - Scene builder with dedicated Location, Time, Weather, and Lighting controls
  - Massive internal text database of common anime tags
  - Inherits strict tag ordering logic from the Styler node

### Changed
- Updated `__init__.py` to export all three node tiers (Simple, Standard, Expert)
- Refactored internal constant lists into the new Factory class for better organization

## [1.1.0] - 2026-02-01

### Added
- **New Node: AnimagineXL4_Prompt_Styler (Advanced)**
  - Structured inputs for proper tag ordering per Cagliostro Lab guidelines
  - Subject count dropdown (1girl, 2boys, multiple characters, no humans, etc.)
  - Dedicated character name input field
  - Series/copyright name input (critical for character accuracy)
  - Artist tag input with correct early placement
  - Pose dropdown with 24 common pose options
  - Framing/camera angle dropdown (portrait, cowboy shot, full body, etc.)
  - Background dropdown with 45+ indoor/outdoor/abstract options
  - Art style dropdown (cel shading, painterly, watercolor, etc.)
  - Rating tag dropdown (safe, sensitive, nsfw, explicit)
  - Extended year style options (2000-2004 through 2024-2025)
  - Enhanced negative prompt toggle for additional quality control
  - Additional positive/negative input fields for custom tags

### Changed
- Renamed original node to "Animagine XL 4.0 Prompt Manager (Simple)" for clarity
- Fixed syntax error in style_year dropdown (was empty tuple)
- Refactored code structure with helper methods for cleaner tag processing
- Improved prompt cleaning and normalization

### Fixed
- Empty tuple syntax error in `INPUT_TYPES` for `style_year` parameter
- Proper handling of trailing/leading commas in prompts
- Whitespace normalization in tag processing

## [1.0.0] - 2026-01-15

### Added
- Initial release of AnimagineXL4_Prompt_Manager
- Basic text input for prompts
- Year style dropdown for temporal steering
- Quality tags toggle
- Official Cagliostro Lab negative prompt
- Automatic quality suffix appending (`masterpiece, high score, great score, absurdres`)

---

## Upgrade Notes

### From 1.2.0 to 1.3.0

New `AnimagineXL4_Creature_Styler` node added for generating creatures. Existing workflows are unaffected.

Use the Creature Styler when you want to generate:
- Cyborgs and androids with mechanical features
- Robots and mecha characters
- Monsters, demons, angels, vampires, and other fantasy creatures
- Unique visual aesthetics like cyberpunk, gothic, eldritch, or bioluminescent

### From 1.0.0 to 1.1.0

The original `AnimagineXL4_Prompt_Manager` node is preserved for backward compatibility. Existing workflows will continue to work.

For new workflows, we recommend using the new `AnimagineXL4_Prompt_Styler` node which provides:
- Proper tag ordering enforcement
- Structured character/series inputs
- Artist tag support with correct placement
- More composition options

Both nodes output the same format (`positive_prompt`, `negative_prompt`) and can be used interchangeably with CLIP Text Encode nodes.
