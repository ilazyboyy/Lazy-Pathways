#!/usr/bin/env python3

import json
import os

def main():
    base_dir = "src/main/resources/assets/lazypathways"
    blockstates_dir = os.path.join(base_dir, "blockstates")
    models_dir = os.path.join(base_dir, "models", "block")
    
    # Create directories if they don't exist
    os.makedirs(blockstates_dir, exist_ok=True)
    os.makedirs(models_dir, exist_ok=True)
    
    # Generate mappings for all 16 neighbor combinations to texture suffixes
    neighbor_mappings = []
    for n in [False, True]:  # north
        for s in [False, True]:  # south
            for e in [False, True]:  # east
                for w in [False, True]:  # west
                    # Create suffix based on neighbors
                    suffix_parts = []
                    if n: suffix_parts.append('n')
                    if s: suffix_parts.append('s') 
                    if e: suffix_parts.append('e')
                    if w: suffix_parts.append('w')
                    
                    suffix = ''.join(suffix_parts) if suffix_parts else 'none'
                    
                    neighbor_mappings.append({
                        'north': n, 'south': s, 'east': e, 'west': w,
                        'suffix': suffix
                    })
    
    print(f"🎯 Generating blockstate system for {len(neighbor_mappings)} neighbor combinations...")
    
    # Generate models for all levels and variants
    for level in range(1, 6):  # levels 1-5
        print(f"📝 Generating models for path_level_{level}...")
        
        for mapping in neighbor_mappings:
            suffix = mapping['suffix']
            model_name = f"path_level_{level}_{suffix}"
            texture_name = f"path_level_{level}_{suffix}"
            
            model_data = {
                "parent": "block/block",
                "textures": {
                    "particle": f"lazypathways:block/{texture_name}",
                    "top": f"lazypathways:block/{texture_name}",
                    "bottom": "minecraft:block/dirt",
                    "side": "minecraft:block/dirt"
                },
                "elements": [{
                    "from": [0, 0, 0],
                    "to": [16, 15, 16],
                    "faces": {
                        "down": {"uv": [0, 0, 16, 16], "texture": "#bottom", "cullface": "down"},
                        "up": {"uv": [0, 0, 16, 16], "texture": "#top", "cullface": "up"},
                        "north": {"uv": [0, 1, 16, 16], "texture": "#side", "cullface": "north"},
                        "south": {"uv": [0, 1, 16, 16], "texture": "#side", "cullface": "south"},
                        "west": {"uv": [0, 1, 16, 16], "texture": "#side", "cullface": "west"},
                        "east": {"uv": [0, 1, 16, 16], "texture": "#side", "cullface": "east"}
                    }
                }]
            }
            
            model_path = os.path.join(models_dir, f"{model_name}.json")
            with open(model_path, 'w') as f:
                json.dump(model_data, f, indent=2)
    
    # Generate the complete blockstate file
    print("🔧 Generating complete blockstate file...")
    
    variants = {}
    
    for level in range(1, 6):  # levels 1-5
        for stepped in [False, True]:
            
            # Add variants for all possible grass neighbor combinations
            for mapping in neighbor_mappings:
                n, s, e, w = mapping['north'], mapping['south'], mapping['east'], mapping['west']
                suffix = mapping['suffix']
                model_name = f"path_level_{level}_{suffix}"
                
                state_key = f"state_render={level},stepped={'true' if stepped else 'false'},grass_north={'true' if n else 'false'},grass_south={'true' if s else 'false'},grass_east={'true' if e else 'false'},grass_west={'true' if w else 'false'}"
                
                variants[state_key] = [
                    {"model": f"lazypathways:block/{model_name}", "y": 0},
                    {"model": f"lazypathways:block/{model_name}", "y": 90},
                    {"model": f"lazypathways:block/{model_name}", "y": 180},
                    {"model": f"lazypathways:block/{model_name}", "y": 270}
                ]
            
            # Add fallback variants (for backward compatibility or edge cases)
            fallback_key = f"state_render={level},stepped={'true' if stepped else 'false'}"
            if fallback_key not in variants:
                variants[fallback_key] = [
                    {"model": f"lazypathways:block/path_level_{level}_none", "y": 0},
                    {"model": f"lazypathways:block/path_level_{level}_none", "y": 90},
                    {"model": f"lazypathways:block/path_level_{level}_none", "y": 180},
                    {"model": f"lazypathways:block/path_level_{level}_none", "y": 270}
                ]
    
    blockstate_data = {"variants": variants}
    
    blockstate_path = os.path.join(blockstates_dir, "path.json")
    with open(blockstate_path, 'w') as f:
        json.dump(blockstate_data, f, indent=2)
    
    print(f"✅ Generated complete blockstate system!")
    print(f"📊 Total variants: {len(variants)}")
    print(f"📊 Total models: {5 * len(neighbor_mappings)}")
    print("🎮 Ready for testing in-game!")

if __name__ == "__main__":
    main()