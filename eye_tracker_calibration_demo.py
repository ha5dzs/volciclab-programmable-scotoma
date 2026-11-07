#!/usr/bin/env python3
"""
eye_tracker_calibration_demo.py — a throwaway, hard-coded demo of the eye-tracker
calibration loop described in README.md ("Scotoma and the calibration stimulus for eye
tracker calibration"), meant to be run from another computer in the lab, at the headset.

NOT a production tool: one headset, fixed target and payloads, no retries, no state. Its
job is to let a person demonstrate the whole loop live (and to smoke-test ports
40001/40004/40006/40007 at once), in the README's own order:

  [1] 40007  turn on the head-contingent calibration ring
         (az/el 0 / -10 deg, inner 6 / outer 10 deg, dark green)
  [2] 40004  set the shared depth of both annuli to 0.5 m
  [3] 40001  reset the previous gaze offset to (0, 0)
  [4]  (the human) ask the participant to fixate the ring and hold
  [5] 40006  (optional feedback) turn on the fovea-locked red 5 deg disc —
         with the gaze on target it sits inside the ring's 6 deg hole (bullseye)
  [6] 40001  read the gaze TWICE (the headset answers with a 10-sample moving
         average); the second read is the one used — fixation may still be settling
  [7] 40001  send back the correction: offset = target - measured
  [8] 40001  verify: read again — it should now sit on (0, -10)
  [9]      turn both annuli off (settings preserved) and verify with '?'

usage:  python3 eye_tracker_calibration_demo.py [headset_ip]
        (default 192.168.42.125, the lab headset; any IP the headset answers at)
exit:   0 completed loop
        1 a required query got no reply (app not running on the headset?)
        2 a gaze reply arrived but could not be parsed
"""

import socket
import sys
import time

DEFAULT_HEADSET = "192.168.42.125"
HEADSET = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_HEADSET   # the one knob of this demo

PORT_GAZE = 40001        # read/set the gaze offset; '?' answers the 10-sample average
PORT_DEPTH = 40004       # shared depth of both annuli, metres
PORT_SCOTOMA = 40006     # the gaze-contingent annulus (the scotoma)
PORT_CALIB = 40007       # the head-contingent annulus (the calibration ring)

TARGET = (0.0, -10.0)            # where the ring sits (az/el, degrees) — must match the payloads
TIMEOUT = 1.0                    # LAN round-trip is near-instant; 1 s is generous
SETTLE = 0.1                     # inter-packet settle for fire-and-forget sends (see fire())
WINDOW_FILL = 0.3                # >= 10 tracker frames (~111-139 ms) after any offset change,
                                 # so the 40001 average window refills under the new offset — and
                                 # it gives the fixation a moment to settle

RING_ON = "1,0,-10,6,10,#006400FF"
RING_OFF = "0,0,-10,6,10,#006400FF"
SCOTOMA_ON = "1,0,0,1,5,#FF0000FF"    # red disc OD 5 deg < ring hole ID 6 deg -> the bullseye
SCOTOMA_OFF = "0,0,0,1,5,#FF0000FF"


