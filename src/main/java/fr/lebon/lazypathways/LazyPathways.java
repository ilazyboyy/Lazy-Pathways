package fr.lebon.lazypathways;


import net.fabricmc.fabric.api.itemgroup.v1.ItemGroupEvents;
import net.minecraft.item.*;
import net.minecraft.registry.Registries;
import net.minecraft.registry.Registry;
import org.apache.logging.log4j.Level;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import fr.lebon.lazypathways.blocks.LawnBlock;
import fr.lebon.lazypathways.blocks.PathBlock;
import fr.lebon.lazypathways.config.LazyPathwaysConfig;
import fr.lebon.lazypathways.entity.PathEntity;
import me.shedaniel.autoconfig.AutoConfig;
import me.shedaniel.autoconfig.serializer.GsonConfigSerializer;
import net.fabricmc.api.ModInitializer;
import net.fabricmc.fabric.api.object.builder.v1.block.FabricBlockSettings;
import net.fabricmc.fabric.api.object.builder.v1.block.entity.FabricBlockEntityTypeBuilder;
import net.minecraft.block.Block;
import net.minecraft.block.MapColor;
import net.minecraft.block.piston.PistonBehavior;
import net.minecraft.block.entity.BlockEntityType;
import net.minecraft.sound.BlockSoundGroup;
import net.minecraft.util.Identifier;

public class LazyPathways implements ModInitializer{

        public static Logger LOGGER = LogManager.getLogger();

        public static final String MOD_ID = "lazypathways";
        public static final String MOD_NAME = "Lazy Pathways";

    public static final Block PATH_BLOCK = new PathBlock(FabricBlockSettings.create().mapColor(MapColor.DIRT_BROWN).pistonBehavior(PistonBehavior.DESTROY).hardness(0.5f).sounds(BlockSoundGroup.GRASS));
        public static final Block LAWN_BLOCK = new LawnBlock(FabricBlockSettings.create().mapColor(MapColor.DIRT_BROWN).pistonBehavior(PistonBehavior.DESTROY).hardness(0.5f).sounds(BlockSoundGroup.GRASS));

        public static final BlockItem LAWN_ITEM = new BlockItem(LAWN_BLOCK, new Item.Settings());
        public static final BlockItem PATH_ITEM = new BlockItem(PATH_BLOCK, new Item.Settings());

        public static BlockEntityType<PathEntity> PATH_ENTITY;

    @Override
    public void onInitialize() {
        log(Level.INFO, "Initializing");

        log(Level.INFO, "Register Blocks");

        Registry.register(Registries.BLOCK, Identifier.of("lazypathways", "path"), PATH_BLOCK);
        ItemGroupEvents.modifyEntriesEvent(ItemGroups.NATURAL).register(entries -> entries.add(PATH_ITEM));
        Registry.register(Registries.ITEM, Identifier.of("lazypathways", "path"), PATH_ITEM);

        Registry.register(Registries.BLOCK, Identifier.of("lazypathways", "lawn"), LAWN_BLOCK);
        ItemGroupEvents.modifyEntriesEvent(ItemGroups.NATURAL).register(entries -> entries.add(LAWN_ITEM));
        Registry.register(Registries.ITEM, Identifier.of("lazypathways", "lawn"), LAWN_ITEM);

        PATH_ENTITY = Registry.register(Registries.BLOCK_ENTITY_TYPE, "lazypathways:path", FabricBlockEntityTypeBuilder.create(PathEntity::new, PATH_BLOCK).build());

        log(Level.INFO, "Initializing config");
        AutoConfig.register(LazyPathwaysConfig.class, GsonConfigSerializer::new);
    }

    public static void log(Level level, String message){
        LOGGER.log(level, "["+MOD_NAME+"] " + message);
    }


}