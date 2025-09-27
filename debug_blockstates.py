#!/usr/bin/env python3

import json
import os

def check_blockstate_integrity():
    print("🔍 Checking blockstate integrity...")
    
    # Load blockstate file
    blockstate_path = "src/main/resources/assets/lazypathways/blockstates/path.json"
    with open(blockstate_path, 'r') as f:
        blockstate_data = json.load(f)
    
    # Get all model references
    model_refs = set()
    missing_models = []
    
    for variant_key, variant_list in blockstate_data["variants"].items():
        for variant in variant_list:
            model_name = variant["model"]
            model_refs.add(model_name)
            
            # Check if model file exists
            model_file = model_name.replace("lazypathways:block/", "src/main/resources/assets/lazypathways/models/block/") + ".json"
            if not os.path.exists(model_file):
                missing_models.append((variant_key, model_name))
    
    print(f"📊 Total unique model references: {len(model_refs)}")
    print(f"🚨 Missing models: {len(missing_models)}")
    
    if missing_models:
        print("\n❌ MISSING MODELS:")
        for variant_key, model_name in missing_models:
            print(f"  - {variant_key} -> {model_name}")
    
    # Check texture references in models
    missing_textures = []
    for model_ref in model_refs:
        model_file = model_ref.replace("lazypathways:block/", "src/main/resources/assets/lazypathways/models/block/") + ".json"
        if os.path.exists(model_file):
            with open(model_file, 'r') as f:
                model_data = json.load(f)
            
            # Check top_overlay texture
            if "textures" in model_data and "top_overlay" in model_data["textures"]:
                texture_ref = model_data["textures"]["top_overlay"]
                texture_file = texture_ref.replace("lazypathways:block/", "src/main/resources/assets/lazypathways/textures/block/") + ".png"
                
                if not os.path.exists(texture_file):
                    missing_textures.append((model_ref, texture_ref))
    
    print(f"🎨 Missing textures: {len(missing_textures)}")
    if missing_textures:
        print("\n❌ MISSING TEXTURES:")
        for model_ref, texture_ref in missing_textures:
            print(f"  - {model_ref} -> {texture_ref}")
    
    # Test specific problematic combinations
    print("\n🧪 Testing specific combinations:")
    test_combinations = [
        "state_render=1,stepped=false,grass_north=false,grass_south=false,grass_east=false,grass_west=false",
        "state_render=2,stepped=false,grass_north=false,grass_south=false,grass_east=false,grass_west=false", 
        "state_render=3,stepped=false,grass_north=false,grass_south=false,grass_east=false,grass_west=false",
        "state_render=4,stepped=false,grass_north=false,grass_south=false,grass_east=false,grass_west=false",
        "state_render=5,stepped=false,grass_north=false,grass_south=false,grass_east=false,grass_west=false",
        "state_render=1,stepped=false,grass_north=true,grass_south=true,grass_east=true,grass_west=true",
        "state_render=1,stepped=false",
        "state_render=2,stepped=false",
        "state_render=3,stepped=false",
        "state_render=4,stepped=false",
        "state_render=5,stepped=false",
    ]
    
    for combo in test_combinations:
        if combo in blockstate_data["variants"]:
            model_name = blockstate_data["variants"][combo][0]["model"]
            model_file = model_name.replace("lazypathways:block/", "src/main/resources/assets/lazypathways/models/block/") + ".json"
            exists = "✅" if os.path.exists(model_file) else "❌"
            print(f"  {exists} {combo} -> {model_name}")
        else:
            print(f"  ❌ {combo} -> NOT FOUND IN BLOCKSTATE")
    
    print(f"\n{'✅ All checks passed!' if not missing_models and not missing_textures else '❌ Issues found - see above'}")

if __name__ == "__main__":
    check_blockstate_integrity()