def send(port, payload, expect_reply):
    """One datagram out; one datagram back if expected.

    Same idiom as PythonUdpBlaster: reserve our own source port BEFORE sending
    (bind "", 0), because the headset replies to the sender's IP:port.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.settimeout(TIMEOUT)
        s.bind(("", 0))
        s.sendto(payload.encode("ascii"), (HEADSET, port))
        if not expect_reply:
            return None
        try:
            data, _ = s.recvfrom(4096)
        except socket.timeout:
            print(f"    (no reply within {TIMEOUT} s — is the app running on {HEADSET}?)",
                  file=sys.stderr)
            sys.exit(1)
        return data.decode("ascii").strip()
    finally:
        s.close()


def fire(port, payload):
    print(f"  -> {HEADSET}:{port}  '{payload}'")
    send(port, payload, expect_reply=False)
    # Settle before the NEXT packet: the headset applies received packets on its main
    # thread (once per frame), and each port holds only ONE pending packet — the last
    # one wins. A second packet on the SAME port that lands within the same frame
    # replaces the first, which is then silently dropped (so a back-to-back
    # "set, then ?" on one port can answer with the pre-set state — the OFF that never
    # "took"). Waiting well past one frame (~11 ms at 90 Hz) between packets gives each
    # time to be applied. Queries need no settle: their reply arrives after processing.
    time.sleep(SETTLE)


def query(port, payload="?"):
    print(f"  -> {HEADSET}:{port}  '{payload}'")
    reply = send(port, payload, expect_reply=True)
    print(f"  <- {reply}")
    return reply


def read_gaze():
    try:
        parts = query(PORT_GAZE).split(",")
        return float(parts[0]), float(parts[1])
    except (ValueError, IndexError):
        print("    (the gaze reply could not be parsed)", file=sys.stderr)
        sys.exit(2)


def expect_toggle_0(port, label):
    if not query(port).split(",")[0] == "0":
        print(f"    !! the {label} did not report itself turned off", file=sys.stderr)
        sys.exit(1)


print(f"== eye-tracker calibration demo — headset {HEADSET} ==")
print(f"target: az {TARGET[0]:.1f} deg, el {TARGET[1]:.1f} deg (the green ring)\n")

print("[1] turn on the head-contingent calibration ring; set the shared depth to 0.5 m")
fire(PORT_CALIB, RING_ON)
fire(PORT_DEPTH, "0.5")

print("\n[2] reset the previous gaze offset to (0, 0)")
fire(PORT_GAZE, "0,0")

print("\n[3] ask the participant to look at the green ring and hold fixation — no blinking.")
input("    press ENTER once they are steady ...\n")
time.sleep(WINDOW_FILL)

print("[4] (feedback) fovea-locked red 5 deg disc: with the gaze on target it sits inside the ring's 6 deg hole")
fire(PORT_SCOTOMA, SCOTOMA_ON)
time.sleep(WINDOW_FILL)

print("\n[5] read the gaze twice (the headset answers with a 10-sample moving average); the second read is used")
first = read_gaze()
print(f"    (first read {first[0]:.2f}, {first[1]:.2f} — the fixation may still be settling)")
time.sleep(0.2)
az, el = read_gaze()
print(f"    (second read {az:.2f}, {el:.2f} — used)")

offset_az = TARGET[0] - az
offset_el = TARGET[1] - el
print(f"\n[6] correction: offset = target - measured = ({TARGET[0]:.1f} - {az:.2f}, {TARGET[1]:.1f} - {el:.2f})")
fire(PORT_GAZE, f"{offset_az:.2f},{offset_el:.2f}")
print(f"    (sent '{offset_az:.2f},{offset_el:.2f}')")
time.sleep(WINDOW_FILL)

print("\n[7] verify: the gaze should now sit on the target")
v_az, v_el = read_gaze()
res_az, res_el = v_az - TARGET[0], v_el - TARGET[1]
print(f"    measured ({v_az:.2f}, {v_el:.2f}) vs target ({TARGET[0]:.1f}, {TARGET[1]:.1f})"
      f"  ->  residual ({res_az:+.2f} deg, {res_el:+.2f} deg)")
if max(abs(res_az), abs(res_el)) <= 1.0:
    print("    within ~1 deg — good for a worn headset. (The tracker is a character-animation\n"
          "    sensor, not a scientific instrument; re-run the loop if the experiment needs more.)")
else:
    print("    more than ~1 deg off — have them re-fixate and repeat from step [3].")

print("\n[8] done — turn both annuli off (settings are preserved) and verify with '?'")
fire(PORT_CALIB, RING_OFF)
fire(PORT_SCOTOMA, SCOTOMA_OFF)
expect_toggle_0(PORT_CALIB, "calibration ring")
expect_toggle_0(PORT_SCOTOMA, "scotoma")
print("\n== calibration loop complete ==")
