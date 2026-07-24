package com.samuel.watcher.entity;

import net.minecraft.world.DifficultyInstance;
import net.minecraft.world.entity.MobSpawnType;
import net.minecraft.world.level.LevelAccessor;

public class WatcherSpawnRules {
    
    public static boolean checkWatcherSpawnRules(
            net.minecraft.world.entity.EntityType<WatcherEntity> entityType,
            LevelAccessor level,
            MobSpawnType spawnType,
            net.minecraft.core.BlockPos blockPos,
            java.util.Random random) {
        
        // Only spawn at night
        long dayTime = level.getLevel().getDayTime() % 24000L;
        if (dayTime < 13000L && dayTime >= 11000L) {
            return false;
        }
        
        // Check spawn rate
        return random.nextInt(100) < 5;
    }
}
