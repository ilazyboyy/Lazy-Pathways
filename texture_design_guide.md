# Lazy Pathways - Standalone Texture Design Guide

## Design Philosophy
Create textures that look complete and natural as individual blocks, without requiring connection to neighboring blocks.

## Level Progression Design

### Level 1 - Fresh Path
- **Concept**: Light foot traffic on grass
- **Composition**: 80% grass, 20% light dirt
- **Pattern**: Subtle dirt spots in center, mostly grass
- **Colors**: Vibrant greens with light brown accents
- **Edge Treatment**: Full grass coverage on edges

### Level 2 - Overgrown Path ✅ (Your Custom Design)
- **Status**: Already implemented and looks great!
- **Concept**: Path being reclaimed by nature
- **Keep**: The overgrown aesthetic works well standalone

### Level 3 - Moderate Wear  
- **Concept**: Clear path formation
- **Composition**: 50% grass, 50% dirt
- **Pattern**: Central dirt path with grass borders
- **Colors**: Mix of grass green and earth brown
- **Edge Treatment**: Grass on edges, dirt in center

### Level 4 - Heavy Wear
- **Concept**: Well-established dirt path
- **Composition**: 20% grass, 80% dirt
- **Pattern**: Dirt dominates with grass patches
- **Colors**: Earth browns with sparse green
- **Edge Treatment**: Minimal grass, mostly dirt

### Level 5 - Maximum Wear
- **Concept**: Packed earth trail  
- **Composition**: 5% grass, 95% packed dirt
- **Pattern**: Almost pure dirt with tiny grass spots
- **Colors**: Deep earth tones, minimal green
- **Edge Treatment**: Consistent dirt across entire texture

## Standalone Design Tips

### ✅ DO:
- Use centered patterns that look complete
- Add subtle randomness for natural appearance  
- Create clear visual progression between levels
- Use self-contained designs that don't rely on neighbors
- Consider how textures look when tinted with grass colors

### ❌ DON'T:
- Create patterns that obviously need continuation
- Use edge-dependent designs (like your overgrown sides)
- Make textures too uniform or repetitive
- Forget about the grass tinting system we have

## Color Considerations
Remember: With our fixed tinting system:
- **Grass areas** (tintindex 0) will be colored by biome
- **Dirt areas** (no tintindex) will show true texture colors
- Design with this in mind for best results

## Testing Your Textures
1. Build the mod with new textures
2. Test in different biomes to see how grass tinting affects them
3. Place individual blocks to see standalone appearance
4. Create small path networks to check how they look together

## Texture Tools Recommendations
- **Aseprite** - Great for pixel art and animations
- **GIMP** - Free alternative with good pixel art tools
- **Photoshop** - Professional option with extensive tools
- **Paint.NET** - Windows-friendly middle ground

## File Format Notes
- Keep as 16x16 PNG files
- Use RGBA format for transparency if needed
- Optimize file size while maintaining quality
- Test in-game regularly during design process