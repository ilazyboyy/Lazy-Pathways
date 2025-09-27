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
    
    print("🔧 Generating WORKING blockstate system (4-variant approach)...")
    
    # Define the 4 variants that actually work
    variants = [
        {"name": "standalone", "texture_suffix": "none"},
        {"name": "surrounded", "texture_suffix": "nsew"}, 
        {"name": "horizontal", "texture_suffix": "ns"},
        {"name": "vertical", "texture_suffix": "ew"}
    ]
    
    # Generate models for all levels and variants
    for level in range(1, 6):  # levels 1-5
        print(f"📝 Generating models for path_level_{level}...")
        
        for variant in variants:
            model_name = f"path_level_{level}_{variant['name']}"
            texture_name = f"path_level_{level}_{variant['texture_suffix']}"
            
            model_data = {
                "parent": "block/block",
                "textures": {
                    "particle": "minecraft:block/dirt",
                    "bottom": "minecraft:block/dirt",
                    "top": "minecraft:block/grass_block_top",
                    "side": "minecraft:block/grass_block_side",
                    "overlay": "minecraft:block/grass_block_side_overlay",
                    "top_overlay": f"lazypathways:block/{texture_name}"
                },
                "elements": [
                    {
                        "from": [0, 0, 0],
                        "to": [16, 16, 16],
                        "faces": {
                            "down": {"uv": [0, 0, 16, 16], "texture": "#bottom", "cullface": "down"},
                            "up": {"uv": [0, 0, 16, 16], "texture": "#top", "tintindex": 0, "cullface": "up"},
                            "north": {"uv": [0, 0, 16, 16], "texture": "#side", "tintindex": 0, "cullface": "north"},
                            "south": {"uv": [0, 0, 16, 16], "texture": "#side", "tintindex": 0, "cullface": "south"},
                            "west": {"uv": [0, 0, 16, 16], "texture": "#side", "tintindex": 0, "cullface": "west"},
                            "east": {"uv": [0, 0, 16, 16], "texture": "#side", "tintindex": 0, "cullface": "east"}
                        }
                    },
                    {
                        "from": [0, 0, 0],
                        "to": [16, 16, 16],
                        "faces": {
                            "up": {"uv": [0, 0, 16, 16], "texture": "#top_overlay", "cullface": "up"},
                            "north": {"uv": [0, 0, 16, 16], "texture": "#overlay", "tintindex": 0, "cullface": "north"},
                            "south": {"uv": [0, 0, 16, 16], "texture": "#overlay", "tintindex": 0, "cullface": "south"},
                            "west": {"uv": [0, 0, 16, 16], "texture": "#overlay", "tintindex": 0, "cullface": "west"},
                            "east": {"uv": [0, 0, 16, 16], "texture": "#overlay", "tintindex": 0, "cullface": "east"}
                        }
                    }
                ]
            }
            
            model_path = os.path.join(models_dir, f"{model_name}.json")
            with open(model_path, 'w') as f:
                json.dump(model_data, f, indent=2)
    
    # Generate the blockstate file using the EXACT original structure
    print("🔧 Generating working blockstate file...")
    
    variants_data = {}
    
    for level in range(1, 6):  # levels 1-5
        for stepped in [False, True]:
            
            # Standalone (no grass neighbors)
            key = f"state_render={level},stepped={'true' if stepped else 'false'},grass_north=false,grass_south=false,grass_east=false,grass_west=false"
            variants_data[key] = [
                {"model": f"lazypathways:block/path_level_{level}_standalone", "y": 0},
                {"model": f"lazypathways:block/path_level_{level}_standalone", "y": 90},
                {"model": f"lazypathways:block/path_level_{level}_standalone", "y": 180},
                {"model": f"lazypathways:block/path_level_{level}_standalone", "y": 270}
            ]
            
            # Surrounded (grass on all sides)
            key = f"state_render={level},stepped={'true' if stepped else 'false'},grass_north=true,grass_south=true,grass_east=true,grass_west=true"
            variants_data[key] = [
                {"model": f"lazypathways:block/path_level_{level}_surrounded", "y": 0},
                {"model": f"lazypathways:block/path_level_{level}_surrounded", "y": 90},
                {"model": f"lazypathways:block/path_level_{level}_surrounded", "y": 180},
                {"model": f"lazypathways:block/path_level_{level}_surrounded", "y": 270}
            ]
            
            # Horizontal (grass north + south)
            key = f"state_render={level},stepped={'true' if stepped else 'false'},grass_north=true,grass_south=true,grass_east=false,grass_west=false"
            variants_data[key] = [
                {"model": f"lazypathways:block/path_level_{level}_horizontal", "y": 0},
                {"model": f"lazypathways:block/path_level_{level}_horizontal", "y": 90},
                {"model": f"lazypathways:block/path_level_{level}_horizontal", "y": 180},
                {"model": f"lazypathways:block/path_level_{level}_horizontal", "y": 270}
            ]
            
            # Vertical (grass east + west)
            key = f"state_render={level},stepped={'true' if stepped else 'false'},grass_north=false,grass_south=false,grass_east=true,grass_west=true"
            variants_data[key] = [
                {"model": f"lazypathways:block/path_level_{level}_vertical", "y": 0},
                {"model": f"lazypathways:block/path_level_{level}_vertical", "y": 90},
                {"model": f"lazypathways:block/path_level_{level}_vertical", "y": 180},
                {"model": f"lazypathways:block/path_level_{level}_vertical", "y": 270}
            ]
            
            # Fallback variants
            fallback_key = f"state_render={level},stepped={'true' if stepped else 'false'}"
            if fallback_key not in variants_data:
                variants_data[fallback_key] = [
                    {"model": f"lazypathways:block/path_level_{level}_standalone", "y": 0},
                    {"model": f"lazypathways:block/path_level_{level}_standalone", "y": 90},
                    {"model": f"lazypathways:block/path_level_{level}_standalone", "y": 180},
                    {"model": f"lazypathways:block/path_level_{level}_standalone", "y": 270}
                ]
    
    blockstate_data = {"variants": variants_data}
    
    blockstate_path = os.path.join(blockstates_dir, "path.json")
    with open(blockstate_path, 'w') as f:
        json.dump(blockstate_data, f, indent=2)
    
    print(f"✅ Generated WORKING blockstate system!")
    print(f"📊 Total variants: {len(variants_data)}")
    print(f"📊 Total models: {5 * len(variants)}")
    print("🎮 This should work - based on original proven structure!")

if __name__ == "__main__":
    main()