"""
Driftcade v1 - Email Updater
Fallback update method: checks email for emergency update packages.
Uses UpdateManager for safe deployment.

SECURITY: Only processes emails from whitelisted senders with correct subject prefix.
"""

import os
import re
import json
import email
import imaplib
import hashlib
import zipfile
import tempfile
from pathlib import Path
from datetime import datetime

# Import our update manager
from update_manager import UpdateManager


class EmailUpdater:
    """Checks email for update packages and deploys them safely."""

    # Required subject prefix (emails without this are ignored)
    SUBJECT_PREFIX = "[DRIFTCADE-UPDATE]"

    # Email server settings (Gmail IMAP)
    IMAP_SERVER = "imap.gmail.com"
    IMAP_PORT = 993

    def __init__(self, project_root, email_address=None, email_password=None, allowed_senders=None):
        """
        Initialize EmailUpdater.

        Args:
            project_root: Path to Driftcade_v1 folder
            email_address: Email to check (loaded from .env if not provided)
            email_password: App password (loaded from .env if not provided)
            allowed_senders: List of allowed sender emails (loaded from .env if not provided)
        """
        self.project_root = Path(project_root)
        self.manager = UpdateManager(project_root)

        # Load credentials from .env if not provided
        env_config = self._load_env_config()

        self.email_address = email_address or env_config.get("EMAIL_ADDRESS")
        self.email_password = email_password or env_config.get("EMAIL_PASSWORD")

        # Allowed senders (comma-separated in .env)
        if allowed_senders:
            self.allowed_senders = allowed_senders
        else:
            senders_str = env_config.get("EMAIL_ALLOWED_SENDERS", "")
            self.allowed_senders = [s.strip().lower() for s in senders_str.split(",") if s.strip()]

        # State tracking
        self.state_file = self.project_root / "_update_staging" / "email_state.json"
        self.processed_ids = self._load_processed_ids()

    def _load_env_config(self):
        """Load email configuration from .env file."""
        config = {}
        env_path = self.project_root / ".env"

        if not env_path.exists():
            print("[EMAIL_UPDATER] Warning: .env file not found")
            return config

        try:
            with open(env_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if "=" in line and not line.startswith("#"):
                        key, value = line.split("=", 1)
                        config[key.strip()] = value.strip()
        except Exception as e:
            print(f"[EMAIL_UPDATER] Error reading .env: {e}")

        return config

    def _load_processed_ids(self):
        """Load list of already-processed email IDs."""
        try:
            if self.state_file.exists():
                with open(self.state_file, "r") as f:
                    state = json.load(f)
                    return set(state.get("processed_ids", []))
        except Exception as e:
            print(f"[EMAIL_UPDATER] Could not load state: {e}")

        return set()

    def _save_processed_ids(self):
        """Save processed email IDs to state file."""
        try:
            self.state_file.parent.mkdir(exist_ok=True)

            # Keep only last 100 IDs to prevent file from growing forever
            recent_ids = list(self.processed_ids)[-100:]

            with open(self.state_file, "w") as f:
                json.dump({"processed_ids": recent_ids}, f)
        except Exception as e:
            print(f"[EMAIL_UPDATER] Could not save state: {e}")

    def _is_sender_allowed(self, sender_email):
        """Check if sender is in the whitelist."""
        if not self.allowed_senders:
            print("[EMAIL_UPDATER] Warning: No allowed senders configured")
            return False

        # Extract email from "Name <email@example.com>" format
        match = re.search(r'<([^>]+)>', sender_email)
        if match:
            sender_email = match.group(1)

        return sender_email.lower() in self.allowed_senders

    def _is_subject_valid(self, subject):
        """Check if subject has the required prefix."""
        return subject.strip().startswith(self.SUBJECT_PREFIX)

    def connect(self):
        """
        Connect to email server.

        Returns:
            IMAP connection object, or None on failure
        """
        if not self.email_address or not self.email_password:
            print("[EMAIL_UPDATER] Email credentials not configured")
            return None

        try:
            print(f"[EMAIL_UPDATER] Connecting to {self.IMAP_SERVER}...")
            connection = imaplib.IMAP4_SSL(self.IMAP_SERVER, self.IMAP_PORT)
            connection.login(self.email_address, self.email_password)
            print("[EMAIL_UPDATER] Connected successfully")
            return connection

        except imaplib.IMAP4.error as e:
            print(f"[EMAIL_UPDATER] Login failed: {e}")
            return None

        except Exception as e:
            print(f"[EMAIL_UPDATER] Connection failed: {e}")
            return None

    def check_for_updates(self, connection):
        """
        Check inbox for valid update emails.

        Args:
            connection: Active IMAP connection

        Returns:
            List of (email_id, subject, sender) tuples for valid update emails
        """
        valid_updates = []

        try:
            connection.select("INBOX")

            # Search for unread emails
            status, messages = connection.search(None, "UNSEEN")

            if status != "OK":
                print("[EMAIL_UPDATER] Could not search inbox")
                return []

            email_ids = messages[0].split()
            print(f"[EMAIL_UPDATER] Found {len(email_ids)} unread emails")

            for email_id in email_ids:
                email_id_str = email_id.decode()

                # Skip already processed
                if email_id_str in self.processed_ids:
                    continue

                # Fetch email headers
                status, msg_data = connection.fetch(email_id, "(BODY.PEEK[HEADER])")

                if status != "OK":
                    continue

                # Parse headers
                header_data = msg_data[0][1]
                msg = email.message_from_bytes(header_data)

                subject = msg.get("Subject", "")
                sender = msg.get("From", "")

                # Validate subject
                if not self._is_subject_valid(subject):
                    continue

                # Validate sender
                if not self._is_sender_allowed(sender):
                    print(f"[EMAIL_UPDATER] BLOCKED: Unauthorized sender: {sender}")
                    continue

                print(f"[EMAIL_UPDATER] Valid update email: {subject}")
                valid_updates.append((email_id_str, subject, sender))

        except Exception as e:
            print(f"[EMAIL_UPDATER] Error checking emails: {e}")

        return valid_updates

    def process_update_email(self, connection, email_id):
        """
        Process a single update email.

        Args:
            connection: Active IMAP connection
            email_id: Email ID to process

        Returns:
            Tuple of (success, message)
        """
        try:
            # Fetch full email
            status, msg_data = connection.fetch(email_id.encode(), "(RFC822)")

            if status != "OK":
                return False, "Could not fetch email"

            msg = email.message_from_bytes(msg_data[0][1])

            # Find attachments
            zip_data = None
            checksum_data = None

            for part in msg.walk():
                filename = part.get_filename()

                if not filename:
                    continue

                if filename.endswith(".zip"):
                    zip_data = part.get_payload(decode=True)
                    print(f"[EMAIL_UPDATER] Found ZIP: {filename}")

                elif filename.endswith(".sha256") or filename.endswith(".checksum"):
                    checksum_data = part.get_payload(decode=True).decode().strip()
                    print(f"[EMAIL_UPDATER] Found checksum: {filename}")

            if not zip_data:
                return False, "No ZIP attachment found"

            if not checksum_data:
                return False, "No checksum file found - REQUIRED for security"

            # Verify checksum
            actual_checksum = hashlib.sha256(zip_data).hexdigest()
            expected_checksum = checksum_data.split()[0]  # Handle "hash  filename" format

            if actual_checksum.lower() != expected_checksum.lower():
                return False, f"Checksum mismatch! Expected {expected_checksum[:16]}... got {actual_checksum[:16]}..."

            print("[EMAIL_UPDATER] Checksum verified")

            # Extract and deploy
            return self._deploy_zip(zip_data)

        except Exception as e:
            return False, f"Error processing email: {e}"

    def _deploy_zip(self, zip_data):
        """
        Extract ZIP and deploy files.

        Args:
            zip_data: ZIP file as bytes

        Returns:
            Tuple of (success, message)
        """
        # Create backup first
        print("[EMAIL_UPDATER] Creating backup...")
        backup_path = self.manager.create_backup("email")

        if not backup_path:
            return False, "Backup failed - aborting update"

        print(f"[EMAIL_UPDATER] Backup created: {backup_path.name}")

        # Clear staging
        self.manager.clear_staging()

        # Extract ZIP to temp directory first
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)

                # Extract ZIP
                with zipfile.ZipFile(tempfile.SpooledTemporaryFile()) as zf:
                    # Write zip_data to temp file for extraction
                    import io
                    with zipfile.ZipFile(io.BytesIO(zip_data), 'r') as zf:
                        zf.extractall(temp_path)

                # Stage each extracted file
                staged_count = 0

                for file_path in temp_path.rglob("*"):
                    if file_path.is_file():
                        relative_path = file_path.relative_to(temp_path)

                        # Read file content
                        with open(file_path, "rb") as f:
                            content = f.read()

                        # Try to decode as text, fall back to bytes
                        try:
                            content = content.decode("utf-8")
                        except UnicodeDecodeError:
                            pass  # Keep as bytes

                        if self.manager.stage_file(str(relative_path), content):
                            staged_count += 1
                            print(f"[EMAIL_UPDATER] Staged: {relative_path}")
                        else:
                            print(f"[EMAIL_UPDATER] Skipped (protected): {relative_path}")

                if staged_count == 0:
                    return False, "No files were staged (all may be protected)"

                # Deploy staged files
                print("[EMAIL_UPDATER] Deploying staged files...")
                success, deployed_count, error = self.manager.deploy_staged_files()

                if success:
                    return True, f"Deployed {deployed_count} files from email"
                else:
                    # Attempt rollback
                    print("[EMAIL_UPDATER] Deployment failed, rolling back...")
                    self.manager.rollback()
                    return False, f"Deployment failed: {error}"

        except zipfile.BadZipFile:
            return False, "Invalid ZIP file"

        except Exception as e:
            return False, f"Extraction failed: {e}"

    def run_once(self):
        """
        Check for updates and process any valid ones.

        Returns:
            Tuple of (updated, message)
        """
        connection = self.connect()

        if not connection:
            return False, "Could not connect to email"

        try:
            valid_updates = self.check_for_updates(connection)

            if not valid_updates:
                return False, "No valid update emails"

            # Process first valid update only (safest approach)
            email_id, subject, sender = valid_updates[0]
            print(f"[EMAIL_UPDATER] Processing: {subject}")

            success, message = self.process_update_email(connection, email_id)

            # Mark as processed regardless of success (to avoid retry loops)
            self.processed_ids.add(email_id)
            self._save_processed_ids()

            # Mark email as read
            connection.store(email_id.encode(), "+FLAGS", "\\Seen")

            return success, message

        finally:
            connection.logout()


