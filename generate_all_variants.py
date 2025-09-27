#!/usr/bin/env python3
"""
COMPLETE Connected Texture Generator for Lazy Pathways Mod

This script generates ALL 16 possible grass neighbor combinations for each path level,
creating beautiful, soft, random grass edges that blend naturally.

Requirements: pip install Pillow numpy

Usage: python generate_all_variants.py
"""

import os
from PIL import Image, ImageFilter, ImageEnhance
import random
import argparse

# Configuration
TEXTURE_SIZE = 16
GRASS_COLORS = [
    (124, 179, 66),   # Primary grass #7CB342
    (106, 160, 56),   # Darker grass  
    (140, 195, 80),   # Lighter grass
    (115, 170, 60),   # Medium grass
]

class AdvancedTextureGenerator:
    def __init__(self, input_dir, output_dir=None):
        self.input_dir = input_dir
        self.output_dir = output_dir or input_dir
        
    def generate_all_combinations(self):
        """Generate ALL 16 possible grass neighbor combinations for each path level"""
        print("🎨 Generating COMPLETE texture variant system with soft random grass edges...")
        
        # Find all original path level textures
        path_textures = []
        for filename in os.listdir(self.input_dir):
            if filename.startswith('path_level_') and filename.endswith('.png'):
                # Only process original files: path_level_1.png, path_level_2.png, etc.
                # Skip files that already have variant suffixes
                if not any(suffix in filename for suffix in ['_n', '_s', '_e', '_w', '_none', '_standalone', '_surrounded', '_horizontal', '_vertical']):
                    # Count underscores to ensure it's a base file
                    if filename.count('_') == 2:  # path_level_X.png has exactly 2 underscores
                        path_textures.append(filename)
        
        # Generate all 16 combinations for each texture
        for texture_file in path_textures:
            print(f"📁 Processing {texture_file} - Generating 16 variants...")
            self.generate_all_variants_for_texture(texture_file)
            
        print("✅ Complete texture generation finished!")
        print(f"📊 Generated variants for {len(path_textures)} base textures")
        
    def generate_all_variants_for_texture(self, texture_filename):
        """Generate all 16 possible combinations for a single texture"""
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
        
        # Generate ALL 16 possible combinations (2^4 = 16)
        for i in range(16):
            # Convert number to binary to get grass neighbor pattern
            grass_north = bool(i & 8)  # 8 = 1000 in binary
            grass_south = bool(i & 4)  # 4 = 0100 in binary  
            grass_east = bool(i & 2)   # 2 = 0010 in binary
            grass_west = bool(i & 1)   # 1 = 0001 in binary
            
            # Create descriptive filename
            suffix = self.get_combination_suffix(grass_north, grass_south, grass_east, grass_west)
            
            # Generate the texture variant
            variant_texture = self.create_advanced_variant(original, grass_north, grass_south, grass_east, grass_west)
            
            # Save the variant
            output_filename = f"{base_name}_{suffix}.png"
            output_path = os.path.join(self.output_dir, output_filename)
            variant_texture.save(output_path)
            
            print(f"  ✅ Created {output_filename}")
    
    def get_combination_suffix(self, north, south, east, west):
        """Generate a descriptive suffix for the grass combination"""
        pattern = ""
        if north: pattern += "n"
        if south: pattern += "s" 
        if east: pattern += "e"
        if west: pattern += "w"
        
        if not pattern:
            return "none"  # No grass neighbors
        
        return pattern  # e.g., "nsew", "ns", "ew", "n", etc.
    
    def create_advanced_variant(self, original, grass_north, grass_south, grass_east, grass_west):
        """Create a variant with advanced soft grass edges and randomness"""
        result = original.copy()
        pixels = result.load()
        
        # Add grass edges based on neighbors
        if grass_north:
            self.add_soft_grass_edge(pixels, 'north')
        if grass_south:
            self.add_soft_grass_edge(pixels, 'south')
        if grass_east:
            self.add_soft_grass_edge(pixels, 'east')
        if grass_west:
            self.add_soft_grass_edge(pixels, 'west')
            
        # Apply softening filter for more natural appearance
        result = self.apply_softening(result)
        
        return result
    
    def add_soft_grass_edge(self, pixels, edge):
        """Add soft, random grass edge with natural variation"""
        grass_color = random.choice(GRASS_COLORS)
        
        if edge == 'north':
            self.create_soft_horizontal_edge(pixels, 0, grass_color, 'top')
        elif edge == 'south':
            self.create_soft_horizontal_edge(pixels, TEXTURE_SIZE - 1, grass_color, 'bottom')
        elif edge == 'east':
            self.create_soft_vertical_edge(pixels, TEXTURE_SIZE - 1, grass_color, 'right')
        elif edge == 'west':
            self.create_soft_vertical_edge(pixels, 0, grass_color, 'left')
    
    def create_soft_horizontal_edge(self, pixels, row, grass_color, side):
        """Create a soft horizontal grass edge with natural variation"""
        for x in range(TEXTURE_SIZE):
            original_color = pixels[x, row]
            
            if self.should_grassify_pixel(original_color):
                # Primary edge with random intensity
                intensity = random.uniform(0.7, 0.9)
                new_color = self.blend_colors_advanced(original_color, grass_color, intensity)
                pixels[x, row] = new_color
                
                # Add transition row with softer blending
                if side == 'top' and row + 1 < TEXTURE_SIZE:
                    transition_row = row + 1
                elif side == 'bottom' and row - 1 >= 0:
                    transition_row = row - 1
                else:
                    continue
                    
                transition_original = pixels[x, transition_row]
                if self.should_grassify_pixel(transition_original):
                    # Random transition intensity
                    transition_intensity = random.uniform(0.2, 0.4)
                    transition_color = self.blend_colors_advanced(transition_original, grass_color, transition_intensity)
                    pixels[x, transition_row] = transition_color
                    
                # Add subtle random grass spots nearby
                self.add_random_grass_spots(pixels, x, row, grass_color)
    
    def create_soft_vertical_edge(self, pixels, col, grass_color, side):
        """Create a soft vertical grass edge with natural variation"""
        for y in range(TEXTURE_SIZE):
            original_color = pixels[col, y]
            
            if self.should_grassify_pixel(original_color):
                # Primary edge with random intensity  
                intensity = random.uniform(0.7, 0.9)
                new_color = self.blend_colors_advanced(original_color, grass_color, intensity)
                pixels[col, y] = new_color
                
                # Add transition column with softer blending
                if side == 'left' and col + 1 < TEXTURE_SIZE:
                    transition_col = col + 1
                elif side == 'right' and col - 1 >= 0:
                    transition_col = col - 1
                else:
                    continue
                    
                transition_original = pixels[transition_col, y]
                if self.should_grassify_pixel(transition_original):
                    # Random transition intensity
                    transition_intensity = random.uniform(0.2, 0.4)
                    transition_color = self.blend_colors_advanced(transition_original, grass_color, transition_intensity)
                    pixels[transition_col, y] = transition_color
                    
                # Add subtle random grass spots nearby
                self.add_random_grass_spots(pixels, col, y, grass_color)
    
    def add_random_grass_spots(self, pixels, x, y, grass_color):
        """Add random small grass spots for natural texture variation"""
        if random.random() < 0.3:  # 30% chance of adding spots
            # Add spots in nearby pixels
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    spot_x, spot_y = x + dx, y + dy
                    if (0 <= spot_x < TEXTURE_SIZE and 0 <= spot_y < TEXTURE_SIZE and 
                        random.random() < 0.1):  # 10% chance per nearby pixel
                        
                        original = pixels[spot_x, spot_y]
                        if self.should_grassify_pixel(original):
                            spot_intensity = random.uniform(0.1, 0.3)
                            spot_color = self.blend_colors_advanced(original, grass_color, spot_intensity)
                            pixels[spot_x, spot_y] = spot_color
    
    def should_grassify_pixel(self, color):
        """Enhanced pixel analysis for grass-ification"""
        r, g, b, a = color
        
        # Don't modify transparent pixels
        if a < 128:
            return False
            
        # Calculate brightness and color characteristics
        brightness = (r + g + b) / (3 * 255)
        
        # Don't grassify very dark pixels (dirt/mud)
        if brightness < 0.15:
            return False
            
        # Enhanced dirt detection
        if r > g and r > b:  # Reddish/brownish
            dirt_factor = (r - min(g, b)) / max(r, 1)
            if dirt_factor > 0.4 and brightness < 0.5:
                return False
        
        # Don't grassify pixels that are already very green
        if g > r * 1.3 and g > b * 1.3:
            return False
            
        return True
    
    def blend_colors_advanced(self, original_color, grass_color, intensity):
        """Advanced color blending with natural variation"""
        r, g, b, a = original_color
        
        # Add slight random variation to grass color
        grass_r = grass_color[0] + random.randint(-10, 10)
        grass_g = grass_color[1] + random.randint(-10, 10)  
        grass_b = grass_color[2] + random.randint(-10, 10)
        
        # Clamp grass color values
        grass_r = max(0, min(255, grass_r))
        grass_g = max(0, min(255, grass_g))
        grass_b = max(0, min(255, grass_b))
        
        # Blend with slight random variation in intensity
        actual_intensity = intensity + random.uniform(-0.1, 0.1)
        actual_intensity = max(0.0, min(1.0, actual_intensity))
        
        new_r = int(r * (1 - actual_intensity) + grass_r * actual_intensity)
        new_g = int(g * (1 - actual_intensity) + grass_g * actual_intensity)
        new_b = int(b * (1 - actual_intensity) + grass_b * actual_intensity)
        
        # Clamp final values
        new_r = max(0, min(255, new_r))
        new_g = max(0, min(255, new_g))
        new_b = max(0, min(255, new_b))
        
        return (new_r, new_g, new_b, a)
    
    def apply_softening(self, image):
        """Apply subtle softening for more natural appearance"""
        # Very light blur to soften harsh edges
        softened = image.filter(ImageFilter.GaussianBlur(radius=0.3))
        
        # Blend original with softened (keep mostly original)
        result = Image.blend(image, softened, 0.3)
        
        return result

def main():
    parser = argparse.ArgumentParser(description='Generate ALL grass-blending variants for Lazy Pathways mod')
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
    print("🚀 Generating ALL COMBINATIONS (16 per texture) with soft random grass edges!")
    
    generator = AdvancedTextureGenerator(input_dir, output_dir)
    generator.generate_all_combinations()
    
    print("\n🎮 Phase 1 Complete - Enhanced textures generated!")
    print("Next: Generate models and blockstate system...")

if __name__ == '__main__':
    main()