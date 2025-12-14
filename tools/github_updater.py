"""
Driftcade v1 - GitHub Updater
Primary update method: polls GitHub repo for changes.
Uses UpdateManager for safe deployment.
"""

import os
import time
import json
import hashlib
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# Import our update manager
from update_manager import UpdateManager


class GitHubUpdater:
    """Polls GitHub for repo changes and deploys updates."""

    # GitHub API base URL
    API_BASE = "https://api.github.com"

    # How often to check for updates (seconds)
    POLL_INTERVAL = 60

    # Repository info
    REPO_OWNER = "sredman42"
    REPO_NAME = "Driftcade"
    BRANCH = "main"

    def __init__(self, project_root, token=None):
        """
        Initialize GitHubUpdater.

        Args:
            project_root: Path to Driftcade_v1 folder
            token: GitHub Personal Access Token (optional but recommended)
        """
        self.project_root = Path(project_root)
        self.token = token or self._load_token_from_env()
        self.manager = UpdateManager(project_root)

        # Track last known commit
        self.last_commit_sha = None
        self.state_file = self.project_root / "_update_staging" / "github_state.json"

        # Load previous state
        self._load_state()

    def _load_token_from_env(self):
        """Load GitHub token from .env file."""
        env_path = self.project_root / ".env"

        if not env_path.exists():
            print("[GITHUB_UPDATER] Warning: .env file not found")
            return None

        try:
            with open(env_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("GITHUB_TOKEN="):
                        return line.split("=", 1)[1]
        except Exception as e:
            print(f"[GITHUB_UPDATER] Error reading .env: {e}")

        return None

    def _load_state(self):
        """Load last known commit SHA from state file."""
        try:
            if self.state_file.exists():
                with open(self.state_file, "r") as f:
                    state = json.load(f)
                    self.last_commit_sha = state.get("last_commit_sha")
                    print(f"[GITHUB_UPDATER] Loaded state: last commit {self.last_commit_sha[:7] if self.last_commit_sha else 'None'}")
        except Exception as e:
            print(f"[GITHUB_UPDATER] Could not load state: {e}")

    def _save_state(self):
        """Save current commit SHA to state file."""
        try:
            self.state_file.parent.mkdir(exist_ok=True)
            with open(self.state_file, "w") as f:
                json.dump({"last_commit_sha": self.last_commit_sha}, f)
        except Exception as e:
            print(f"[GITHUB_UPDATER] Could not save state: {e}")

    def _api_request(self, endpoint):
        """
        Make a GitHub API request.

        Args:
            endpoint: API endpoint (e.g., '/repos/owner/repo/commits')

        Returns:
            Parsed JSON response, or None on error
        """
        url = f"{self.API_BASE}{endpoint}"

        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Driftcade-Updater"
        }

        if self.token:
            headers["Authorization"] = f"token {self.token}"

        try:
            request = Request(url, headers=headers)
            with urlopen(request, timeout=30) as response:
                return json.loads(response.read().decode())

        except HTTPError as e:
            print(f"[GITHUB_UPDATER] HTTP Error {e.code}: {e.reason}")
            if e.code == 401:
                print("[GITHUB_UPDATER] Token may be invalid or expired")
            elif e.code == 403:
                print("[GITHUB_UPDATER] Rate limited or forbidden")
            return None

        except URLError as e:
            print(f"[GITHUB_UPDATER] Network error: {e.reason}")
            return None

        except Exception as e:
            print(f"[GITHUB_UPDATER] Request failed: {e}")
            return None

    def _download_raw_file(self, file_path):
        """
        Download a raw file from GitHub.

        Args:
            file_path: Path within repo (e.g., 'backend/app.py')

        Returns:
            File content as string, or None on error
        """
        url = f"https://raw.githubusercontent.com/{self.REPO_OWNER}/{self.REPO_NAME}/{self.BRANCH}/{file_path}"

        headers = {"User-Agent": "Driftcade-Updater"}

        if self.token:
            headers["Authorization"] = f"token {self.token}"

        try:
            request = Request(url, headers=headers)
            with urlopen(request, timeout=30) as response:
                return response.read().decode()

        except Exception as e:
            print(f"[GITHUB_UPDATER] Failed to download {file_path}: {e}")
            return None

    def get_latest_commit(self):
        """
        Get the latest commit SHA from the repo.

        Returns:
            Commit SHA string, or None on error
        """
        endpoint = f"/repos/{self.REPO_OWNER}/{self.REPO_NAME}/commits/{self.BRANCH}"
        data = self._api_request(endpoint)

        if data and "sha" in data:
            return data["sha"]

        return None

    def get_changed_files(self, since_sha=None):
        """
        Get list of files changed since a commit.

        Args:
            since_sha: Commit SHA to compare from. If None, gets all files.

        Returns:
            List of file paths that changed
        """
        if since_sha:
            # Compare commits
            endpoint = f"/repos/{self.REPO_OWNER}/{self.REPO_NAME}/compare/{since_sha}...{self.BRANCH}"
            data = self._api_request(endpoint)

            if data and "files" in data:
                return [f["filename"] for f in data["files"]]

            return []

        else:
            # Get all files in repo (initial sync)
            return self._get_all_repo_files()

    def _get_all_repo_files(self):
        """Get all files in the repository."""
        endpoint = f"/repos/{self.REPO_OWNER}/{self.REPO_NAME}/git/trees/{self.BRANCH}?recursive=1"
        data = self._api_request(endpoint)

        if data and "tree" in data:
            return [
                item["path"]
                for item in data["tree"]
                if item["type"] == "blob"  # Only files, not directories
            ]

        return []

    def check_for_updates(self):
        """
        Check if there are new commits to deploy.

        Returns:
            Tuple of (has_updates, latest_sha, changed_files)
        """
        print("[GITHUB_UPDATER] Checking for updates...")

        latest_sha = self.get_latest_commit()

        if not latest_sha:
            print("[GITHUB_UPDATER] Could not get latest commit")
            return False, None, []

        if latest_sha == self.last_commit_sha:
            print("[GITHUB_UPDATER] Already up to date")
            return False, latest_sha, []

        # Get changed files
        changed_files = self.get_changed_files(self.last_commit_sha)

        # Filter to only allowed files
        allowed_files = [f for f in changed_files if self.manager.is_path_allowed(f)]

        if not allowed_files:
            print("[GITHUB_UPDATER] No deployable changes")
            self.last_commit_sha = latest_sha
            self._save_state()
            return False, latest_sha, []

        print(f"[GITHUB_UPDATER] Found {len(allowed_files)} files to update")
        return True, latest_sha, allowed_files

    def deploy_updates(self, files_to_update):
        """
        Download and deploy updated files.

        Args:
            files_to_update: List of file paths to update

        Returns:
            Tuple of (success, message)
        """
        if not files_to_update:
            return True, "No files to update"

        # Create backup first
        print("[GITHUB_UPDATER] Creating backup...")
        backup_path = self.manager.create_backup("github")

        if not backup_path:
            return False, "Backup failed - aborting update"

        print(f"[GITHUB_UPDATER] Backup created: {backup_path.name}")

        # Clear staging
        self.manager.clear_staging()

        # Download and stage each file
        staged_count = 0
        for file_path in files_to_update:
            print(f"[GITHUB_UPDATER] Downloading: {file_path}")
            content = self._download_raw_file(file_path)

            if content is not None:
                if self.manager.stage_file(file_path, content):
                    staged_count += 1
                else:
                    print(f"[GITHUB_UPDATER] Failed to stage: {file_path}")
            else:
                print(f"[GITHUB_UPDATER] Failed to download: {file_path}")

        if staged_count == 0:
            return False, "No files were staged successfully"

        # Deploy staged files
        print("[GITHUB_UPDATER] Deploying staged files...")
        success, deployed_count, error = self.manager.deploy_staged_files()

        if success:
            return True, f"Deployed {deployed_count} files successfully"
        else:
            # Attempt rollback
            print("[GITHUB_UPDATER] Deployment failed, rolling back...")
            self.manager.rollback()
            return False, f"Deployment failed: {error}"

    def run_once(self):
        """
        Check for updates and deploy if available.

        Returns:
            Tuple of (updated, message)
        """
        has_updates, latest_sha, changed_files = self.check_for_updates()

        if not has_updates:
            return False, "No updates available"

        success, message = self.deploy_updates(changed_files)

        if success:
            self.last_commit_sha = latest_sha
            self._save_state()

        return success, message

    def run_forever(self):
        """Run the updater in a continuous loop."""
        print(f"[GITHUB_UPDATER] Starting update loop (interval: {self.POLL_INTERVAL}s)")
        print(f"[GITHUB_UPDATER] Watching: {self.REPO_OWNER}/{self.REPO_NAME}")
        print("[GITHUB_UPDATER] Press Ctrl+C to stop")

        while True:
            try:
                updated, message = self.run_once()

                if updated:
                    print(f"[GITHUB_UPDATER] UPDATE COMPLETE: {message}")
                else:
                    print(f"[GITHUB_UPDATER] {message}")

            except KeyboardInterrupt:
                print("\n[GITHUB_UPDATER] Stopped by user")
                break

            except Exception as e:
                print(f"[GITHUB_UPDATER] Error: {e}")

            time.sleep(self.POLL_INTERVAL)


# Quick test when run directly
if __name__ == "__main__":
    print("[GITHUB_UPDATER] Self-test starting...")

    # Use current directory's parent as project root
    test_root = Path(__file__).parent.parent
    updater = GitHubUpdater(test_root)

    print(f"[GITHUB_UPDATER] Project root: {updater.project_root}")
    print(f"[GITHUB_UPDATER] Token loaded: {'Yes' if updater.token else 'No'}")

    # Test API connection
    print("\n[GITHUB_UPDATER] Testing GitHub API connection...")
    latest = updater.get_latest_commit()

    if latest:
        print(f"[GITHUB_UPDATER] PASS: Latest commit = {latest[:7]}")
    else:
        print("[GITHUB_UPDATER] FAIL: Could not connect to GitHub")

    print("\n[GITHUB_UPDATER] Self-test complete.")