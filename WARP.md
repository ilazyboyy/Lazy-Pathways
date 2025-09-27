# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

Lazy Pathways is a Fabric mod for Minecraft that automatically creates beautiful pathways as players and entities walk on grass blocks. The mod transforms grass blocks into graduated path blocks that evolve over time based on usage and can eventually become permanent paths.

**Tech Stack:**
- Java 21
- Minecraft 1.21.1
- Fabric Mod Loader
- Gradle with Fabric Loom
- Cloth Config for configuration GUI
- ModMenu integration

## Core Architecture

### Main Components

1. **Block System** (`blocks/`):
   - `PathBlock`: The main pathway block with 5 visual states, tracks usage via block entity
   - `LawnBlock`: Decorative grass alternative that can be fertilized

2. **Block Entity** (`entity/PathEntity.java`):
   - Manages path lifecycle (upgrade/downgrade timing)
   - Tracks step counts and permanence logic
   - Handles configuration-based behavior (downgrades after ~38s, upgrades after ~14s)

3. **Mixins** (`mixin/`):
   - `BlockOnStepped`: Core functionality - transforms grass to paths when stepped on
   - `HoeMixin`: Allows paths to be tilled back to farmland
   - Plant-related mixins: Enable planting on path blocks (sugar cane, saplings, etc.)
   - `EatGoalCanStart`: Allows animals to graze on path blocks

4. **Configuration** (`config/`):
   - `LazyPathwaysConfig`: Configurable timing, mob path creation, permanence settings
   - `LazyPathwaysConfigMenu`: ModMenu integration for in-game config

5. **Utilities** (`util/`):
   - `ColorProvider`: Biome-aware coloring for path blocks with texture blending system
   - `GrowRoutineGrassBlock`: Bone meal growth mechanics for paths

### Key Mechanics

- **Path Evolution**: Paths have 5 visual states that upgrade with use and downgrade over time
- **Permanent Paths**: After sufficient use, paths can become permanent or convert to vanilla dirt paths
- **Biome Integration**: Path colors adapt to surrounding biome grass colors
- **Plant Compatibility**: Most vanilla plants can grow on path blocks
- **Texture Blending**: Dynamic color blending with neighboring blocks for natural integration
- **Performance Optimization**: Uses custom block update flags to avoid unnecessary neighbor notifications

## Common Development Tasks

### Building and Testing
```bash
# Build the mod
./gradlew build

# Run in development client
./gradlew runClient

# Run development server
./gradlew runServer

# Clean build artifacts
./gradlew clean

# Run tests
./gradlew test

# Check available tasks
./gradlew tasks
```

### Development Setup
```bash
# Generate IDE workspace
./gradlew genIdeaWorkspace  # For IntelliJ
./gradlew vscode            # For VS Code
./gradlew genEclipseRuns    # For Eclipse

# Generate mappings/sources
./gradlew genSources
```

### Publishing
```bash
# Build distribution jar
./gradlew remapJar

# Publish to local Maven
./gradlew publishToMavenLocal

# Upload to CurseForge (requires APICURSE env var)
./gradlew curseforge
```

## Code Patterns and Conventions

### Block State Management
- Use `PathBlock.SKIP_ALL_NEIGHBOR_AND_LIGHTING_UPDATES` for performance-critical block updates
- Path blocks use `STATE_RENDER` (1-5) for visual progression and `STEPPED` boolean for interaction tracking

### Configuration Access
```java
LazyPathwaysConfig config = AutoConfig.getConfigHolder(LazyPathwaysConfig.class).getConfig();
```

### Texture Blending System
- Enabled by default with configurable intensity (`blendingIntensity`)
- Uses intelligent caching for performance optimization
- Analyzes 4 horizontal neighbors and applies weighted color averages
- Higher wear levels blend less (representing compacted earth)

### Mixin Patterns
- Use `@Inject(method = "methodName", at = @At("HEAD"))` for method interception
- Call `cir.cancel()` to prevent original method execution after custom logic
- Target specific entity types with `instanceof` checks for performance

### Block Entity Ticking
- Server-side only ticking via `getTicker()` method
- Use `world.isClient()` guards in tick methods
- Convert config seconds to ticks by multiplying by 20

### Registration Patterns
- Register blocks first, then items referencing those blocks
- Use `Identifier.of("lazypathways", name)` for resource locations
- Add items to creative tabs via `ItemGroupEvents.modifyEntriesEvent()`

## File Structure Context

- `src/main/java/fr/lebon/lazypathways/` - Main source code
- `src/main/resources/assets/lazypathways/` - Client-side assets (models, textures, lang)
- `src/main/resources/data/` - Data generation (loot tables, recipes, tags)
- `build.gradle` - Build configuration with Fabric Loom
- `gradle.properties` - Version and dependency management
- `fabric.mod.json` - Mod metadata and entrypoints
- `lazypathways.mixins.json` - Mixin configuration
- `TEXTURE_BLENDING.md` - Detailed texture blending system documentation

## Development Notes

### Key Configuration Values
- Default upgrade time: 280 ticks (~14 seconds)
- Default downgrade time: 760 ticks (~38 seconds) 
- Default steps before permanent: 12
- Texture blending intensity: 0.4 (40% neighbor influence)

### Performance Considerations
- Config access should be cached during entity creation to avoid repeated lookups
- Block entity ticking is server-side only
- Custom update flags reduce unnecessary neighbor notifications
- Texture blending uses intelligent caching system

## Version Compatibility

- Requires Java 21
- Built for Minecraft 1.21.1
- Uses Fabric API and Fabric Loader 0.16.9+
- Compatible with Cloth Config and ModMenu
