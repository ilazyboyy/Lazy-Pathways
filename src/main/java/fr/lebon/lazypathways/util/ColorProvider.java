package fr.lebon.lazypathways.util;

import net.minecraft.util.math.BlockPos;
import net.minecraft.world.BlockRenderView;
import net.minecraft.block.BlockState;

public class ColorProvider {
    
    public static int getPathColor(BlockState state, BlockRenderView view, BlockPos pos, int tintIndex){
        // Return a static color - no dynamic color changes based on biome or wear level
        return 0xFFFFFF; // White - lets the texture show its natural colors
    }
    
    public static int getLawnColor(BlockState state, BlockRenderView view, BlockPos pos, int tintIndex){
        // Return a static color - no dynamic color changes based on biome
        return 0xFFFFFF; // White - lets the texture show its natural colors
    }
}
