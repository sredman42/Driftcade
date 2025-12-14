"""
Driftcade v1 - Update Runner
Main controller: runs GitHub updater as primary, email as fallback.
This is the script you run at startup.
"""

import os
import sys
import time
import logging
from pathlib import Path
from datetime import datetime

# Add tools directory to path for imports
TOOLS_DIR = Path(__file__).parent
PROJECT_ROOT = TOOLS_DIR.parent
sys.path.insert(0, str(TOOLS_DIR))

from github_updater import GitHubUpdater
from email_updater import EmailUpdater


class UpdateRunner:
    """Coordinates GitHub (primary) and Email (fallback) updaters."""

    # How often to check GitHub (seconds)
    POLL_INTERVAL = 60

    # How many GitHub failures before trying email fallback
    GITHUB_FAIL_THRESHOLD = 3

    # How often to check email fallback (seconds) - less frequent than GitHub
    EMAIL_CHECK_INTERVAL = 300  # 5 minutes

    def __init__(self, project_root=None):
        """
        Initialize UpdateRunner.

        Args:
            project_root: Path to Driftcade_v1 folder. Auto-detected if not provided.
        """
        self.project_root = Path(project_root) if project_root else PROJECT_ROOT

        # Setup logging
        self._setup_logging()

        # Initialize updaters
        self.github_updater = GitHubUpdater(self.project_root)
        self.email_updater = EmailUpdater(self.project_root)

        # Failure tracking
        self.github_fail_count = 0
        self.last_email_check = 0

    def _setup_logging(self):
        """Configure logging to file and console."""
        log_dir = self.project_root / "logs"
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / "updater.log"

        # Create logger
        self.logger = logging.getLogger("Driftcade.Updater")
        self.logger.setLevel(logging.INFO)

        # Clear existing handlers
        self.logger.handlers = []

        # File handler (detailed)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        file_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_format)

        # Console handler (concise)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter('[%(levelname)s] %(message)s')
        console_handler.setFormatter(console_format)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def log(self, level, message):
        """Log a message."""
        if level == "info":
            self.logger.info(message)
        elif level == "error":
            self.logger.error(message)
        elif level == "warning":
            self.logger.warning(message)
        else:
            self.logger.debug(message)

    def check_github(self):
        """
        Check GitHub for updates.

        Returns:
            Tuple of (success, had_update, message)
            - success: True if GitHub check completed (even with no updates)
            - had_update: True if an update was deployed
            - message: Description of what happened
        """
        try:
            has_updates, latest_sha, changed_files = self.github_updater.check_for_updates()

            if not has_updates:
                # No updates, but check succeeded
                return True, False, "GitHub: No updates available"

            # Deploy updates
            success, message = self.github_updater.deploy_updates(changed_files)

            if success:
                # Update state
                self.github_updater.last_commit_sha = latest_sha
                self.github_updater._save_state()
                return True, True, f"GitHub: {message}"
            else:
                return False, False, f"GitHub deploy failed: {message}"

        except Exception as e:
            return False, False, f"GitHub error: {e}"

    def check_email(self):
        """
        Check email for updates (fallback).

        Returns:
            Tuple of (success, had_update, message)
        """
        try:
            updated, message = self.email_updater.run_once()
            return True, updated, f"Email: {message}"

        except Exception as e:
            return False, False, f"Email error: {e}"

    def run_once(self):
        """
        Run a single update check cycle.

        Returns:
            Tuple of (had_update, message)
        """
        # Try GitHub first
        self.log("info", "Checking GitHub for updates...")
        success, had_update, message = self.check_github()

        if success:
            # Reset failure counter on success
            self.github_fail_count = 0

            if had_update:
                self.log("info", f"UPDATE DEPLOYED: {message}")
            else:
                self.log("info", message)

            return had_update, message

        else:
            # GitHub failed
            self.github_fail_count += 1
            self.log("warning", f"{message} (failure {self.github_fail_count}/{self.GITHUB_FAIL_THRESHOLD})")

            # Check if we should try email fallback
            if self.github_fail_count >= self.GITHUB_FAIL_THRESHOLD:
                current_time = time.time()

                if current_time - self.last_email_check >= self.EMAIL_CHECK_INTERVAL:
                    self.log("info", "GitHub unavailable, trying email fallback...")
                    self.last_email_check = current_time

                    success, had_update, message = self.check_email()

                    if had_update:
                        self.log("info", f"UPDATE DEPLOYED: {message}")
                        return True, message
                    else:
                        self.log("info", message)

            return False, message

    def run_forever(self):
        """Run the updater in a continuous loop."""
        self.log("info", "=" * 50)
        self.log("info", "Driftcade Update Runner starting")
        self.log("info", f"Project root: {self.project_root}")
        self.log("info", f"Poll interval: {self.POLL_INTERVAL} seconds")
        self.log("info", f"GitHub fail threshold: {self.GITHUB_FAIL_THRESHOLD}")
        self.log("info", "=" * 50)

        print("\nPress Ctrl+C to stop\n")

        while True:
            try:
                self.run_once()

            except KeyboardInterrupt:
                self.log("info", "Stopped by user")
                print("\nUpdater stopped.")
                break

            except Exception as e:
                self.log("error", f"Unexpected error: {e}")

            time.sleep(self.POLL_INTERVAL)

    def run_single_check(self):
        """Run a single check and exit (useful for testing)."""
        self.log("info", "Running single update check...")
        had_update, message = self.run_once()
        self.log("info", f"Result: {message}")
        return had_update


# Entry point
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Driftcade Update Runner")
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run a single check and exit"
    )
    parser.add_argument(
        "--root",
        type=str,
        default=None,
        help="Project root path (auto-detected if not provided)"
    )

    args = parser.parse_args()

    runner = UpdateRunner(args.root)

    if args.once:
        runner.run_single_check()
    else:
        runner.run_forever()