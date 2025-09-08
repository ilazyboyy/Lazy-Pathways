# Lazy Pathways

**Lazy Pathways** is a Minecraft Fabric mod that automatically creates beautiful, evolving pathways as you walk on grass blocks. Watch as natural paths form organically beneath your feet and gradually wear down with use!

## ✨ Features

### 🦶 **Automatic Path Creation**
- Walk on grass blocks to automatically convert them into path blocks
- No tools required - just walk where you want paths to appear
- Works with players and optionally with mobs (configurable)

### 🌱 **Dynamic Path Evolution**
- **5 Visual Stages**: Paths evolve from fresh grass-like appearance to well-worn dirt paths
- **Time-Based Progression**: Paths naturally upgrade with use and downgrade over time
- **Smart Lifecycle**: Heavily used paths can become permanent or convert to vanilla dirt paths

### 🎨 **Immersive Visual Design**
- **Biome-Aware Colors**: Path colors automatically match your local biome's grass tones
- **Natural Progression**: Fresh paths look grassy, worn paths look like authentic dirt
- **Randomized Textures**: Each path block rotates randomly to eliminate repetitive patterns
- **Subtle Terrain Blending**: Enhanced color blending creates seamless integration with surroundings

### 🔊 **Dynamic Audio Experience**
- **Progressive Sound Design**: Audio changes based on path wear level
  - Level 1-2: Grass footsteps (fresh paths)
  - Level 3: Rooted dirt sounds (moderate wear)
  - Level 4-5: Mud sounds (well-worn paths)
- **Immersive Feedback**: Hear the difference as paths become more established

### ⚙️ **Highly Configurable**
- **Timing Control**: Adjust upgrade/downgrade intervals
- **Mob Pathways**: Enable/disable mob path creation
- **Permanent Paths**: Configure if heavily used paths become permanent
- **Visual Options**: Control texture blending intensity
- **ModMenu Integration**: Easy in-game configuration

### 🌿 **Vanilla Integration**
- **Plant Compatibility**: Most vanilla plants can grow on path blocks
- **Fertilizable**: Use bone meal on early-stage paths to grow plants
- **Farmable**: Use hoes to convert paths back to farmland
- **Animal Friendly**: Animals can graze on path blocks

## 📋 Requirements

- **Minecraft**: 1.21.1
- **Fabric Loader**: 0.16.9+
- **Java**: 21
- **Dependencies**:
  - Fabric API
  - Cloth Config (for configuration GUI)
  - ModMenu (for in-game config access)

## 🚀 Installation

1. Install [Fabric Loader](https://fabricmc.net/use/installer/)
2. Download the latest release from [Releases](../../releases)
3. Place the `.jar` file in your `mods` folder
4. Install required dependencies (Fabric API, Cloth Config, ModMenu)
5. Launch Minecraft and enjoy!

## 🎮 Usage

### Basic Usage
1. **Walk on grass blocks** - they'll automatically convert to path blocks
2. **Keep using paths** - they'll upgrade to more worn appearances over time
3. **Leave paths unused** - they'll gradually revert to grass after ~38 seconds
4. **Create networks** - paths connect visually and blend with each other

### Configuration
- Access settings via **ModMenu** in the mods screen
- Or edit `config/lazypathways.json` directly
- Adjust timing, enable mob paths, configure permanence options

### Tips
- **High-traffic areas** naturally develop into permanent pathways
- **Seasonal paths** will fade back to grass if unused
- **Use bone meal** on fresh paths to grow decorative plants
- **Hoe paths** to convert them back to farmland for farming

## ⚡ Performance

Lazy Pathways is designed with performance in mind:
- **Efficient block updates** using optimized update flags
- **Smart neighbor detection** only checks relevant adjacent blocks  
- **Color caching system** reduces redundant biome color calculations
- **Minimal network overhead** with custom block entity ticking

## 🔧 Technical Details

### Path Mechanics
- **5 progression levels** with distinct visual and audio characteristics
- **Block entity system** manages upgrade/downgrade timing
- **Neighbor-aware rendering** for seamless path networks
- **Biome integration** for natural color matching

### Compatibility
- **Fabric ecosystem** - works with most Fabric mods
- **Vanilla mechanics** - integrates seamlessly with existing gameplay
- **Plant mods** - compatible with mods that add new plant types
- **Performance mods** - works alongside optimization mods

## 📸 Screenshots

*Add your favorite screenshots of path networks here!*

## 🤝 Contributing

Contributions are welcome! Please feel free to:
- Report bugs via [Issues](../../issues)
- Submit feature requests
- Create pull requests for improvements
- Share screenshots of your path creations

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Fabric](https://fabricmc.net/)
- Uses [Cloth Config](https://github.com/shedaniel/cloth-config) for configuration
- Integrated with [ModMenu](https://github.com/Prospector/ModMenu)

---

**Lazy Pathways** - *Let your footsteps tell the story* 🛤️
