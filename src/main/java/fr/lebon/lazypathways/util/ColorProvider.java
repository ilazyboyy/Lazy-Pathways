package fr.lebon.lazypathways.util;

import net.minecraft.client.color.world.BiomeColors;
import net.minecraft.util.math.BlockPos;
import net.minecraft.util.math.Direction;
import net.minecraft.world.BlockRenderView;
import net.minecraft.block.BlockState;
import net.minecraft.block.Blocks;
import net.minecraft.block.GrassBlock;
import net.minecraft.block.Block;
import fr.lebon.lazypathways.blocks.PathBlock;
import fr.lebon.lazypathways.config.LazyPathwaysConfig;
import fr.lebon.lazypathways.LazyPathways;
import me.shedaniel.autoconfig.AutoConfig;
import org.apache.logging.log4j.Level;
import java.util.HashMap;
import java.util.Map;

public class ColorProvider {
    // Cache for neighbor block color calculations to improve performance
    private static final Map<String, Integer> neighborColorCache = new HashMap<>();
    private static final int CACHE_MAX_SIZE = 1000;
    
    public static int getPathColor(BlockState state, BlockRenderView view, BlockPos pos, int tintIndex){
        if (view == null || pos == null) {
            return 0x5E9D34; // Default darker green as fallback
        }
        
        // Get the path wear level (1-5) to determine tinting behavior
        int pathLevel = 1; // default
        if (state != null && state.contains(PathBlock.STATE_RENDER)) {
            pathLevel = state.get(PathBlock.STATE_RENDER);
        }
        
        // For heavily worn paths (level 3+), reduce or eliminate grass tinting
        // This prevents mud/dirt areas from looking green
        if (pathLevel >= 4) {
            // Very worn paths - minimal grass tinting, more natural brown
            return 0x8B7355; // Natural dirt path brown
        } else if (pathLevel == 3) {
            // Moderate wear - slight tinting towards brown
            int baseGrassColor = BiomeColors.getGrassColor(view, pos);
            return blendColors(baseGrassColor, 0x8B7355, 0.6f); // 60% brown, 40% grass
        } else {
            // Fresh paths (1-2) - still grass-like but slightly worn
            int baseGrassColor = BiomeColors.getGrassColor(view, pos);
            
            // Calculate darkness factor based on path level
            float darknessFactor = Math.max(0.75f, 1.0f - (pathLevel * 0.12f));
            
            // Get blended color with neighboring blocks (only for fresh paths)
            int blendedColor = getBlendedNeighborColor(view, pos, baseGrassColor, pathLevel);
            
            return darkenColor(blendedColor, darknessFactor);
        }
    }
    
    /**
     * Blends the base grass color with colors from neighboring blocks
     * to create seamless integration with the surrounding terrain
     */
    private static int getBlendedNeighborColor(BlockRenderView view, BlockPos pos, int baseGrassColor, int pathLevel) {
        LazyPathwaysConfig config = AutoConfig.getConfigHolder(LazyPathwaysConfig.class).getConfig();
        
        // If blending is disabled, return base color
        if (!config.enableTextureBlending) {
            return baseGrassColor;
        }
        
        // Create cache key
        String cacheKey = pos.getX() + "," + pos.getY() + "," + pos.getZ() + "," + pathLevel + "," + config.blendingIntensity;
        
        // Check cache first
        Integer cachedColor = neighborColorCache.get(cacheKey);
        if (cachedColor != null) {
            return cachedColor;
        }
        
        // Sample colors from horizontal neighbors (N, S, E, W)
        int totalRed = 0, totalGreen = 0, totalBlue = 0;
        int validSamples = 0;
        
        Direction[] horizontalDirections = {Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST};
        
        for (Direction direction : horizontalDirections) {
            BlockPos neighborPos = pos.offset(direction);
            BlockState neighborState = view.getBlockState(neighborPos);
            
            int neighborColor = getBlockColor(view, neighborPos, neighborState, baseGrassColor);
            if (neighborColor != -1) {
                totalRed += (neighborColor >> 16) & 0xFF;
                totalGreen += (neighborColor >> 8) & 0xFF;
                totalBlue += neighborColor & 0xFF;
                validSamples++;
            }
        }
        
        // If we have neighbor colors, blend them with the base grass color
        int blendedColor;
        if (validSamples > 0) {
            int avgNeighborRed = totalRed / validSamples;
            int avgNeighborGreen = totalGreen / validSamples;
            int avgNeighborBlue = totalBlue / validSamples;
            
            // Extract base grass color components
            int baseRed = (baseGrassColor >> 16) & 0xFF;
            int baseGreen = (baseGrassColor >> 8) & 0xFF;
            int baseBlue = baseGrassColor & 0xFF;
            
            // Blend with moderate neighbor influence for visible but natural connected texture effect
            // Higher path levels (more worn) should blend less with neighbors but still show some connection
            float baseBlendingIntensity = Math.max(0.1f, Math.min(1.0f, config.blendingIntensity));
            // More noticeable blending that's still path-level dependent
            float neighborInfluence = Math.max(0.08f, (baseBlendingIntensity * 0.35f) - (pathLevel * 0.06f));
            // For heavily worn paths (level 4-5), reduce but don't eliminate neighbor influence
            if (pathLevel >= 4) {
                neighborInfluence = Math.max(0.05f, neighborInfluence * 0.6f);
            }
            float baseInfluence = 1.0f - neighborInfluence;
            
            int blendedRed = (int) (baseRed * baseInfluence + avgNeighborRed * neighborInfluence);
            int blendedGreen = (int) (baseGreen * baseInfluence + avgNeighborGreen * neighborInfluence);
            int blendedBlue = (int) (baseBlue * baseInfluence + avgNeighborBlue * neighborInfluence);
            
            blendedColor = (blendedRed << 16) | (blendedGreen << 8) | blendedBlue;
        } else {
            blendedColor = baseGrassColor;
        }
        
        // Cache the result (with size limit)
        if (neighborColorCache.size() < CACHE_MAX_SIZE) {
            neighborColorCache.put(cacheKey, blendedColor);
        }
        
        return blendedColor;
    }
    
