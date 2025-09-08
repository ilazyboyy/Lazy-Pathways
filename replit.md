# Overview

Lazy Pathways is a Minecraft mod for Fabric that automatically creates beautiful pathways as players and entities walk on grass blocks. The mod progressively transforms grass blocks into worn path blocks through repeated use, creating natural-looking trails that evolve over time. It features multiple visual stages of path degradation, configurable timing settings, and optional permanent path creation.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Core Framework
- **Fabric Mod Platform**: Built on Minecraft Fabric loader for version 1.21.1+ with Java 21 compatibility
- **Mixin-Based Architecture**: Uses Fabric's mixin system to modify vanilla Minecraft behavior without directly editing game code
- **Event-Driven Design**: Intercepts block stepping events to trigger path creation and progression

### Block System Design
- **Progressive Path States**: Implements 5-level path degradation system from fresh grass to worn dirt paths
- **Dynamic Block Models**: Each path level has distinct visual appearance with custom textures and block models
- **Blockstate Management**: Uses Minecraft's blockstate system to handle visual variations and rotations
- **Custom Block Types**: Introduces "lawn" and "path" blocks as intermediate states between grass and dirt

### Game Integration Strategy
- **Vanilla Compatibility**: Integrates seamlessly with existing Minecraft mechanics through block tags
- **Plant Compatibility**: Ensures plants can still grow on path blocks through mixin modifications
- **Animal Behavior**: Maintains proper mob spawning and interaction with path blocks
- **Tool Interaction**: Preserves hoe functionality while adding path creation behavior

### Configuration System
- **ModMenu Integration**: Provides in-game configuration interface for mod settings
- **Timing Controls**: Configurable upgrade/downgrade timing for path progression
- **Mob Path Creation**: Optional setting to enable path creation by non-player entities
- **Permanent Path Option**: Configurable permanent path creation after repeated use

### Resource Management
- **Multilingual Support**: Localization files for English and French languages
- **Asset Organization**: Structured asset files for textures, models, blockstates, and recipes
- **Loot Table Integration**: Custom loot tables for proper item drops when blocks are broken

## External Dependencies

### Core Dependencies
- **Fabric Loader**: Version 0.16.9+ required for mod loading and mixin support
- **Fabric API**: Full Fabric API compatibility for comprehensive mod functionality
- **Minecraft**: Version 1.21.1+ compatibility with intermediary mappings
- **Java Runtime**: Java 21+ required for modern language features

### Optional Integrations
- **ModMenu**: Provides configuration GUI when present
- **Silk Touch Enchantment**: Special behavior for harvesting custom blocks with silk touch tools

### Asset Dependencies
- **Vanilla Textures**: Leverages existing Minecraft textures (grass, dirt) as base materials
- **Custom Overlays**: Custom texture overlays for different path wear levels
- **Block Model System**: Extends Minecraft's block model format for multi-layered rendering