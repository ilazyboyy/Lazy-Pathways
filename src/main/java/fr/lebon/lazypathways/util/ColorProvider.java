package fr.lebon.lazypathways.util;

import net.minecraft.client.color.world.BiomeColors;
import net.minecraft.util.math.BlockPos;
import net.minecraft.world.BlockRenderView;
import net.minecraft.block.BlockState;

public class ColorProvider {
    
    public static int getPathColor(BlockState state, BlockRenderView view, BlockPos pos, int tintIndex){
        if (view == null || pos == null) {
            return tintIndex == 0 ? 0x7CB342 : 0xFFFFFF; // Default grass green for grass parts, white for dirt
        }
        
        // Only tint grass parts (tintIndex 0), leave dirt parts natural (tintIndex 1+)
        if (tintIndex == 0) {
            return BiomeColors.getGrassColor(view, pos); // Grass color for grass elements
        } else {
            return 0xFFFFFF; // No tint for dirt elements
        }
    }
    
    public static int getLawnColor(BlockState state, BlockRenderView view, BlockPos pos, int tintIndex){
        if (view == null || pos == null) {
            return 0x7CB342; // Default grass green as fallback
        }
        
        // Use the biome's grass color for lawn blocks
        return BiomeColors.getGrassColor(view, pos);
    }
}
