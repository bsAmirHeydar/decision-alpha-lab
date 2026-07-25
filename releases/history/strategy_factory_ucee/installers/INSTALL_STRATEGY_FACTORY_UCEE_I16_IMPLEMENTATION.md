# Install UCE-I16 Patch

Apply the patch at repository root. Use `UCEE_I16_FILE_INDEX.txt` to stage only phase files. Run the phase tests, delivery validator, engineering policy, and local MetaEditor compilation before enabling any migrated runtime behavior.

## Mandatory local Windows gate

Compile the UCE-I16 diagnostic and three self-tests with MetaEditor. Archive compile logs and differential replay evidence. Until then, adapters remain shadow/differential only.
