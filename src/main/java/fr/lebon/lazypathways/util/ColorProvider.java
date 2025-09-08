package fr.lebon.lazypathways.util;

public class ColorProvider {
    public static int getColor(Object view, Object pos){
        // Simplified color provider that returns default grass color
        // This avoids client-side dependency issues during compilation
        return 0x8CBF3F; // Default grass green color
    }
}
