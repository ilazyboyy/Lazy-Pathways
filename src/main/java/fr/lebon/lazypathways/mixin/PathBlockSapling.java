package fr.lebon.lazypathways.mixin;

import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

import fr.lebon.lazypathways.LazyPathways;
import net.minecraft.block.BlockState;
import net.minecraft.world.gen.feature.Feature;

@Mixin(Feature.class) 
public class PathBlockSapling {
        @Inject(method = "isSoil(Lnet/minecraft/block/BlockState;)Z", cancellable = true, at = @At(value = "RETURN"))
    private static void makePathSaplingable(BlockState state, CallbackInfoReturnable<Boolean> cir) {
        if (!cir.getReturnValue() && (state.isOf(LazyPathways.PATH_BLOCK) || state.isOf(LazyPathways.LAWN_BLOCK))) cir.setReturnValue(true);
    }
}