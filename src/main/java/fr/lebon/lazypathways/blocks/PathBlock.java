package fr.lebon.lazypathways.blocks;

import java.util.Random;

import fr.lebon.lazypathways.LazyPathways;
import fr.lebon.lazypathways.entity.PathEntity;
import fr.lebon.lazypathways.util.GrowRoutineGrassBlock;
import net.minecraft.block.*;
import net.minecraft.block.entity.*;
import net.minecraft.entity.Entity;
import net.minecraft.server.world.ServerWorld;
import net.minecraft.sound.BlockSoundGroup;
import net.minecraft.state.StateManager;
import net.minecraft.state.property.BooleanProperty;
import net.minecraft.state.property.IntProperty;
import net.minecraft.util.math.BlockPos;
import net.minecraft.util.math.Direction;
import net.minecraft.world.World;
import net.minecraft.world.WorldAccess;
import net.minecraft.world.WorldView;
import com.mojang.serialization.MapCodec;
import org.jetbrains.annotations.Nullable;

public class PathBlock extends BlockWithEntity implements BlockEntityProvider, Fertilizable{
    
    public static final MapCodec<PathBlock> CODEC = createCodec(PathBlock::new);

    public static final IntProperty STATE_RENDER = IntProperty.of("state_render",1,5);
    public static final BooleanProperty STEPPED = BooleanProperty.of("stepped");
    
    // Grass neighbor detection for seamless blending
    public static final BooleanProperty GRASS_NORTH = BooleanProperty.of("grass_north");
    public static final BooleanProperty GRASS_SOUTH = BooleanProperty.of("grass_south");
    public static final BooleanProperty GRASS_EAST = BooleanProperty.of("grass_east");
    public static final BooleanProperty GRASS_WEST = BooleanProperty.of("grass_west");
    
    

    /** setBlockState() flags that won't activate observers (and skips unnecessary lighting updates) */
    public static final int SKIP_ALL_NEIGHBOR_AND_LIGHTING_UPDATES = Block.NOTIFY_LISTENERS | Block.FORCE_STATE;

    @Override
    protected void appendProperties(StateManager.Builder<Block, BlockState> stateManager) {
        stateManager.add(STEPPED);
        stateManager.add(STATE_RENDER);
        stateManager.add(GRASS_NORTH);
        stateManager.add(GRASS_SOUTH);
        stateManager.add(GRASS_EAST);
        stateManager.add(GRASS_WEST);
    }

    public PathBlock(Settings settings) {
        super(settings);
        setDefaultState(getStateManager().getDefaultState()
            .with(STEPPED, false)
            .with(STATE_RENDER, 1)
            .with(GRASS_NORTH, false)
            .with(GRASS_SOUTH, false)
            .with(GRASS_EAST, false)
            .with(GRASS_WEST, false));
    }

    @Override
    protected MapCodec<? extends PathBlock> getCodec() {
        return CODEC;
    }

    @Override
    public BlockRenderType getRenderType(BlockState state) {
        return BlockRenderType.MODEL;
    }

    @Override
    public BlockEntity createBlockEntity(BlockPos pos, BlockState state) {
        return new PathEntity(pos, state);
    }

    @Override
    @Nullable
    public <T extends BlockEntity> BlockEntityTicker<T> getTicker(World world, BlockState state, BlockEntityType<T> type) {
        return world.isClient ? null : validateTicker(type, LazyPathways.PATH_ENTITY, PathEntity::tick);
    }

    @Override
    public void onSteppedOn(World world, BlockPos pos,BlockState state, Entity entity){
        if(!(world.isClient()) && entity.isAlive()){
            if (!state.get(STEPPED)) {
                world.setBlockState(pos, state.with(STEPPED, true), SKIP_ALL_NEIGHBOR_AND_LIGHTING_UPDATES);
            }
        }
    }

    @Override
    public boolean isFertilizable(WorldView world, BlockPos pos, BlockState state) {
        if(world.getBlockState(pos).get(STATE_RENDER) <= 3){ //if state ok so it can be fertilize
            return world.getBlockState(pos.up()).isAir();
        }
        return false;
    }

    @Override
    public boolean canGrow(World world, net.minecraft.util.math.random.Random random, BlockPos pos, BlockState state) {
        return true;
    }

    @Override
    public void grow(ServerWorld world, net.minecraft.util.math.random.Random random, BlockPos pos, BlockState state) {
        GrowRoutineGrassBlock.grow(world, random, pos, state, this);
    }
    
    @Override
    public BlockSoundGroup getSoundGroup(BlockState state) {
        // Get the path level (1-5)
        int pathLevel = state.get(STATE_RENDER);
        
        // Gradually transition from grass to mud based on path level
        switch (pathLevel) {
            case 1: return BlockSoundGroup.GRASS;           // Fresh path - still grassy
            case 2: return BlockSoundGroup.ROOTED_DIRT;     // Slightly more solid
            case 3: return BlockSoundGroup.PACKED_MUD;      // Getting compacted
            case 4: return BlockSoundGroup.MUD;             // Well-worn and muddy
            case 5: return BlockSoundGroup.MUD;             // Very worn, muddy
            default: return BlockSoundGroup.GRASS;
        }
    }
    
    /**
     * Checks if the block at the given position is a grass block that should cause edge blending
     */
    private boolean isGrassBlock(WorldAccess world, BlockPos pos) {
        BlockState neighborState = world.getBlockState(pos);
        Block neighborBlock = neighborState.getBlock();
        
        // Check for vanilla grass block
        if (neighborBlock == Blocks.GRASS_BLOCK) {
            return true;
        }
        
        // Check for our own lawn block (should also cause blending)
        if (neighborBlock instanceof LawnBlock) {
            return true;
        }
        
        // You can add more grass-like blocks here if needed
        // For example: mycelium, podzol, etc.
        
        return false;
    }
    
    /**
     * Updates the grass neighbor properties based on adjacent blocks
     */
    private BlockState updateGrassNeighbors(WorldAccess world, BlockPos pos, BlockState state) {
        return state
            .with(GRASS_NORTH, isGrassBlock(world, pos.north()))
            .with(GRASS_SOUTH, isGrassBlock(world, pos.south()))
            .with(GRASS_EAST, isGrassBlock(world, pos.east()))
            .with(GRASS_WEST, isGrassBlock(world, pos.west()));
    }
    
    /**
     * Called when a neighboring block changes - updates grass blending properties
     */
    @Override
    public BlockState getStateForNeighborUpdate(BlockState state, Direction direction, BlockState neighborState,
            WorldAccess world, BlockPos pos, BlockPos neighborPos) {
        // Only update grass neighbor properties for horizontal directions
        if (direction.getAxis().isHorizontal()) {
            return updateGrassNeighbors(world, pos, state);
        }
        return super.getStateForNeighborUpdate(state, direction, neighborState, world, pos, neighborPos);
    }
    
    /**
     * Called when the block is first placed - set initial grass neighbor states
     */
    @Override
    public BlockState getPlacementState(net.minecraft.item.ItemPlacementContext ctx) {
        BlockState state = this.getDefaultState();
        return updateGrassNeighbors(ctx.getWorld(), ctx.getBlockPos(), state);
    }

}
