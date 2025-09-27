# Texture Variants for Grass Blending

## Simplified Approach: 4 Main Patterns

Instead of creating 16 variants per level (which would be 80 textures total), let's start with the 4 most important patterns:

### Pattern Types Needed:

#### 1. **Standalone** (`_standalone`)
- **When**: No grass neighbors on any side
- **Design**: Sharp edges, self-contained path design
- **Use**: Isolated path blocks

#### 2. **Surrounded** (`_surrounded`) 
- **When**: Grass neighbors on all 4 sides
- **Design**: Grass edges on all sides, path center
- **Use**: Path blocks completely surrounded by grass

#### 3. **Horizontal** (`_horizontal`)
- **When**: Grass neighbors on North AND South (path runs East-West)
- **Design**: Grass edges on top/bottom, path edges on left/right
- **Use**: East-West running paths

#### 4. **Vertical** (`_vertical`)
- **When**: Grass neighbors on East AND West (path runs North-South)  
- **Design**: Grass edges on left/right, path edges on top/bottom
- **Use**: North-South running paths

## Texture Files Needed (20 total):

### Level 1:
- `path_level_1_standalone.png` - No grass neighbors
- `path_level_1_surrounded.png` - All grass neighbors  
- `path_level_1_horizontal.png` - North/South grass
- `path_level_1_vertical.png` - East/West grass

### Level 2:
- `path_level_2_standalone.png` - Current texture works for this!
- `path_level_2_surrounded.png` 
- `path_level_2_horizontal.png`
- `path_level_2_vertical.png`

### Level 3-5: 
- Same pattern for each level

## Blockstate Logic:

The blockstate will choose textures based on:

```
if (no grass neighbors) -> use _standalone
else if (all 4 grass neighbors) -> use _surrounded  
else if (north AND south grass) -> use _horizontal
else if (east AND west grass) -> use _vertical
else -> use _standalone (fallback for other combinations)
```

## Design Template:

Using your example pattern from the .md file:

### Standalone (Sharp Edges):
```
D D D D D D D D D D D D D D D D
D P P P P P P P P P P P P P P D  
D P T T T T T T T T T T T T P D
D P T T T T T T T T T T T T P D
D P T T T T C C C C T T T T P D
D P T T T C C C C C C T T T P D
D P T T C C C C C C C C T T P D
D P T T C C C C C C C C T T P D
D P T T C C C C C C C C T T P D
D P T T C C C C C C C C T T P D
D P T T T C C C C C C T T T P D
D P T T T T C C C C T T T T P D
D P T T T T T T T T T T T T P D
D P P P P P P P P P P P P P P D
D D D D D D D D D D D D D D D D
```

### Surrounded (Grass Edges):
```
G G G G G G G G G G G G G G G G
G g g g g g g g g g g g g g g G  
G g P P P P P P P P P P P P g G
G g P T T T T T T T T T T P g G
G g P T T T C C C C T T T P g G
G g P T T C C C C C C T T P g G
G g P T C C C C C C C C T P g G
G g P T C C C C C C C C T P g G
G g P T C C C C C C C C T P g G
G g P T C C C C C C C C T P g G
G g P T T C C C C C C T T P g G
G g P T T T C C C C T T T P g G
G g P P P P P P P P P P P P g G
G g g g g g g g g g g g g g g G
G G G G G G G G G G G G G G G G
```

**Legend:**
- G = Pure grass (tinted by biome)
- g = Light grass transition  
- P = Path edge
- T = Trail/worn area
- C = Center/most worn area
- D = Dirt/non-grass edge

This approach gives you the natural grass blending you want while keeping the texture count manageable!