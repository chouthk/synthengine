#!/bin/bash
# SynthEngine — Docker Watchdog
# Monitors simulation container and auto-restarts on crash.
# Ensures 24/7 unattended data production.

CONTAINER_NAME="synth_carla"
MAX_RESTARTS=50
RESTART_DELAY=5
COOLDOWN_FILE="/tmp/synth_watchdog_cooldown"

echo "🐶 SynthEngine Watchdog Started"
echo "   Monitoring container: $CONTAINER_NAME"
echo "   Max restarts: $MAX_RESTARTS"
echo ""

restart_count=0

while [ $restart_count -lt $MAX_RESTARTS ]; do
    if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
        restart_count=$((restart_count + 1))
        timestamp=$(date '+%Y-%m-%d %H:%M:%S')
        echo "[$timestamp] ⚠️  Container $CONTAINER_NAME stopped. Restart #$restart_count..."
        docker restart $CONTAINER_NAME 2>/dev/null
        echo "[$timestamp] ✅ Container restarted. Waiting ${RESTART_DELAY}s..."
        sleep $RESTART_DELAY
    fi
    sleep 2
done

echo "❌ Max restarts ($MAX_RESTARTS) reached. Manual intervention required."
