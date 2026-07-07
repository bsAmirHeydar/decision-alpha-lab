# Install — Hook Sequence Partition Fix Patch

Place the zip at the project root and run in PowerShell:

```powershell
Expand-Archive -Path .\alpha_lab_hook_sequence_partition_fix_patch.zip -DestinationPath . -Force
Remove-Item .\alpha_lab_hook_sequence_partition_fix_patch.zip
```

Then compile:

```text
mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5
```

Recommended temporary debug inputs:

```text
InpHookPhase02PrintSummary = true
InpHookPhase02PrintSamples = true
InpHookPhase02ShowHookSequenceIdsInLabels = true
```

Expected chart effect:

```text
A node that appeared inside an earlier Hook sequence should not reappear as node 1 of another overlapping sequence.
Sequences should extend to 3/4 when valid continuation nodes exist instead of repeatedly ending at 2.
```
