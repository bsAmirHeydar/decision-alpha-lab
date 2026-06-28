# Offline License Issuer Folder

This folder is the private issuer-side archive for FlagCounting Phoenix offline licenses.

Keep this folder private. Do not ship it to recipients and do not commit generated user folders.

## What stays in git

Only these guide files should remain in the repository:

```text
licenses/README_LICENSE_ISSUER.md
licenses/.gitignore
```

## What is generated locally

Each license issuance creates one user folder next to this guide:

```text
licenses/
  user0001-Amir-Hosein-Heydar/
    user0001-Amir-Hosein-Heydar_recipient_inputs.txt
    user0001-Amir-Hosein-Heydar_issuer_audit.json
    user0001-Amir-Hosein-Heydar_full_record.txt
  issued_licenses_index.csv
```

The `.gitignore` in this folder ignores generated records by default.

## Create a license bound to account and broker server

Run from the repository root:

```powershell
python tools/flag_counting/offline_license_keygen.py `
  --first-name Amir `
  --middle-name Hosein `
  --last-name Heydar `
  --account 12345678 `
  --server "Broker-Demo" `
  --expires 20261231 `
  --passphrase "Your-Strong-Password-Here"
```

The tool prints the recipient inputs and also writes them under:

```text
licenses/user0001-Amir-Hosein-Heydar/
```

## Create a license without server binding

Use this only when the server name is unstable or the user legitimately needs multiple server names for the same account:

```powershell
python tools/flag_counting/offline_license_keygen.py `
  --first-name Amir `
  --middle-name Hosein `
  --last-name Heydar `
  --account 12345678 `
  --server-any `
  --expires 20261231 `
  --passphrase "Your-Strong-Password-Here"
```

## Force a user code

By default the tool finds the next available user number and creates `user0001`, `user0002`, and so on.

To force a specific code:

```powershell
python tools/flag_counting/offline_license_keygen.py `
  --user-code user0001 `
  --first-name Amir `
  --middle-name Hosein `
  --last-name Heydar `
  --account 12345678 `
  --server "Broker-Demo" `
  --expires 20261231 `
  --passphrase "Your-Strong-Password-Here"
```

## Files to send to the recipient

Send only the six values from:

```text
user0001-Amir-Hosein-Heydar_recipient_inputs.txt
```

These are the only values the user needs to paste into MT5 Inputs:

```text
InpPhaseModelProfile
InpRenderMemo
InpNodeModelSeed
InpBoundaryModelSeed
InpValidationModelSeed
InpReleaseModelSeed
```

## Files to keep private

Keep these private:

```text
*_issuer_audit.json
*_full_record.txt
issued_licenses_index.csv
tools/flag_counting/offline_license_keygen.py
```

## Overwrite an existing user folder

Use `--overwrite` only when you intentionally want to replace files for the same user code/name folder.

```powershell
python tools/flag_counting/offline_license_keygen.py `
  --overwrite `
  --user-code user0001 `
  --first-name Amir `
  --middle-name Hosein `
  --last-name Heydar `
  --account 12345678 `
  --server "Broker-Demo" `
  --expires 20261231
```
