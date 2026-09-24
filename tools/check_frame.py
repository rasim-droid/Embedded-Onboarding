#!/usr/bin/env python3
"""
STATUS LINE CHECKER

Checks the status line from README.md, section 3.3:

    NODE,<uptime_s>,<co2_ppm>,<temp_c_x10>,<adc_mv>,<pwm_duty>,<flags>

Usage:
    python3 tools/check_frame.py            paste lines in, then Ctrl-D
    python3 tools/check_frame.py log.txt    check a captured file
    python3 tools/check_frame.py -v log.txt decode each line
    python3 tools/check_frame.py --example  print a valid line

Exit status 0 if everything passed, 1 otherwise.
Run it on yourself before your debrief. If you think it is wrong, say so at
your debrief and bring the evidence.
"""

import argparse
import re
import sys

LINE_RE = re.compile(
    r"^NODE,"
    r"(?P<uptime>0|[1-9][0-9]*),"
    r"(?P<co2>0|[1-9][0-9]*),"
    r"(?P<temp>0|-?[1-9][0-9]*),"
    r"(?P<adc>0|[1-9][0-9]*),"
    r"(?P<duty>0|[1-9][0-9]*),"
    r"(?P<flags>[0-9A-F]{2})$"
)

RANGES = {
    "uptime": (0, 4294967295, "uptime_s"),
    "co2": (0, 40000, "co2_ppm"),
    "temp": (-400, 1250, "temp_c_x10"),
    "adc": (0, 3300, "adc_mv"),
    "duty": (0, 100, "pwm_duty"),
}

FLAG_NAMES = ["sensor not answering", "kill switch latched", "CRC failure"]
RESERVED_MASK = 0xF8  # bits 3-7


def check(line):
    """Return (ok, [problems], decoded_or_None)."""
    problems = []

    m = LINE_RE.match(line)
    if not m:
        if not line.startswith("NODE,"):
            problems.append("does not start with 'NODE,'")
        elif " " in line:
            problems.append("contains a space - there are no spaces in the line")
        elif line.count(",") != 6:
            problems.append("expected 6 commas, found %d" % line.count(","))
        elif re.search(r",0[0-9]", line):
            problems.append("looks like a number with a leading zero - send 5, not 05")
        elif line != line.upper():
            problems.append("flags must be UPPERCASE hex, e.g. 0A not 0a")
        else:
            problems.append("does not match the format in README.md section 3.3")
        return False, problems, None

    d = {k: int(m.group(k)) for k in RANGES}
    flags = int(m.group("flags"), 16)

    for key, (lo, hi, label) in RANGES.items():
        if not (lo <= d[key] <= hi):
            problems.append("%s = %d is outside %d..%d" % (label, d[key], lo, hi))

    if flags & RESERVED_MASK:
        problems.append("flag bits 3-7 should be 0, got 0x%02X" % (flags & RESERVED_MASK))

    d["flags"] = flags
    return (not problems), problems, d


def describe(d):
    f = d["flags"]
    if f:
        names = [FLAG_NAMES[i] for i in range(3) if f & (1 << i)]
        flagtxt = "%02X  (%s)" % (f, ", ".join(names) if names else "?")
    else:
        flagtxt = "00  (all clear)"
    return "\n".join([
        "      up %d s" % d["uptime"],
        "      CO2 %d ppm" % d["co2"],
        "      temp %.1f C" % (d["temp"] / 10.0),
        "      pot %d mV" % d["adc"],
        "      pwm %d%%" % d["duty"],
        "      flags %s" % flagtxt,
    ])


def main():
    ap = argparse.ArgumentParser(description="Check onboarding task status lines.")
    ap.add_argument("file", nargs="?", help="captured file; omit to read what you paste in")
    ap.add_argument("-v", "--verbose", action="store_true", help="decode each valid line")
    ap.add_argument("--example", action="store_true", help="print a valid line and exit")
    args = ap.parse_args()

    if args.example:
        print("NODE,142,814,231,1650,50,00")
        return 0

    if args.file:
        try:
            lines = open(args.file, "r", encoding="utf-8", errors="replace").readlines()
        except OSError as exc:
            print("cannot read %s: %s" % (args.file, exc), file=sys.stderr)
            return 1
    else:
        if sys.stdin.isatty():
            print("Paste your status lines, then press Ctrl-D (Ctrl-Z on Windows).\n")
        lines = sys.stdin.readlines()

    total = passed = 0
    for n, raw in enumerate(lines, 1):
        line = raw.strip()
        if not line:
            continue
        total += 1
        ok, problems, d = check(line)
        if ok:
            passed += 1
            print("line %-4d OK    %s" % (n, line))
            if args.verbose:
                print(describe(d))
        else:
            print("line %-4d BAD   %s" % (n, line))
            for p in problems:
                print("               -> %s" % p)

    if total == 0:
        print("No lines found. Is your node printing, and did you capture the 'NODE,' part?")
        return 1

    print("\n%d line(s) checked, %d OK, %d bad." % (total, passed, total - passed))
    if passed == total:
        print("All good. See you at the debrief.")
    return 0 if passed == total else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
    except KeyboardInterrupt:
        sys.exit(130)
