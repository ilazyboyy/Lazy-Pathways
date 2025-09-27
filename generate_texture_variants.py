#!/usr/bin/env python3
"""
Generative Connected Texture Generator for Lazy Pathways Mod

This script takes existing path textures and automatically generates
grass-blending variants for connected texture functionality.

Requirements: pip install Pillow

Usage: python generate_texture_variants.py
"""

import os
from PIL import Image, ImageColor
import argparse

# Configuration
TEXTURE_SIZE = 16
GRASS_COLOR = (124, 179, 66)  # #7CB342 - will be tinted by biome
GRASS_TRANSITION = (106, 160, 56)  # Slightly darker grass for transitions

class TextureVariantGenerator:
    def __init__(self, input_dir, output_dir=None):
        self.input_dir = input_dir
        self.output_dir = output_dir or input_dir
        
    def generate_all_variants(self):
        """Generate variants for all path level textures"""
        print("🎨 Generating texture variants for grass blending...")
        
        # Find all path level textures
        path_textures = []
        for filename in os.listdir(self.input_dir):
            if filename.startswith('path_level_') and filename.endswith('.png'):
                # Skip existing variants
                if not any(variant in filename for variant in ['_standalone', '_surrounded', '_horizontal', '_vertical']):
                    path_textures.append(filename)
        
        for texture_file in path_textures:
            print(f"📁 Processing {texture_file}...")
            self.generate_variants_for_texture(texture_file)
            
        print("✅ Texture variant generation complete!")
    
    def generate_variants_for_texture(self, texture_filename):
        """Generate 4 variants for a single texture"""
        base_path = os.path.join(self.input_dir, texture_filename)
        
        if not os.path.exists(base_path):
            print(f"❌ File not found: {base_path}")
            return
            
        # Load original texture
        try:
            original = Image.open(base_path).convert('RGBA')
        except Exception as e:
            print(f"❌ Error loading {texture_filename}: {e}")
            return
            
        if original.size != (TEXTURE_SIZE, TEXTURE_SIZE):
            print(f"⚠️  Warning: {texture_filename} is not {TEXTURE_SIZE}x{TEXTURE_SIZE}, resizing...")
            original = original.resize((TEXTURE_SIZE, TEXTURE_SIZE), Image.NEAREST)
        
        # Generate base name (without extension)
        base_name = texture_filename.replace('.png', '')
        
        # Generate variants
        variants = {
            'standalone': [],  # No grass edges (unchanged)
            'surrounded': ['top', 'bottom', 'left', 'right'],  # All grass edges
            'horizontal': ['top', 'bottom'],  # North/South grass (horizontal path)
            'vertical': ['left', 'right']     # East/West grass (vertical path)
        }
        
        for variant_name, grass_edges in variants.items():
            variant_texture = self.create_variant(original, grass_edges)
            output_filename = f"{base_name}_{variant_name}.png"
            output_path = os.path.join(self.output_dir, output_filename)
            
            variant_texture.save(output_path)
            print(f"  ✅ Created {output_filename}")
    
    def create_variant(self, original, grass_edges):
        """Create a variant with grass edges on specified sides"""
        result = original.copy()
        
        for edge in grass_edges:
            self.grassify_edge(result, edge)
            
        return result
    
    def grassify_edge(self, image, edge):
        """Add grass-like appearance to specified edge"""
        pixels = image.load()
        
        if edge == 'top':
            self.grassify_horizontal_edge(pixels, 0, True)  # Top row
            self.grassify_horizontal_edge(pixels, 1, False)  # Transition row
        elif edge == 'bottom':
            self.grassify_horizontal_edge(pixels, TEXTURE_SIZE - 1, True)  # Bottom row
            self.grassify_horizontal_edge(pixels, TEXTURE_SIZE - 2, False)  # Transition row
        elif edge == 'left':
            self.grassify_vertical_edge(pixels, 0, True)  # Left column
            self.grassify_vertical_edge(pixels, 1, False)  # Transition column
        elif edge == 'right':
            self.grassify_vertical_edge(pixels, TEXTURE_SIZE - 1, True)  # Right column
            self.grassify_vertical_edge(pixels, TEXTURE_SIZE - 2, False)  # Transition column
    
    def grassify_horizontal_edge(self, pixels, row, is_pure_edge):
        """Modify a horizontal row (top or bottom edge)"""
        for x in range(TEXTURE_SIZE):
            original_color = pixels[x, row]
            if self.should_grassify_pixel(original_color):
                if is_pure_edge:
                    pixels[x, row] = self.blend_with_grass(original_color, 0.8)
                else:
                    pixels[x, row] = self.blend_with_grass(original_color, 0.3)
    
    def grassify_vertical_edge(self, pixels, col, is_pure_edge):
        """Modify a vertical column (left or right edge)"""
        for y in range(TEXTURE_SIZE):
            original_color = pixels[col, y]
            if self.should_grassify_pixel(original_color):
                if is_pure_edge:
                    pixels[col, y] = self.blend_with_grass(original_color, 0.8)
                else:
                    pixels[col, y] = self.blend_with_grass(original_color, 0.3)
    
    def should_grassify_pixel(self, color):
        """Determine if a pixel should be modified to look grass-like"""
        r, g, b, a = color
        
        # Don't modify fully transparent pixels
        if a < 128:
            return False
            
        # Calculate brightness
        brightness = (r + g + b) / (3 * 255)
        
        # Don't grassify very dark pixels (they're probably dirt/mud)
        if brightness < 0.2:
            return False
            
        # Don't grassify pixels that are already very brown/dirt-like
        # Check if it's a dirt-like color (brownish)
        if r > g and r > b and g > b:  # More red than green, more green than blue = brownish
            dirt_factor = (r - b) / max(r, 1)  # How brown vs other colors
            if dirt_factor > 0.3 and brightness < 0.6:
                return False
        
        return True
    
    def blend_with_grass(self, original_color, grass_intensity):
        """Blend original color with grass color"""
        r, g, b, a = original_color
        
        # Blend with grass color
        new_r = int(r * (1 - grass_intensity) + GRASS_COLOR[0] * grass_intensity)
        new_g = int(g * (1 - grass_intensity) + GRASS_COLOR[1] * grass_intensity)
        new_b = int(b * (1 - grass_intensity) + GRASS_COLOR[2] * grass_intensity)
        
        # Clamp values
        new_r = max(0, min(255, new_r))
        new_g = max(0, min(255, new_g))
        new_b = max(0, min(255, new_b))
        
        return (new_r, new_g, new_b, a)

def main():
    parser = argparse.ArgumentParser(description='Generate grass-blending texture variants for Lazy Pathways mod')
    parser.add_argument('--input', '-i', 
                       default='src/main/resources/assets/lazypathways/textures/block',
                       help='Input directory containing original textures')
    parser.add_argument('--output', '-o',
                       help='Output directory (defaults to input directory)')
    
    args = parser.parse_args()
    
    input_dir = args.input
    output_dir = args.output
    
    if not os.path.exists(input_dir):
        print(f"❌ Input directory not found: {input_dir}")
        print("Make sure you're running this from the mod root directory")
        return
    
    print(f"📂 Input directory: {input_dir}")
    print(f"📂 Output directory: {output_dir or input_dir}")
    
    generator = TextureVariantGenerator(input_dir, output_dir)
    generator.generate_all_variants()
    
    print("\n🎮 Ready to build and test!")
    print("Run: ./gradlew clean build")

if __name__ == '__main__':
    main()