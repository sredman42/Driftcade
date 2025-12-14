"""
Driftcade v1 - Update Manager
Shared logic for backups, staging, atomic deployment, and rollback.
All updaters (GitHub, email) use this module.
"""

import os
import shutil
import hashlib
import json
from datetime import datetime
from pathlib import Path


class UpdateManager:
    """Handles safe file deployment with backup and rollback."""

    # Folders that CAN be updated
    ALLOWED_FOLDERS = ["backend", "tools", "config", "experiences"]

    # Files/folders that must NEVER be updated
    PROTECTED_ITEMS = [".env", "logs", "_backups", "_update_staging", "frontend"]

    # How many backups to keep
    MAX_BACKUPS = 3

    def __init__(self, project_root):
        """
        Initialize UpdateManager.

        Args:
            project_root: Path to Driftcade_v1 folder (e.g., D:\\Driftcade_v1)
        """
        self.project_root = Path(project_root)
        self.staging_dir = self.project_root / "_update_staging"
        self.backup_dir = self.project_root / "_backups"

        # Create directories if they don't exist
        self.staging_dir.mkdir(exist_ok=True)
        self.backup_dir.mkdir(exist_ok=True)

    def is_path_allowed(self, relative_path):
        """
        Check if a file path is allowed to be updated.

        Args:
            relative_path: Path relative to project root (e.g., 'backend/app.py')

        Returns:
            True if allowed, False if protected
        """
        path_str = str(relative_path).replace("\\", "/")
        path_parts = path_str.split("/")

        # Check if path starts with a protected item
        for protected in self.PROTECTED_ITEMS:
            if path_parts[0] == protected or path_str == protected:
                return False

        # Check if path starts with an allowed folder
        for allowed in self.ALLOWED_FOLDERS:
            if path_parts[0] == allowed:
                return True

        # Default: not allowed (safe by default)
        return False

    def create_backup(self, description="manual"):
        """
        Create a backup of all allowed folders.

        Args:
            description: Short label for the backup (e.g., 'github', 'email')

        Returns:
            Path to backup folder, or None if backup failed
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_{timestamp}_{description}"
        backup_path = self.backup_dir / backup_name

        try:
            backup_path.mkdir(exist_ok=True)

            # Backup each allowed folder
            for folder in self.ALLOWED_FOLDERS:
                source = self.project_root / folder
                dest = backup_path / folder

                if source.exists():
                    shutil.copytree(source, dest)

            # Write backup metadata
            metadata = {
                "timestamp": timestamp,
                "description": description,
                "folders": self.ALLOWED_FOLDERS
            }
            metadata_file = backup_path / "backup_info.json"
            with open(metadata_file, "w") as f:
                json.dump(metadata, f, indent=2)

            # Clean old backups
            self._cleanup_old_backups()

            return backup_path

        except Exception as e:
            print(f"[UPDATE_MANAGER] Backup failed: {e}")
            return None

    def _cleanup_old_backups(self):
        """Remove old backups, keeping only MAX_BACKUPS most recent."""
        try:
            backups = sorted(self.backup_dir.iterdir(), reverse=True)
            backups = [b for b in backups if b.is_dir() and b.name.startswith("backup_")]

            while len(backups) > self.MAX_BACKUPS:
                old_backup = backups.pop()
                shutil.rmtree(old_backup)
                print(f"[UPDATE_MANAGER] Deleted old backup: {old_backup.name}")

        except Exception as e:
            print(f"[UPDATE_MANAGER] Cleanup warning: {e}")

    def clear_staging(self):
        """Clear the staging directory."""
        try:
            if self.staging_dir.exists():
                shutil.rmtree(self.staging_dir)
            self.staging_dir.mkdir(exist_ok=True)
            return True
        except Exception as e:
            print(f"[UPDATE_MANAGER] Clear staging failed: {e}")
            return False

    def stage_file(self, relative_path, content):
        """
        Stage a file for deployment.

        Args:
            relative_path: Path relative to project root (e.g., 'backend/app.py')
            content: File content as string or bytes

        Returns:
            True if staged successfully, False otherwise
        """
        if not self.is_path_allowed(relative_path):
            print(f"[UPDATE_MANAGER] BLOCKED: {relative_path} is protected")
            return False

        try:
            staged_file = self.staging_dir / relative_path
            staged_file.parent.mkdir(parents=True, exist_ok=True)

            mode = "wb" if isinstance(content, bytes) else "w"
            with open(staged_file, mode) as f:
                f.write(content)

            return True

        except Exception as e:
            print(f"[UPDATE_MANAGER] Stage failed for {relative_path}: {e}")
            return False

    def validate_staging(self):
        """
        Validate all staged files before deployment.

        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        issues = []

        if not self.staging_dir.exists():
            return False, ["Staging directory does not exist"]

        staged_files = list(self.staging_dir.rglob("*"))
        staged_files = [f for f in staged_files if f.is_file()]

        if not staged_files:
            return False, ["No files staged for deployment"]

        for staged_file in staged_files:
            relative_path = staged_file.relative_to(self.staging_dir)

            # Double-check protection
            if not self.is_path_allowed(relative_path):
                issues.append(f"Protected path in staging: {relative_path}")

            # Check file is readable
            try:
                with open(staged_file, "rb") as f:
                    f.read(1)
            except Exception as e:
                issues.append(f"Unreadable file: {relative_path} - {e}")

        return len(issues) == 0, issues

    def deploy_staged_files(self):
        """
        Deploy all staged files to their final locations.

        Returns:
            Tuple of (success, deployed_count, error_message)
        """
        # Validate first
        is_valid, issues = self.validate_staging()
        if not is_valid:
            return False, 0, f"Validation failed: {issues}"

        deployed_count = 0

        try:
            staged_files = list(self.staging_dir.rglob("*"))
            staged_files = [f for f in staged_files if f.is_file()]

            for staged_file in staged_files:
                relative_path = staged_file.relative_to(self.staging_dir)
                target_path = self.project_root / relative_path

                # Create parent directories
                target_path.parent.mkdir(parents=True, exist_ok=True)

                # Copy file (atomic on same filesystem)
                shutil.copy2(staged_file, target_path)
                deployed_count += 1
                print(f"[UPDATE_MANAGER] Deployed: {relative_path}")

            # Clear staging after successful deploy
            self.clear_staging()

            return True, deployed_count, None

        except Exception as e:
            return False, deployed_count, str(e)

    def rollback(self, backup_name=None):
        """
        Rollback to a previous backup.

        Args:
            backup_name: Specific backup folder name. If None, uses most recent.

        Returns:
            Tuple of (success, message)
        """
        try:
            if backup_name:
                backup_path = self.backup_dir / backup_name
            else:
                # Find most recent backup
                backups = sorted(self.backup_dir.iterdir(), reverse=True)
                backups = [b for b in backups if b.is_dir() and b.name.startswith("backup_")]

                if not backups:
                    return False, "No backups available"

                backup_path = backups[0]

            if not backup_path.exists():
                return False, f"Backup not found: {backup_path.name}"

            # Restore each folder from backup
            for folder in self.ALLOWED_FOLDERS:
                backup_folder = backup_path / folder
                target_folder = self.project_root / folder

                if backup_folder.exists():
                    # Remove current folder
                    if target_folder.exists():
                        shutil.rmtree(target_folder)

                    # Restore from backup
                    shutil.copytree(backup_folder, target_folder)
                    print(f"[UPDATE_MANAGER] Restored: {folder}")

            return True, f"Rolled back to {backup_path.name}"

        except Exception as e:
            return False, f"Rollback failed: {e}"

    def get_file_hash(self, file_path):
        """
        Get SHA256 hash of a file.

        Args:
            file_path: Path to file

        Returns:
            Hash string, or None if file doesn't exist
        """
        try:
            with open(file_path, "rb") as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception:
            return None


# Quick test when run directly
if __name__ == "__main__":
    print("[UPDATE_MANAGER] Self-test starting...")

    # Use current directory's parent as project root for testing
    test_root = Path(__file__).parent.parent
    manager = UpdateManager(test_root)

    print(f"[UPDATE_MANAGER] Project root: {manager.project_root}")
    print(f"[UPDATE_MANAGER] Staging dir: {manager.staging_dir}")
    print(f"[UPDATE_MANAGER] Backup dir: {manager.backup_dir}")

    # Test path protection
    test_paths = [
        ("backend/app.py", True),
        ("tools/updater.py", True),
        (".env", False),
        ("frontend/index.html", False),
        ("logs/debug.log", False),
    ]

    print("\n[UPDATE_MANAGER] Path protection tests:")
    for path, expected in test_paths:
        result = manager.is_path_allowed(path)
        status = "PASS" if result == expected else "FAIL"
        print(f"  {status}: {path} -> allowed={result}")

    print("\n[UPDATE_MANAGER] Self-test complete.")