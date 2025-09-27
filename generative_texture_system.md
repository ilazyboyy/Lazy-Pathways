# Generative Connected Texture System

## 🎯 **The Smart Approach**

Instead of manually creating 4 texture variants for each path level, we can automatically generate them from the existing textures using simple edge modification rules.

## 🛠️ **How It Works**

### **Step 1: Identify Edge Zones**
For any 16x16 texture, we define edge zones:
- **Edge pixels**: Row/column 0 and 15 (outermost border)  
- **Transition pixels**: Row/column 1 and 14 (inner border)
- **Core pixels**: Everything else (untouched)

### **Step 2: Grass-ification Rules**
When generating a "grass-adjacent" edge:

1. **Edge pixels (0, 15)**: Replace with grass-like colors
2. **Transition pixels (1, 14)**: Blend original color with grass
3. **Core pixels**: Leave unchanged

### **Step 3: Generation Patterns**

#### **Standalone** (no grass neighbors)
```
Original texture unchanged
```

#### **Surrounded** (all grass neighbors)
```
Grass-ify: Top, Bottom, Left, Right edges
```

#### **Horizontal** (North+South grass)
```
Grass-ify: Top, Bottom edges only
Keep original: Left, Right edges
```

#### **Vertical** (East+West grass)
```
Grass-ify: Left, Right edges only  
Keep original: Top, Bottom edges
```

## 🎨 **Color Transformation Logic**

### **Grass Edge Colors:**
- **Pure grass edge**: `#7CB342` (gets biome tinting)
- **Grass transition**: Original color × 0.7 + grass color × 0.3
- **Preserve dirt/path areas**: Don't change brown/dirt colored pixels

### **Smart Edge Detection:**
```python
def should_grassify_pixel(original_color, position):
    # Don't grassify if it's already very dark (dirt/mud)
    if brightness(original_color) < 0.3:
        return False
    
    # Don't grassify pure path colors  
    if is_path_color(original_color):
        return False
        
    # Grassify lighter pixels that could represent grass/vegetation
    return True
```

## 🔧 **Implementation Approach**

### **Option A: Build-Time Generation (Recommended)**
Generate texture variants during the mod build process:

1. **Gradle Task**: Add a texture processing task to build.gradle
2. **Python/Java Script**: Process existing textures and generate variants
3. **Output**: Create the 4 variants automatically for each level

### **Option B: Resource Pack Generation**
Create a simple script you run manually:

1. **Texture Processor Script**: Reads existing textures
2. **Applies Rules**: Generates variants based on grass-blending rules
3. **Outputs Files**: Saves variants back to texture folder

### **Option C: Runtime Generation (Advanced)**
Generate textures in-game using Fabric's texture modification APIs.

## 📝 **Simple Script Example**

Here's a conceptual Python script that could do this:

```python
from PIL import Image

def generate_grass_variant(original_texture, grass_edges):
    """
    original_texture: PIL Image (16x16)
    grass_edges: list like ['top', 'left'] indicating which edges to grass-ify
    """
    result = original_texture.copy()
    
    for edge in grass_edges:
        if edge == 'top':
            grassify_edge(result, 'top')
        elif edge == 'bottom':
            grassify_edge(result, 'bottom')
        elif edge == 'left':
            grassify_edge(result, 'left')
        elif edge == 'right':
            grassify_edge(result, 'right')
    
    return result

def grassify_edge(image, edge):
    """Add grass-like colors to specified edge"""
    grass_color = (124, 179, 66)  # #7CB342
    
    if edge == 'top':
        # Modify row 0 (pure grass) and row 1 (transition)
        modify_pixels(image, row=0, grass_color, intensity=1.0)
        modify_pixels(image, row=1, grass_color, intensity=0.3)
    # ... similar for other edges
```

## 🎯 **Implementation for Your Mod**

### **Immediate Steps:**

1. **Create texture processor script** (Python + Pillow)
2. **Process existing textures**:
   - `path_level_1.png` → generate 4 variants
   - `path_level_2.png` (your overgrown) → generate 4 variants  
   - `path_level_3.png` → generate 4 variants
   - etc.

3. **Integrate with build process** or run manually

### **Benefits:**
- ✅ **Automatic**: Generate variants from any texture
- ✅ **Consistent**: Same grass-blending rules for all levels  
- ✅ **Flexible**: Easy to tweak colors and edge zones
- ✅ **Simple**: Uses existing textures as input

### **File Output:**
```
path_level_1.png (original)
├── path_level_1_standalone.png (unchanged)
├── path_level_1_surrounded.png (grass on all edges)
├── path_level_1_horizontal.png (grass on top/bottom)
└── path_level_1_vertical.png (grass on left/right)
```

This approach lets you design just one texture per level, and the system automatically creates the grass-blending variants!