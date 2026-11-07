# PythonUdpBlaster

A universal, standardised command-line tester for the headset's UDP control
ports — the lab-side counterpart of the "Network communication protocol" in
`../README.md`. One plain-ASCII datagram per call, and optionally the single
reply the protocol promises. Pure Python standard library: nothing to install.

## Layout

```
PythonUdpBlaster/
  __main__.py   CLI entry point (runs blaster.main)
  blaster.py    parse_args / blaster() / main() -- importable if you script a test suite
  README.md     this file
```

## Usage

```
python3 PythonUdpBlaster <headset IP> <UDP port> <payload> [expect-reply] [-t SECONDS]
```

| Argument | Meaning |
| -------- | ------- |
| `<headset IP>` | e.g. `192.168.42.125` (headset, while the app runs) |
| `<UDP port>` | `40000` eye-tracker thresholds · `40001` gaze (averaged read / offset set) · `40002` passthrough · `40003` hand rendering · `40004` scotoma distance · `40005` IPD |
| `<payload>` | plain ASCII, one datagram; **quote it** in the shell if it contains spaces (e.g. `"0, 0"`) |
| `[expect-reply]` | `0` (default) fire-and-forget · `1` wait for the headset's reply and print it to stdout |
| `[-t SECONDS]` | reply wait timeout, default `1` (LAN round-trips are near-instant) |

### Examples

```bash
python3 PythonUdpBlaster 192.168.42.125 40002 "0" 0              # passthrough off (write-only port)
python3 PythonUdpBlaster 192.168.42.125 40000 "?" 1              # query thresholds -> prints e.g. 0.9000,0.5000
python3 PythonUdpBlaster 192.168.42.125 40000 "0.95,0.43" 0      # set EyeTrackingConfidence=0.95, EyesAreClosed=0.43
python3 PythonUdpBlaster 192.168.42.125 40003 "1" 0              # hand rendering on
python3 PythonUdpBlaster 192.168.42.125 40001 "?" 1              # query averaged gaze -> prints e.g. 2.3450,-1.0025
python3 PythonUdpBlaster 192.168.42.125 40001 "0.5,-0.1" 0       # set the gaze offset (write side; no reply)
python3 PythonUdpBlaster 192.168.42.125 40005 "?" 1              # query IPD (metres) -> prints e.g. 0.063, while worn
```

## Contract

- **stdout**: the headset's reply, printed verbatim, if any — nothing else. This keeps
  `python3 PythonUdpBlaster ... | ...` and `$(python3 PythonUdpBlaster ...)` clean.
- **stderr**: errors, timeouts, and a hint — write-only port, not implemented yet, or
  (for an implemented port) a real failure to investigate.
- **Exit codes** (the standardised test signal):

| exit | meaning |
| ---- | ------- |
| `0` | sent; a reply was not expected, or the expected reply arrived |
| `1` | sent, but the expected reply timed out — treat as a failed test |
| `2` | could not send at all (bad arguments, unresolvable address, socket error) |

## Notes

- The tool lives in the repo root, **outside `Assets/`**, so the Unity editor never
  imports it — no `.meta` files, no scene impact. (Unity only imports from `Assets/`,
  `Packages/` and `ProjectSettings/`.)
- Reply capture works because the tool reserves its source port *before* sending; the
  headset replies to the sender's `IP:port`, and only this socket owns that port.
- Current headset-side state (as of writing): `40000` and `40001` are implemented
  (`ExternalEyeTrackerControl.cs`, `ExternalEyeTrackerAzimuthElevationAdjuster.cs`) —
  `?` gets back the current values (on `40001`: the average of the last 10 gaze samples),
  and a numeric packet sets them. A `?` timeout on these is a **real failure** (check the
  headset logs for the matching `[External...]` tag, and note the reply must leave the
  headset from its listening socket — source port = control port; see `../AGENTS.md`).
  `40002`, `40003` and `40004` are implemented and write-only (they **never** reply —
  always use `expect-reply 0` on them). `40005` is implemented and query-only, but the
  headset reports an IPD only while it is being worn — a `?` timeout with the headset off
  is the *expected* state, not a failure.
- Windows: use `python` if `python3` is not on your PATH (the tool is identical either way).
