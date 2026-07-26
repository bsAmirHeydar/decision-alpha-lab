# FlagCounting Phoenix — Offline License Runbook

This project uses a hardened offline runtime license for EX5 distribution.

The license is issued with:

```text
tools/flag_counting/offline_license_keygen.py
```

The tool is private and must never be sent to recipients.

## Issuer archive layout

Every generated license is now archived automatically under:

```text
licenses/
```

Example:

```text
licenses/
  README_LICENSE_ISSUER.md
  user0001-Amir-Hosein-Heydar/
    user0001-Amir-Hosein-Heydar_recipient_inputs.txt
    user0001-Amir-Hosein-Heydar_issuer_audit.json
    user0001-Amir-Hosein-Heydar_full_record.txt
  issued_licenses_index.csv
```

Only `README_LICENSE_ISSUER.md` and `licenses/.gitignore` should be committed. Generated user folders are private local issuer records.

## Required issuer fields

The keygen now requires recipient identity fields:

```text
--first-name
--last-name
```

It also supports:

```text
--middle-name
--user-code
--out-root
--overwrite
--no-save
```

The default user code auto-increments from the existing folders under `licenses/`.

## Secure account + server-bound license

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

This creates a folder like:

```text
licenses/user0001-Amir-Hosein-Heydar/
```

The file to send to the recipient is:

```text
user0001-Amir-Hosein-Heydar_recipient_inputs.txt
```

## Recipient values

The recipient pastes the six neutral input values into MT5:

```text
InpPhaseModelProfile
InpRenderMemo
InpNodeModelSeed
InpBoundaryModelSeed
InpValidationModelSeed
InpReleaseModelSeed
```

## Private files

Do not send these to the recipient:

```text
*_issuer_audit.json
*_full_record.txt
issued_licenses_index.csv
tools/flag_counting/offline_license_keygen.py
```