# Quick test when run directly
if __name__ == "__main__":
    print("[EMAIL_UPDATER] Self-test starting...")

    # Use current directory's parent as project root
    test_root = Path(__file__).parent.parent
    updater = EmailUpdater(test_root)

    print(f"[EMAIL_UPDATER] Project root: {updater.project_root}")
    print(f"[EMAIL_UPDATER] Email configured: {'Yes' if updater.email_address else 'No'}")
    print(f"[EMAIL_UPDATER] Password configured: {'Yes' if updater.email_password else 'No'}")
    print(f"[EMAIL_UPDATER] Allowed senders: {len(updater.allowed_senders)} configured")

    # Test subject validation
    test_subjects = [
        ("[DRIFTCADE-UPDATE] Emergency fix", True),
        ("[DRIFTCADE-UPDATE]", True),
        ("Re: [DRIFTCADE-UPDATE] Fix", False),
        ("Random spam", False),
    ]

    print("\n[EMAIL_UPDATER] Subject validation tests:")
    for subject, expected in test_subjects:
        result = updater._is_subject_valid(subject)
        status = "PASS" if result == expected else "FAIL"
        print(f"  {status}: '{subject}' -> valid={result}")

    print("\n[EMAIL_UPDATER] Self-test complete.")
    print("[EMAIL_UPDATER] Note: Email connection not tested (requires credentials)")