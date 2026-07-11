# Run Modes and Authority Matrix

The runtime defines stable modes before implementing their full behavior:

| Mode | Event | Snapshot | Candidate | Order Authority |
|---|---:|---:|---:|---:|
| Visual Anatomy | Yes | Optional | No | No |
| Anatomy Audit | Yes | Yes | No | No |
| Outcome Study | Yes | Yes | Later | No |
| Candidate Matrix | Yes | Yes | Later | No |
| Tester Execution | Yes | Yes | Later | Tester only later |
| Paper | Yes | Yes | Later | Virtual later |
| Live Disabled | Yes | Yes | Later | Explicitly false |
| Training Export | Yes | Yes | Later | No |
| ONNX Inference | Yes | Yes | Later | No until risk and execution phases |

Run mode does not grant authority by itself. Authority comes from the bound execution adapter and hard gates.