    /**
     * Gets the appropriate color for a neighboring block
     */
    private static int getBlockColor(BlockRenderView view, BlockPos pos, BlockState state, int fallbackGrassColor) {
        Block block = state.getBlock();
        
        // Grass blocks - use biome grass color
        if (block instanceof GrassBlock || block == Blocks.GRASS_BLOCK) {
            return BiomeColors.getGrassColor(view, pos);
        }
        
        // Other path blocks - blend with their base grass color for seamless path networks
        if (block instanceof PathBlock) {
            return BiomeColors.getGrassColor(view, pos);
        }
        
        // Stone-like blocks - lighter grey for better blending
        if (block == Blocks.STONE || block == Blocks.COBBLESTONE || block == Blocks.STONE_BRICKS) {
            return 0x9A9A9A; // Lighter gray
        }
        
        // Dirt blocks - warmer brown closer to grass
        if (block == Blocks.DIRT || block == Blocks.COARSE_DIRT) {
            return 0x8B6914; // Warmer brown
        }
        
        // Sand blocks - more muted for better grass blending
        if (block == Blocks.SAND) {
            return 0xE8D5B7; // More muted sandy color
        }
        
        // Red sand - more muted
        if (block == Blocks.RED_SAND) {
            return 0xC49A6C; // Muted red sand
        }
        
        // Gravel - warmer grey
        if (block == Blocks.GRAVEL) {
            return 0x9A9A8A; // Warmer greyish
        }
        
        // Snow blocks
        if (block == Blocks.SNOW_BLOCK || block == Blocks.SNOW) {
            return 0xF0F8FF; // White-ish
        }
        
        // Wood blocks
        if (block == Blocks.OAK_PLANKS || block == Blocks.BIRCH_PLANKS || 
            block == Blocks.SPRUCE_PLANKS || block == Blocks.JUNGLE_PLANKS) {
            return 0x8B4513; // Wood brown
        }
        
        // Mycelium
        if (block == Blocks.MYCELIUM) {
            return 0x6F5F5F; // Gray-purple
        }
        
        // Podzol
        if (block == Blocks.PODZOL) {
            return 0x8B4513; // Brown
        }
        
        // Clay
        if (block == Blocks.CLAY) {
            return 0xA4A8B8; // Light gray-blue
        }
        
        // Terracotta
        if (block == Blocks.TERRACOTTA || block == Blocks.WHITE_TERRACOTTA) {
            return 0xCC8B65; // Terracotta orange
        }
        
        // Path blocks (vanilla)
        if (block == Blocks.DIRT_PATH) {
            return 0x8B7355; // Path brown
        }
        
        // Default: don't blend with this block type
        return -1;
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
     * Blends two colors together
     * @param color1 The first color
     * @param color2 The second color  
     * @param ratio The blend ratio (0.0 = all color1, 1.0 = all color2)
     * @return The blended color
     */
    private static int blendColors(int color1, int color2, float ratio) {
        int r1 = (color1 >> 16) & 0xFF;
        int g1 = (color1 >> 8) & 0xFF;
        int b1 = color1 & 0xFF;
        
        int r2 = (color2 >> 16) & 0xFF;
        int g2 = (color2 >> 8) & 0xFF;
        int b2 = color2 & 0xFF;
        
        int r = (int) (r1 * (1.0f - ratio) + r2 * ratio);
        int g = (int) (g1 * (1.0f - ratio) + g2 * ratio);
        int b = (int) (b1 * (1.0f - ratio) + b2 * ratio);
        
        return (r << 16) | (g << 8) | b;
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
    
    /**
     * Clears the neighbor color cache to free memory
     * This can be called periodically or when changing dimensions
     */
    public static void clearCache() {
        neighborColorCache.clear();
    }
}
