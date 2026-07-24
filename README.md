# The Watcher Mod - Complete Horror Mod for Minecraft 1.20.1

A terrifying horror modification for Minecraft featuring "The Watcher" - an advanced AI-driven entity designed to create psychological horror and paranoia.

## Features Implemented

### Entity: The Watcher
- **3-block tall creature** with custom model and animations
- **Glowing white eyes** for intimidating appearance
- **Advanced AI behaviors**:
  - Observes players from distance
  - Circles around the player
  - Remembers encounters during the session
  - Attacks only after multiple encounters
  - Occasional disappearances and teleportation
  - Only spawns during night time

### Paranormal Events System
- Flickering lights
- Torch extinguishing
- Paranoid sounds (breathing, whispers, footsteps)
- Fog effects
- Screen distortion
- Dynamic darkness
- Random events that trigger paranoia

### AI Psychological Features
- Non-immediate attacks
- Paranoia building mechanic
- Player tracking and circling
- Encounter counter system
- Threat escalation based on encounters
- Hide/peek behavior from terrain

### Configuration System
- Customizable spawn rate
- Adjustable health and damage
- Movement speed control
- Event frequency settings
- Sound toggle
- Fog toggle
- Jumpscare toggle

## Project Structure

```
minecraft-watcher-mod/
├── build.gradle              # Gradle build configuration
├── settings.gradle           # Gradle settings
├── src/
│   └── main/
│       ├── java/
│       │   └── com/samuel/watcher/
│       │       ├── WatcherMod.java          # Main mod class
│       │       ├── config/
│       │       │   └── WatcherConfig.java   # Configuration
│       │       ├── entity/
│       │       │   ├── ModEntities.java     # Entity registry
│       │       │   ├── WatcherEntity.java   # Main entity
│       │       │   ├── WatcherAIGoal.java   # AI behavior
│       │       │   ├── WatcherModel.java    # 3D model
│       │       │   ├── WatcherRenderer.java # Renderer
│       │       │   └── WatcherSpawnHelper.java
│       │       ├── event/
│       │       │   ├── EntitySpawnHandler.java
│       │       │   ├── ParanormalEvents.java
│       │       │   ├── ClientSetupEvents.java
│       │       │   └── CommonSetupEvents.java
│       │       └── client/
│       │           └── ClientEvents.java
│       └── resources/
│           ├── META-INF/
│           │   └── mods.toml               # Mod metadata
│           └── assets/watcher/
│               ├── lang/
│               │   └── en_us.json          # English translations
│               ├── sounds.json             # Sound definitions
│               ├── models/entity/
│               │   └── watcher.json        # Entity model
│               └── textures/entity/
│                   └── watcher.png         # Entity texture
└── README.md

```

## Building

### Requirements
- Java 17+
- Gradle 8.0+
- Git

### Compile

```bash
./gradlew build
```

The compiled JAR will be located at:
```
build/libs/watcher-mod-1.0.0.jar
```

## Installation

1. Download `watcher-mod-1.0.0.jar`
2. Place it in your Minecraft `mods` folder
3. Launch Minecraft with Forge 47.x for version 1.20.1

## Configuration

After first launch, configuration file appears at:
```
config/watcher-server.toml
config/watcher-client.toml
```

### Server Config Options
- `spawnRate` (1-100): How often The Watcher spawns
- `watcherHealth` (10-100): Maximum health
- `watcherDamage` (1-20): Damage per attack
- `watcherSpeed` (0.1-1.0): Movement speed
- `appearanceDistance` (16-256): Max spawn distance from player
- `eventFrequency` (1-50): Paranormal event frequency
- `enableSounds`: Toggle entity sounds
- `enableFog`: Toggle fog effects
- `enableJumpscares`: Toggle jumpscare events

### Client Config Options
- `enableParticles`: Visual particle effects
- `fogDistance` (5-100): Fog rendering distance
- `screenDistortion` (0-10): Screen effect intensity

## Gameplay Features

### The Watcher Behavior

**First Encounter:**
- Silently observes from distance
- Circles the player
- Creates paranoia through presence alone

**Subsequent Encounters:**
- Gets closer
- More aggressive circling
- Occasional teleportation behind player
- Triggers paranormal events

**After 3+ Encounters:**
- Becomes hostile
- Charges at player
- Deals significant damage
- Can enter buildings

### Paranormal Events

These random events trigger to increase fear:
1. **Light Flicker** - Nearby lights flicker on/off
2. **Paranoid Sounds** - Breathing, whispers, footsteps
3. **Fog Effect** - Thick fog appears around player
4. **Chest Event** - Nearby chests close unexpectedly
5. **Door Event** - Doors open/close randomly
6. **Torch Extinguish** - Torches go out
7. **Shadow Flicker** - Quick shadow appears
8. **Whisper** - Unsettling whisper sounds

## Technical Specifications

- **Target Version**: Minecraft 1.20.1
- **Forge Version**: 47.x
- **Java Version**: 17+
- **Model Format**: Blockbench-compatible
- **License**: All rights reserved

## Development Notes

### Code Quality
- Clean, well-documented code
- No compilation warnings
- Optimized AI pathfinding
- Efficient event handling

### Performance
- Entity rendering optimized for distance
- Efficient collision detection
- AI updates limited to necessary ticks
- Event frequency configurable for performance

## Future Features (Planned)

- Multiple variants of The Watcher
- Custom sounds and music
- Loot drops and rewards
- Integration with other horror mods
- Custom dimensions/biomes
- Advanced animation system

## Credits

Created by Samuel TheYlor

## Support

For issues, suggestions, or questions, refer to the project repository.

---

**Warning**: This mod is designed to be scary. Not recommended for young children or those sensitive to horror themes.
