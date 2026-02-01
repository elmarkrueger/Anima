# Changelog

All notable changes to ComfyUI Animagine XL 4.0 Prompt Styler will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

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

### From 1.0.0 to 1.1.0

The original `AnimagineXL4_Prompt_Manager` node is preserved for backward compatibility. Existing workflows will continue to work.

For new workflows, we recommend using the new `AnimagineXL4_Prompt_Styler` node which provides:
- Proper tag ordering enforcement
- Structured character/series inputs
- Artist tag support with correct placement
- More composition options

Both nodes output the same format (`positive_prompt`, `negative_prompt`) and can be used interchangeably with CLIP Text Encode nodes.
