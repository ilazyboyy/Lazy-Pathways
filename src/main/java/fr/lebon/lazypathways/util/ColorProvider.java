package fr.lebon.lazypathways.util;

import net.minecraft.client.color.world.BiomeColors;
import net.minecraft.util.math.BlockPos;
import net.minecraft.world.BlockRenderView;
import net.minecraft.block.BlockState;

public class ColorProvider {
    
    public static int getPathColor(BlockState state, BlockRenderView view, BlockPos pos, int tintIndex){
        if (view == null || pos == null) {
            return 0x7CB342; // Default grass green as fallback
        }
        
        // Use the biome's grass color but don't do complex blending or level-based changes
        return BiomeColors.getGrassColor(view, pos);
    }
    
    public static int getLawnColor(BlockState state, BlockRenderView view, BlockPos pos, int tintIndex){
        if (view == null || pos == null) {
            return 0x7CB342; // Default grass green as fallback
        }
        
        // Use the biome's grass color for lawn blocks
        return BiomeColors.getGrassColor(view, pos);
    }
}
