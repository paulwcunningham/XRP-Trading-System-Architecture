#!/usr/bin/env python3
"""
Checkpoint Manager for XRP Trading System
Manages project checkpoints and state transitions
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional

class CheckpointManager:
    def __init__(self, state_file: str = "state_management/current_state.json"):
        self.state_file = state_file
        self.checkpoints_dir = "state_management/checkpoints"
        os.makedirs(self.checkpoints_dir, exist_ok=True)
    
    def load_state(self) -> Dict:
        """Load current project state"""
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_state(self, state: Dict) -> None:
        """Save current project state"""
        with open(self.state_file, 'w') as f:
            json.dump(state, f, indent=2)
    
    def create_checkpoint(self, description: str, details: Dict = None) -> str:
        """Create a new checkpoint"""
        state = self.load_state()
        
        # Generate checkpoint ID
        checkpoint_count = len(state.get('checkpoints', []))
        checkpoint_id = f"cp_{checkpoint_count + 1:03d}"
        timestamp = datetime.utcnow().isoformat() + "Z"
        
        # Create checkpoint data
        checkpoint = {
            "checkpoint_id": checkpoint_id,
            "timestamp": timestamp,
            "description": description,
            "state": details or {},
            "project_state_snapshot": state.copy()
        }
        
        # Save checkpoint file
        checkpoint_file = f"{self.checkpoints_dir}/{checkpoint_id}_{timestamp.replace(':', '-')}.json"
        with open(checkpoint_file, 'w') as f:
            json.dump(checkpoint, f, indent=2)
        
        # Update main state
        if 'checkpoints' not in state:
            state['checkpoints'] = []
        
        state['checkpoints'].append({
            "checkpoint_id": checkpoint_id,
            "timestamp": timestamp,
            "description": description,
            "state": details or "Checkpoint created successfully"
        })
        
        self.save_state(state)
        
        print(f"✅ Checkpoint {checkpoint_id} created: {description}")
        return checkpoint_id
    
    def list_checkpoints(self) -> List[Dict]:
        """List all checkpoints"""
        state = self.load_state()
        return state.get('checkpoints', [])
    
    def restore_checkpoint(self, checkpoint_id: str) -> bool:
        """Restore from a specific checkpoint"""
        checkpoint_files = [f for f in os.listdir(self.checkpoints_dir) if f.startswith(checkpoint_id)]
        
        if not checkpoint_files:
            print(f"❌ Checkpoint {checkpoint_id} not found")
            return False
        
        checkpoint_file = os.path.join(self.checkpoints_dir, checkpoint_files[0])
        
        with open(checkpoint_file, 'r') as f:
            checkpoint = json.load(f)
        
        # Restore state
        restored_state = checkpoint['project_state_snapshot']
        self.save_state(restored_state)
        
        print(f"✅ Restored from checkpoint {checkpoint_id}: {checkpoint['description']}")
        return True
    
    def update_current_phase(self, phase_name: str, status: str, progress: int = 0, current_task: str = "", next_task: str = "") -> None:
        """Update current phase information"""
        state = self.load_state()
        
        if 'current_phase' not in state:
            state['current_phase'] = {}
        
        state['current_phase'].update({
            "phase_name": phase_name,
            "status": status,
            "progress_percentage": progress,
            "current_task": current_task,
            "next_task": next_task,
            "last_updated": datetime.utcnow().isoformat() + "Z"
        })
        
        self.save_state(state)
        print(f"📊 Phase updated: {phase_name} ({progress}% complete)")
    
    def add_issue(self, issue: str, severity: str, description: str, action_required: str) -> None:
        """Add a new issue to track"""
        state = self.load_state()
        
        if 'current_issues' not in state:
            state['current_issues'] = []
        
        new_issue = {
            "issue": issue,
            "severity": severity,
            "description": description,
            "action_required": action_required,
            "created_at": datetime.utcnow().isoformat() + "Z"
        }
        
        state['current_issues'].append(new_issue)
        self.save_state(state)
        print(f"⚠️  Issue added: {issue} ({severity})")
    
    def resolve_issue(self, issue_text: str) -> bool:
        """Mark an issue as resolved"""
        state = self.load_state()
        
        if 'current_issues' not in state:
            return False
        
        for i, issue in enumerate(state['current_issues']):
            if issue_text.lower() in issue['issue'].lower():
                resolved_issue = state['current_issues'].pop(i)
                
                if 'resolved_issues' not in state:
                    state['resolved_issues'] = []
                
                resolved_issue['resolved_at'] = datetime.utcnow().isoformat() + "Z"
                state['resolved_issues'].append(resolved_issue)
                
                self.save_state(state)
                print(f"✅ Issue resolved: {resolved_issue['issue']}")
                return True
        
        return False
    
    def get_status_summary(self) -> str:
        """Get a comprehensive status summary"""
        state = self.load_state()
        
        summary = []
        summary.append("🎯 XRP Trading System - Status Summary")
        summary.append("=" * 50)
        
        # Current phase
        if 'current_phase' in state:
            phase = state['current_phase']
            summary.append(f"📊 Current Phase: {phase.get('phase_name', 'Unknown')}")
            summary.append(f"   Status: {phase.get('status', 'Unknown')}")
            summary.append(f"   Progress: {phase.get('progress_percentage', 0)}%")
            summary.append(f"   Current Task: {phase.get('current_task', 'None')}")
        
        # Repository status
        if 'repositories_status' in state:
            summary.append("\n📦 Repository Status:")
            for repo, status in state['repositories_status'].items():
                workflow_status = status.get('workflow_status', 'Unknown')
                emoji = "✅" if workflow_status == "SUCCESS" else "❌" if workflow_status == "FAILED" else "⚠️"
                summary.append(f"   {emoji} {repo}: {workflow_status}")
        
        # Current issues
        if 'current_issues' in state and state['current_issues']:
            summary.append(f"\n🚨 Active Issues ({len(state['current_issues'])}):")
            for issue in state['current_issues']:
                severity_emoji = "🔴" if issue['severity'] == "CRITICAL" else "🟡" if issue['severity'] == "HIGH" else "🟢"
                summary.append(f"   {severity_emoji} {issue['issue']}")
        
        # Recent checkpoints
        if 'checkpoints' in state and state['checkpoints']:
            recent_checkpoints = state['checkpoints'][-3:]
            summary.append(f"\n📋 Recent Checkpoints:")
            for cp in recent_checkpoints:
                summary.append(f"   • {cp['checkpoint_id']}: {cp['description']}")
        
        return "\n".join(summary)

def main():
    """Command line interface for checkpoint manager"""
    if len(sys.argv) < 2:
        print("Usage: python3 checkpoint_manager.py <command> [args...]")
        print("Commands:")
        print("  create <description> - Create new checkpoint")
        print("  list - List all checkpoints")
        print("  restore <checkpoint_id> - Restore from checkpoint")
        print("  status - Show status summary")
        print("  update-phase <name> <status> [progress] - Update current phase")
        print("  add-issue <issue> <severity> <description> <action> - Add new issue")
        print("  resolve-issue <issue_text> - Resolve an issue")
        return
    
    manager = CheckpointManager()
    command = sys.argv[1]
    
    if command == "create":
        if len(sys.argv) < 3:
            print("Usage: create <description>")
            return
        description = " ".join(sys.argv[2:])
        manager.create_checkpoint(description)
    
    elif command == "list":
        checkpoints = manager.list_checkpoints()
        print("📋 Available Checkpoints:")
        for cp in checkpoints:
            print(f"  {cp['checkpoint_id']}: {cp['description']} ({cp['timestamp']})")
    
    elif command == "restore":
        if len(sys.argv) < 3:
            print("Usage: restore <checkpoint_id>")
            return
        checkpoint_id = sys.argv[2]
        manager.restore_checkpoint(checkpoint_id)
    
    elif command == "status":
        print(manager.get_status_summary())
    
    elif command == "update-phase":
        if len(sys.argv) < 4:
            print("Usage: update-phase <name> <status> [progress]")
            return
        name = sys.argv[2]
        status = sys.argv[3]
        progress = int(sys.argv[4]) if len(sys.argv) > 4 else 0
        manager.update_current_phase(name, status, progress)
    
    elif command == "add-issue":
        if len(sys.argv) < 6:
            print("Usage: add-issue <issue> <severity> <description> <action>")
            return
        issue = sys.argv[2]
        severity = sys.argv[3]
        description = sys.argv[4]
        action = sys.argv[5]
        manager.add_issue(issue, severity, description, action)
    
    elif command == "resolve-issue":
        if len(sys.argv) < 3:
            print("Usage: resolve-issue <issue_text>")
            return
        issue_text = sys.argv[2]
        if not manager.resolve_issue(issue_text):
            print(f"❌ Issue not found: {issue_text}")
    
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
