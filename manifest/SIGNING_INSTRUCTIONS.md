# PGP Signing Instructions — Mythara Archive

**Date**: November 2, 2025  
**Purpose**: Sign critical manifest files for escrow and licensing verification  
**Key**: `571F FB4C CCFA DCF A44A  63F6 D968 C2D5 DBE2 486C`

---

## Prerequisites

- GPG installed (`gpg --version`)
- Private key for `Mythara.Engine@yahoo.com` accessible
- Passphrase ready

---

## Step 1: Sign RELEASE_MANIFEST.json

Create a detached signature for the release manifest:

```powershell
gpg --armor --detach-sign --output manifest\RELEASE_MANIFEST.json.asc manifest\RELEASE_MANIFEST.json
```

**Expected output**: `manifest\RELEASE_MANIFEST.json.asc`

---

## Step 2: Sign checksums.sha256

Create a detached signature for the checksums file:

```powershell
gpg --armor --detach-sign --output manifest\checksums.sha256.asc manifest\checksums.sha256
```

**Expected output**: `manifest\checksums.sha256.asc`

---

## Step 3: Sign forensic_manifest.json

Create a detached signature for the forensic manifest:

```powershell
gpg --armor --detach-sign --output forensic_manifest.json.asc forensic_manifest.json
```

**Expected output**: `forensic_manifest.json.asc` (already exists, re-sign if needed)

---

## Step 4: Verify Signatures

Verify all signatures are valid:

```powershell
# Verify RELEASE_MANIFEST signature
gpg --verify manifest\RELEASE_MANIFEST.json.asc manifest\RELEASE_MANIFEST.json

# Verify checksums signature
gpg --verify manifest\checksums.sha256.asc manifest\checksums.sha256

# Verify forensic manifest signature
gpg --verify forensic_manifest.json.asc forensic_manifest.json
```

**Expected output**: `Good signature from "Mythara Engine <Mythara.Engine@yahoo.com>"`

---

## Step 5: Update Manifest with Signature Hash

After creating `checksums.sha256.asc`, calculate its hash and update RELEASE_MANIFEST.json:

```powershell
$hash = (Get-FileHash -Algorithm SHA256 'manifest\checksums.sha256.asc').Hash.ToLower()
Write-Output "checksums.sha256.asc SHA256: $hash"
```

Then update the entry in `manifest/RELEASE_MANIFEST.json`:

```json
{
  "filename": "manifest/checksums.sha256.asc",
  "classification": "PUBLIC",
  "sha256": "<INSERT_HASH_HERE>"
}
```

---

## Step 6: Recalculate RELEASE_MANIFEST.json Self-Hash

After all updates, recalculate the manifest's own hash:

```powershell
$hash = (Get-FileHash -Algorithm SHA256 'manifest\RELEASE_MANIFEST.json').Hash.ToLower()
Write-Output "RELEASE_MANIFEST.json final SHA256: $hash"
```

Update the first entry in the manifest with this value.

---

## Step 7: Export Public Key (if needed)

If public key needs to be regenerated or verified:

```powershell
gpg --armor --export Mythara.Engine@yahoo.com > forensic_public_key_NEW.asc
```

Compare with existing `forensic_public_key.asc` to ensure consistency.

---

## Verification Commands for Third Parties

Include these commands in `README.md` for licensees/escrow agents:

```bash
# Import public key
gpg --import forensic_public_key.asc

# Verify manifest signature
gpg --verify manifest/RELEASE_MANIFEST.json.asc manifest/RELEASE_MANIFEST.json

# Verify checksums
gpg --verify manifest/checksums.sha256.asc manifest/checksums.sha256
sha256sum -c manifest/checksums.sha256
```

---

## Current Status

✅ RELEASE_MANIFEST.json — hashes updated, ready for signing  
✅ checksums.sha256 — canonical, ready for signing  
✅ forensic_public_key.asc — exported and included  
⏳ Signatures pending (create .asc files using commands above)

---

## Security Notes

- Sign on air-gapped machine if possible
- Verify fingerprint before signing: `gpg --fingerprint Mythara.Engine@yahoo.com`
- Store private key backup in secure location
- Passphrase should be strong and recorded in password manager

---

**After signing, archive is cryptographically sealed and ready for escrow/licensing.**
