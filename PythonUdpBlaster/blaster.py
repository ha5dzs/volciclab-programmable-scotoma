"""Core send/receive logic for the PythonUdpBlaster test tool.

Lab-side half of the "Network communication protocol" documented in
../README.md: it sends one plain-ASCII datagram to a UDP control port on the
headset, and optionally waits for the single reply the protocol promises.

Deliberately mirrors the C# side:
  - one functionality, one UDP port, one plain-ASCII datagram;
  - the headset replies (where it does) to the sender's IP:port, so we
    reserve our own source port *before* sending, and that is where we wait;
  - replies are printed verbatim, nothing else goes to stdout, so the tool
    composes cleanly in scripts.

Exit-code contract (so these tests are standardised and scriptable):
  0  sent successfully; a reply was not expected, or the expected reply arrived
  1  sent successfully, but the expected reply did not arrive in time
  2  could not send at all (bad arguments, unresolvable address, socket error)
"""

import socket
import sys

DEFAULT_TIMEOUT_SECONDS = 1.0  # LAN round-trip is near-instant; 1 s is generous
RECV_BUFFER_BYTES = 4096      # a reply is one short ASCII line today; stay generous
MAX_PAYLOAD_BYTES = 65507     # largest single UDP datagram IP-65535 - UDP-8 - IPv4-20

USAGE = """PythonUdpBlaster - universal tester for the headset's UDP control ports.

usage: PythonUdpBlaster <headset IP> <UDP port> <payload> [expect-reply] [-t SECONDS]

  <headset IP>     headset IP when it is running the app, e.g. 192.168.42.125
  <UDP port>       control port (see ../README.md, "Network communication protocol"):
                     40000  eye tracker thresholds:  '?' reads, 'conf,blink' sets
                     40001  gaze:  '?' reads the last-10-sample average, 'az,el' sets the offset
                     40002  passthrough:  '0' off, anything else on   (write-only)
                     40003  hand rendering: '0' off, anything else on (write-only)
                     40004  scotoma distance in metres: a single float  (write-only)
                     40005  IPD in metres:  '?' reads  (only valid while the headset is worn)
  <payload>        plain ASCII for ONE datagram; quote it in the shell
                   if it contains spaces, e.g. "0, 0"
  [expect-reply]   0 (default) fire-and-forget; 1 wait for the headset's reply
  [-t SECONDS]     reply wait timeout, default 1 s

stdout: the headset's reply, printed verbatim, if any (nothing else on stdout)
stderr: errors, timeouts and hints
exit:   0 = sent, and reply received if one was expected
        1 = sent, but the expected reply timed out
        2 = could not send (bad arguments, address, or socket error)

examples:
  python3 PythonUdpBlaster 192.168.42.125 40002 "0" 0            # passthrough off
  python3 PythonUdpBlaster 192.168.42.125 40000 "?" 1            # query thresholds -> e.g. 0.9000,0.5000
  python3 PythonUdpBlaster 192.168.42.125 40000 "0.95,0.43" 0    # set thresholds
  python3 PythonUdpBlaster 192.168.42.125 40003 "1" 0 -t 2       # hand rendering on, longer timeout
"""


def _parse_bool(value, name):
    lowered = value.strip().lower()
    if lowered in ("0", "off", "no", "false"):
        return False
    if lowered in ("1", "on", "yes", "true"):
        return True
    raise ValueError(f"{name} must be 0/1 (or off/on, no/yes), got {value!r}")


