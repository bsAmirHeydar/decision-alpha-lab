# Offline License Lab Notes

The private issuer workflow is now archive-first.

Run the keygen from the repository root. It prints recipient inputs and writes local issuer records under `licenses/`.

Example:

```powershell
python tools/flag_counting/offline_license_keygen.py `
  --first-name Amir `
  --middle-name Hosein `
  --last-name Heydar `
  --account 12345678 `
  --server "Broker-Demo" `
  --expires 20261231
```

Generated folder:

```text
licenses/user0001-Amir-Hosein-Heydar/
```

Generated files:

```text
user0001-Amir-Hosein-Heydar_recipient_inputs.txt
user0001-Amir-Hosein-Heydar_issuer_audit.json
user0001-Amir-Hosein-Heydar_full_record.txt
```

The recipient receives only the recipient inputs file content. The other files remain private.
