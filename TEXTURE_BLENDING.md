# Texture Blending Feature

The Lazy Pathways mod now includes an intelligent texture blending system that makes your pathways blend seamlessly with neighboring blocks for a more natural look.

## How It Works

The blending system analyzes the blocks immediately surrounding each path block (North, South, East, West) and subtly mixes their colors with the path's base grass color. This creates smooth transitions between your paths and different terrain types.

## Supported Block Types

The system recognizes and blends with many common Minecraft blocks:

- **Natural blocks**: Grass, dirt, sand, gravel, snow, mycelium, podzol
- **Stone blocks**: Stone, cobblestone, stone bricks
- **Building blocks**: Wood planks, clay, terracotta
- **Path blocks**: Vanilla dirt paths and other path blocks

## Configuration Options

### Enable Texture Blending
- **Default**: `true`
- **Description**: Master toggle for the entire blending system
- Turn this off if you prefer the original uniform path appearance

### Blending Intensity
- **Default**: `0.4` (40% neighbor influence)
- **Range**: `0.1` to `1.0`
- **Description**: Controls how strongly neighboring block colors influence the path
  - `0.1` = Very subtle blending, paths remain mostly their original color
  - `0.4` = Moderate blending (recommended)
  - `1.0` = Strong blending, paths heavily adopt neighbor colors

## Dynamic Behavior

- **Path Level Influence**: Higher wear levels (more worn paths) blend less with neighbors, representing compacted earth
- **Performance Optimized**: Uses intelligent caching to prevent performance impact
- **Biome Aware**: Base colors still respect biome grass colors
- **Memory Safe**: Automatic cache cleanup prevents memory leaks

## Tips for Best Results

1. **Moderate Settings**: The default `0.4` intensity provides good balance between blending and path visibility
2. **Path Networks**: Blending works best when paths connect different terrain types
3. **Building Integration**: Paths will naturally blend with stone, wood, and clay structures
4. **Snow Compatibility**: Paths in snowy areas will take on a subtle white tint

## Technical Details

The blending system:
- Samples colors from the 4 horizontal neighbors
- Calculates weighted averages based on configuration
- Applies biome-appropriate base colors
- Caches results for performance
- Updates automatically when terrain changes

This creates truly dynamic pathways that feel integrated into your world's landscape!