def parse_args(argv):
    """Parse the command line into blaster() kwargs.

    Raises ValueError with a human-readable message on any problem; main()
    turns that into a usage error and exit code 2.
    """
    timeout = DEFAULT_TIMEOUT_SECONDS
    timeout_seen = False
    rest = []
    i = 0
    while i < len(argv):
        tok = argv[i]
        if tok in ("-t", "--timeout"):
            if timeout_seen:
                raise ValueError("the timeout is given more than once")
            i += 1
            if i >= len(argv):
                raise ValueError("-t/--timeout expects a value in seconds")
            timeout = float(argv[i])
            timeout_seen = True
        elif tok.startswith("--timeout=") or tok.startswith("-t="):
            if timeout_seen:
                raise ValueError("the timeout is given more than once")
            timeout = float(tok.split("=", 1)[1])
            timeout_seen = True
        else:
            rest.append(tok)
        i += 1

    if not 0 < timeout < float("inf"):
        raise ValueError(f"the timeout must be a positive number of seconds, got {timeout!r}")
    if not 3 <= len(rest) <= 4:
        raise ValueError("expected 3 or 4 positional arguments: "
                         "<headset IP> <UDP port> <payload> [expect-reply]")

    if len(rest) == 4:
        ip, port, payload, expect = rest
        expect_reply = _parse_bool(expect, "expect-reply")
    else:
        ip, port, payload = rest
        expect_reply = False

    port = int(port)
    if not 1 <= port <= 65535:
        raise ValueError(f"the port must be 1..65535, got {port}")

    return {"ip": ip, "port": port, "payload": payload,
            "expect_reply": expect_reply, "timeout": timeout}


def blaster(ip, port, payload, expect_reply=False, timeout=DEFAULT_TIMEOUT_SECONDS):
    """Send one plain-ASCII datagram to ip:port, optionally wait for one reply.

    Returns (exit_code, reply_text); reply_text is None unless a reply arrived.
    Exit codes: 0 ok, 1 reply expected but not received, 2 could not send.
    """
    if len(payload.encode("utf-8")) > MAX_PAYLOAD_BYTES:
        raise ValueError("the payload is larger than a single UDP datagram (~64 KiB)")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.settimeout(timeout)
        # Reserve our own source port BEFORE sending: the headset replies to
        # the sender's IP:port, and only this socket owns that port, so this
        # is exactly where the reply is delivered to us.
        sock.bind(("", 0))
        sock.sendto(payload.encode("utf-8"), (ip, port))
        if not expect_reply:
            return 0, None
        try:
            data, _source = sock.recvfrom(RECV_BUFFER_BYTES)
        except socket.timeout:
            return 1, None
        return 0, data.decode("utf-8", errors="replace").rstrip("\r\n")
    finally:
        sock.close()


def main(argv):
    if any(flag in ("--help", "-h", "help") for flag in argv):
        print(USAGE)
        return 0

    try:
        args = parse_args(argv)
    except (ValueError, TypeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        print("", file=sys.stderr)
        print(USAGE, file=sys.stderr)
        return 2

    try:
        code, reply = blaster(**args)
    except (OSError, ValueError) as exc:
        print(f"error: could not send to {args['ip']}:{args['port']}: {exc}", file=sys.stderr)
        return 2

    if reply is not None:
        print(reply)

    if code == 1:
        print(f"timeout: sent {args['payload']!r} to {args['ip']}:{args['port']}, "
              f"no reply within {args['timeout']} s", file=sys.stderr)
        if args["port"] in (40002, 40003, 40004):
            print("hint: ports 40002/40003/40004 are write-only (see ../README.md); "
                  "pass 0 as expect-reply.", file=sys.stderr)
        elif args["port"] in (40000, 40001):
            print("hint: port " + str(args["port"]) + " IS implemented ("
                  "ExternalEyeTrackerControl.cs / ExternalEyeTrackerAzimuthElevationAdjuster.cs) "
                  "- a timeout is a real failure: check the headset logs for the matching "
                  "'[External...]' tag; note the reply must leave the headset from its "
                  "listening socket (source port = the control port; see ../AGENTS.md).", file=sys.stderr)
        elif args["port"] == 40005:
            print("hint: port 40005 IS implemented (ExternalInterpupillaryDistanceReporter.cs), "
                  "but the headset reports an IPD only while it is being worn - with the "
                  "headset off, a timeout is the expected state, not a failure.", file=sys.stderr)
    return code
