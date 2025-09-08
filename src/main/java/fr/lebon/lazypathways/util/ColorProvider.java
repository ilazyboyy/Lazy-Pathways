package fr.lebon.lazypathways.util;

import net.minecraft.client.color.world.BiomeColors;
import net.minecraft.util.math.BlockPos;
import net.minecraft.world.BlockRenderView;
import net.minecraft.block.BlockState;
import fr.lebon.lazypathways.blocks.PathBlock;

public class ColorProvider {
    public static int getPathColor(BlockState state, BlockRenderView view, BlockPos pos, int tintIndex){
        if (view == null || pos == null) {
            return 0x5E9D34; // Default darker green as fallback
        }
        
        // Get the biome's grass color
        int grassColor = BiomeColors.getGrassColor(view, pos);
        
        // Get the path wear level (1-5) to determine darkness
        int pathLevel = 1; // default
        if (state != null && state.contains(PathBlock.STATE_RENDER)) {
            pathLevel = state.get(PathBlock.STATE_RENDER);
        }
        
        // Calculate darkness factor based on path level
        // Level 1: 90% of original (slightly darker)
        // Level 2: 80% of original 
        // Level 3: 70% of original
        // Level 4: 60% of original
        // Level 5: 50% of original (very dark/worn)
        float darknessFactor = 1.0f - (pathLevel * 0.1f);
        
        return darkenColor(grassColor, darknessFactor);
    }
    
    public static int getLawnColor(BlockState state, BlockRenderView view, BlockPos pos, int tintIndex){
        if (view == null || pos == null) {
            return 0x6FA139; // Default lighter green as fallback
        }
        
        // Get the biome's grass color
        int grassColor = BiomeColors.getGrassColor(view, pos);
        
        // Slightly darken the grass color by about 5% for lawn (lighter than paths)
        return darkenColor(grassColor, 0.95f);
    }
    
    /**
     * Darkens a color by multiplying each RGB component by the given factor
     * @param color The original color in RGB format
     * @param factor The darkening factor (0.0 = black, 1.0 = original color)
     * @return The darkened color
     */
    private static int darkenColor(int color, float factor) {
        int red = (int) (((color >> 16) & 0xFF) * factor);
        int green = (int) (((color >> 8) & 0xFF) * factor);
        int blue = (int) ((color & 0xFF) * factor);
        
        // Ensure values stay within 0-255 range
        red = Math.max(0, Math.min(255, red));
        green = Math.max(0, Math.min(255, green));
        blue = Math.max(0, Math.min(255, blue));
        
        return (red << 16) | (green << 8) | blue;
    }
}
