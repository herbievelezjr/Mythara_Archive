"""
Mythara Engine - License Key Management
Generates, validates, and manages enterprise license keys.

Copyright © 2025 Herbert Velez Jr. All rights reserved.
Proprietary and Confidential.
"""

import hashlib
import secrets
import json
from datetime import datetime
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


def generate_license_key(
    edition: str,  # "ENT" (Enterprise) or "SOV" (Sovereign)
    company_name: str,
    email: str,
    expires_at: Optional[datetime] = None,
) -> str:
    """
    Generate cryptographically secure license key.

    Format: MYTHARA-{EDITION}-{COMPANY_HASH}-{RANDOM}-{CHECKSUM}
    Example: MYTHARA-ENT-A7F3D-8K2P9-X4M1

    Args:
        edition: "ENT" for Enterprise, "SOV" for Sovereign
        company_name: Customer company name
        email: Customer primary email
        expires_at: Optional expiration date (None = perpetual)

    Returns:
        License key string
    """
    # Normalize edition
    edition = edition.upper()
    if edition not in ["ENT", "SOV"]:
        raise ValueError(f"Invalid edition: {edition}. Must be ENT or SOV.")

    # Hash company identifier (first 5 chars of SHA256)
    company_hash = (
        hashlib.sha256(
            f"{company_name.lower().strip()}:{email.lower().strip()}".encode()
        )
        .hexdigest()[:5]
        .upper()
    )

    # Random component (6 hex chars = 24 bits entropy)
    random_part = secrets.token_hex(3).upper()

    # Checksum to prevent tampering (first 4 chars of SHA256)
    checksum_input = f"{edition}{company_hash}{random_part}"
    checksum = hashlib.sha256(checksum_input.encode()).hexdigest()[:4].upper()

    key = f"MYTHARA-{edition}-{company_hash}-{random_part}-{checksum}"

    logger.info(f"Generated license key for {company_name} ({edition})")
    return key


def validate_license_key(key: str) -> Dict[str, Any]:
    """
    Validate license key format and checksum.

    Args:
        key: License key string (e.g., MYTHARA-ENT-A7F3D-8K2P9-X4M1)

    Returns:
        Dict with validation result:
        {
            "valid": bool,
            "edition": str,  # "Enterprise" or "Sovereign"
            "company_hash": str,
            "error": str  # Only present if invalid
        }
    """
    try:
        # Split and verify structure
        parts = key.strip().upper().split("-")
        if len(parts) != 5:
            return {
                "valid": False,
                "error": f"Invalid format: expected 5 parts, got {len(parts)}",
            }

        prefix, edition, company_hash, random_part, checksum = parts

        if prefix != "MYTHARA":
            return {"valid": False, "error": f"Invalid prefix: {prefix}"}

        if edition not in ["ENT", "SOV"]:
            return {"valid": False, "error": f"Invalid edition: {edition}"}

        # Verify checksum
        checksum_input = f"{edition}{company_hash}{random_part}"
        expected_checksum = (
            hashlib.sha256(checksum_input.encode()).hexdigest()[:4].upper()
        )

        if checksum != expected_checksum:
            return {
                "valid": False,
                "error": f"Invalid checksum: expected {expected_checksum}, got {checksum}",
            }

        # Valid license key
        edition_name = "Enterprise" if edition == "ENT" else "Sovereign"
        logger.info(f"Validated {edition_name} license key: {company_hash}")

        return {
            "valid": True,
            "edition": edition_name,
            "edition_code": edition,
            "company_hash": company_hash,
        }

    except Exception as e:
        logger.error(f"License validation error: {e}")
        return {"valid": False, "error": str(e)}


def save_license_to_file(
    key: str, metadata: Dict[str, Any], path: str = "/etc/mythara/license.json"
) -> Dict[str, Any]:
    """
    Save license key with metadata to file (called after payment confirmation).

    Args:
        key: Valid license key
        metadata: Dict containing company_name, email, edition, payment_id, etc.
        path: Filesystem path to save license file

    Returns:
        License data dict that was saved
    """
    license_data = {
        "license_key": key,
        "issued_at": datetime.utcnow().isoformat() + "Z",
        "company": metadata.get("company_name"),
        "email": metadata.get("email"),
        "edition": metadata.get("edition"),
        "expires_at": metadata.get("expires_at"),  # None for perpetual
        "payment_id": metadata.get("stripe_payment_id"),
        "payment_amount_usd": metadata.get("payment_amount_usd"),
        "notes": metadata.get("notes", ""),
    }

    try:
        # Ensure directory exists
        import os

        os.makedirs(os.path.dirname(path), exist_ok=True)

        # Write license file
        with open(path, "w") as f:
            json.dump(license_data, f, indent=2)

        logger.info(f"Saved license to {path} for {license_data['company']}")
        return license_data

    except Exception as e:
        logger.error(f"Failed to save license to {path}: {e}")
        raise


def load_license_from_file(
    path: str = "/etc/mythara/license.json",
) -> Optional[Dict[str, Any]]:
    """
    Load license data from file.

    Args:
        path: Filesystem path to license file

    Returns:
        License data dict or None if file doesn't exist
    """
    try:
        with open(path, "r") as f:
            license_data = json.load(f)

        # Validate key from file
        validation = validate_license_key(license_data["license_key"])
        if not validation["valid"]:
            logger.error(f"Invalid license key in {path}: {validation['error']}")
            return None

        logger.info(f"Loaded {validation['edition']} license from {path}")
        return license_data

    except FileNotFoundError:
        logger.debug(f"License file not found: {path}")
        return None
    except Exception as e:
        logger.error(f"Failed to load license from {path}: {e}")
        return None


def is_license_expired(license_data: Dict[str, Any]) -> bool:
    """
    Check if license has expired.

    Args:
        license_data: Dict from load_license_from_file()

    Returns:
        True if expired, False if still valid or perpetual
    """
    expires_at_str = license_data.get("expires_at")
    if not expires_at_str:
        # Perpetual license
        return False

    try:
        expires_at = datetime.fromisoformat(expires_at_str.replace("Z", "+00:00"))
        now = datetime.utcnow()

        if now > expires_at:
            logger.warning(f"License expired at {expires_at_str}")
            return True

        return False

    except Exception as e:
        logger.error(f"Failed to parse expiration date: {e}")
        return True  # Fail closed


# Example usage for testing
if __name__ == "__main__":
    # Generate a test license
    test_key = generate_license_key(
        edition="ENT", company_name="Acme Corporation", email="procurement@acme.com"
    )
    print(f"Generated key: {test_key}")

    # Validate it
    result = validate_license_key(test_key)
    print(f"Validation: {result}")

    # Test invalid key
    invalid = validate_license_key("MYTHARA-ENT-AAAAA-BBBBB-CCCC")
    print(f"Invalid key test: {invalid}")
