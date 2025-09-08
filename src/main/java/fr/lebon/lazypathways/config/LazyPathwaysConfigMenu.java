package fr.lebon.lazypathways.config;

import com.terraformersmc.modmenu.api.ConfigScreenFactory;
import com.terraformersmc.modmenu.api.ModMenuApi;

import me.shedaniel.autoconfig.AutoConfig;
import net.fabricmc.api.EnvType;
import net.fabricmc.api.Environment;

public class LazyPathwaysConfigMenu implements ModMenuApi{

    @Override
    @Environment(EnvType.CLIENT)
    public ConfigScreenFactory<?> getModConfigScreenFactory() {
        return parent -> AutoConfig.getConfigScreen(LazyPathwaysConfig.class, parent).get();
    }
}
