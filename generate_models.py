#!/usr/bin/env python3
"""
Generate model files for all texture variants
"""

import os
import json

MODEL_TEMPLATE = {
    "parent": "block/block",
    "textures": {
        "particle": "minecraft:block/dirt",
        "bottom": "minecraft:block/dirt",
        "top": "minecraft:block/grass_block_top",
        "side": "minecraft:block/grass_block_side",
        "overlay": "minecraft:block/grass_block_side_overlay",
        "top_overlay": "REPLACE_ME"
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

def generate_models():
    models_dir = "src/main/resources/assets/lazypathways/models/block"
    
    if not os.path.exists(models_dir):
        print(f"❌ Models directory not found: {models_dir}")
        return
    
    levels = [1, 2, 3, 4, 5]
    variants = ['standalone', 'surrounded', 'horizontal', 'vertical']
    
    print("🔧 Generating model files for texture variants...")
    
    for level in levels:
        for variant in variants:
            model_name = f"path_level_{level}_{variant}"
            model_file = f"{model_name}.json"
            model_path = os.path.join(models_dir, model_file)
            
            # Create model data
            model_data = MODEL_TEMPLATE.copy()
            model_data["textures"]["top_overlay"] = f"lazypathways:block/{model_name}"
            
            # Write model file
            with open(model_path, 'w') as f:
                json.dump(model_data, f, indent=2)
            
            print(f"  ✅ Created {model_file}")
    
    print("✅ Model generation complete!")

if __name__ == '__main__':
    generate_models()