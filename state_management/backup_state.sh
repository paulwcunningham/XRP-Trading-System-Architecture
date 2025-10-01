#!/bin/bash
# Automated State Backup Script for XRP Trading System

set -e

# Configuration
REPO_DIR="/home/ubuntu/state_repo"
BACKUP_DIR="$REPO_DIR/state_management/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="state_backup_$TIMESTAMP.tar.gz"

# Ensure backup directory exists
mkdir -p "$BACKUP_DIR"

echo "🔄 Creating state backup at $(date)"

# Create comprehensive backup
cd "$REPO_DIR"
tar -czf "$BACKUP_DIR/$BACKUP_FILE" \
    state_management/current_state.json \
    state_management/ai_prompts/ \
    state_management/logs/ \
    *.md \
    *.yml \
    *.json 2>/dev/null || true

# Backup working directories from main system
if [ -d "/home/ubuntu/SignalEngine" ]; then
    echo "📦 Backing up SignalEngine working directory..."
    tar -czf "$BACKUP_DIR/signalengine_working_$TIMESTAMP.tar.gz" -C /home/ubuntu SignalEngine
fi

if [ -d "/home/ubuntu/TradeServer" ]; then
    echo "📦 Backing up TradeServer working directory..."
    tar -czf "$BACKUP_DIR/tradeserver_working_$TIMESTAMP.tar.gz" -C /home/ubuntu TradeServer
fi

if [ -d "/home/ubuntu/FeedServer" ]; then
    echo "📦 Backing up FeedServer working directory..."
    tar -czf "$BACKUP_DIR/feedserver_working_$TIMESTAMP.tar.gz" -C /home/ubuntu FeedServer
fi

if [ -d "/home/ubuntu/Monitoring-Server" ]; then
    echo "📦 Backing up Monitoring-Server working directory..."
    tar -czf "$BACKUP_DIR/monitoringserver_working_$TIMESTAMP.tar.gz" -C /home/ubuntu Monitoring-Server
fi

# Backup SSH keys and configuration
if [ -d "/home/ubuntu/.ssh" ]; then
    echo "🔐 Backing up SSH configuration..."
    tar -czf "$BACKUP_DIR/ssh_config_$TIMESTAMP.tar.gz" -C /home/ubuntu .ssh
fi

# Get current system state
echo "📊 Capturing current system state..."
cat > "$BACKUP_DIR/system_state_$TIMESTAMP.json" << EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%S.000Z)",
  "hostname": "$(hostname)",
  "working_directory": "$(pwd)",
  "git_status": {
    "current_branch": "$(git branch --show-current 2>/dev/null || echo 'unknown')",
    "last_commit": "$(git rev-parse HEAD 2>/dev/null || echo 'unknown')",
    "uncommitted_changes": $(git status --porcelain 2>/dev/null | wc -l || echo 0)
  },
  "environment": {
    "github_token_set": $([ -n "$GITHUB_TOKEN" ] && echo "true" || echo "false"),
    "ssh_keys_present": $([ -f ~/.ssh/id_ed25519 ] && echo "true" || echo "false")
  },
  "disk_usage": "$(df -h . | tail -1)",
  "memory_usage": "$(free -h | grep Mem)"
}
EOF

# Cleanup old backups (keep last 10)
echo "🧹 Cleaning up old backups..."
cd "$BACKUP_DIR"
ls -t state_backup_*.tar.gz 2>/dev/null | tail -n +11 | xargs rm -f || true
ls -t *_working_*.tar.gz 2>/dev/null | tail -n +11 | xargs rm -f || true
ls -t system_state_*.json 2>/dev/null | tail -n +11 | xargs rm -f || true

echo "✅ State backup completed: $BACKUP_FILE"
echo "📁 Backup location: $BACKUP_DIR"
echo "📊 Backup size: $(du -h "$BACKUP_DIR/$BACKUP_FILE" | cut -f1)"

# Update current state with backup info
if [ -f "$REPO_DIR/state_management/current_state.json" ]; then
    python3 << EOF
import json
import os
from datetime import datetime

state_file = "$REPO_DIR/state_management/current_state.json"
if os.path.exists(state_file):
    with open(state_file, 'r') as f:
        state = json.load(f)
    
    if 'backups' not in state:
        state['backups'] = []
    
    state['backups'].append({
        'timestamp': '$(date -u +%Y-%m-%dT%H:%M:%S.000Z)',
        'backup_file': '$BACKUP_FILE',
        'size': '$(du -h "$BACKUP_DIR/$BACKUP_FILE" | cut -f1)',
        'type': 'automated'
    })
    
    # Keep only last 5 backup records
    state['backups'] = state['backups'][-5:]
    
    with open(state_file, 'w') as f:
        json.dump(state, f, indent=2)
    
    print("📝 Updated current_state.json with backup information")
EOF
fi

echo "🎉 Backup process completed successfully!"
