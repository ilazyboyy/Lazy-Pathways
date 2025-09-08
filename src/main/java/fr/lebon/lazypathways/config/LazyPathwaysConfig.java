package fr.lebon.lazypathways.config;


import me.shedaniel.autoconfig.ConfigData;
import me.shedaniel.autoconfig.annotation.Config;
import me.shedaniel.autoconfig.annotation.ConfigEntry;

@Config(name = "lazypathways")
public class LazyPathwaysConfig implements ConfigData {
    @ConfigEntry.Gui.Tooltip()
    public boolean enableMobPathCreation = false; //Mob aren't enable by default for performance issue
    @ConfigEntry.Gui.Tooltip()
    public int downgradeTime = 760;
    @ConfigEntry.Gui.Tooltip()
    public int upgradeTime = 280;
    @ConfigEntry.Gui.Tooltip()
    public boolean permanentPath = false;
    @ConfigEntry.Gui.Tooltip()
    public int steppedBeforePermanent = 12;
    @ConfigEntry.Gui.Tooltip()
    public boolean permanentAsDirtPath = false;
    @ConfigEntry.Gui.Tooltip()
    public boolean enableTextureBlending = true;
    @ConfigEntry.Gui.Tooltip()
    public float blendingIntensity = 0.4f;
}
