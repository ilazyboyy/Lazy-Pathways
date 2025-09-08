package fr.lebon.lazypathways;

import org.apache.logging.log4j.Level;

import fr.lebon.lazypathways.util.ColorProvider;
import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.blockrenderlayer.v1.BlockRenderLayerMap;
import net.fabricmc.fabric.api.client.rendering.v1.ColorProviderRegistry;
import net.minecraft.client.color.world.BiomeColors;
import net.minecraft.client.render.RenderLayer;

public class LazyPathwaysClient implements ClientModInitializer{

    @Override
    public void onInitializeClient() {
        LazyPathways.log(Level.INFO, "Client initialize");
        ColorProviderRegistry.BLOCK.register((state, view, pos, tintIndex) -> ColorProvider.getColor(view, pos), LazyPathways.PATH_BLOCK);
        ColorProviderRegistry.BLOCK.register((state, view, pos, tintIndex) -> 0x5E9D34, LazyPathways.LAWN_BLOCK);

        ColorProviderRegistry.ITEM.register((stack, tintIndex) -> 0x5E9D34, LazyPathways.LAWN_ITEM);
        ColorProviderRegistry.ITEM.register((stack, tintIndex) -> 0x5E9D34, LazyPathways.PATH_BLOCK);

        BlockRenderLayerMap.INSTANCE.putBlock(LazyPathways.PATH_BLOCK, RenderLayer.getCutout());//For transparancy
        BlockRenderLayerMap.INSTANCE.putBlock(LazyPathways.LAWN_BLOCK, RenderLayer.getCutout());
    }
    
}
