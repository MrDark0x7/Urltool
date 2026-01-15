#!/usr/bin/env python3
"""
urltool.py — URL query encoder/decoder helper (WSA-friendly)

Key features:
- enc: encode payload for query string
- dec: decode payload from query string
- url: build full URL with param=value
- --pretty: keep readable chars unencoded (like @ and ,)
- --wsaplus: convert a leading "%27+" into "+" (WSA-style after you manually put the quote in URL)
- supports args, stdin piping, or prompt

Examples:
  python3 urltool.py enc "' UNION SELECT @@version, NULL#"
  python3 urltool.py enc "' UNION SELECT @@version, NULL#" --pretty
  python3 urltool.py enc "' UNION SELECT @@version, NULL#" --pretty --wsaplus
  echo "' UNION SELECT @@version, NULL#" | python3 urltool.py enc --pretty --wsaplus
  python3 urltool.py dec "%27+UNION+SELECT+@@version,+NULL%23"
  python3 urltool.py url "https://t/filter" category "' UNION SELECT @@version, NULL#" --pretty --wsaplus
"""

from __future__ import annotations

import argparse
import sys
from urllib.parse import quote_plus, quote, unquote_plus, unquote

DEFAULT_PRETTY_SAFE = "@,()=/:._-"


def read_payload(arg: str | None) -> str:
    if arg is not None:
        return arg
    if not sys.stdin.isatty():
        return sys.stdin.read().rstrip("\n")
    try:
        return input("payload> ")
    except KeyboardInterrupt:
        print("\nCancelled.", file=sys.stderr)
        sys.exit(1)


def encode_query(s: str, plus: bool, safe: str) -> str:
    # plus=True => spaces -> '+'
    return quote_plus(s, safe=safe) if plus else quote(s, safe=safe)


def decode_query(s: str, plus: bool) -> str:
    # plus=True => '+' treated as space
    return unquote_plus(s) if plus else unquote(s)


def build_url(base: str, param: str, encoded_value: str) -> str:
    joiner = "&" if "?" in base else "?"
    return f"{base}{joiner}{param}={encoded_value}"


def wsa_plus_transform(encoded: str) -> str:
    """
    If payload begins with "' " then normal encoding becomes '%27+...'
    WSA examples often omit the encoded quote and start with '+...'
    This converts leading '%27+' -> '+'
    (Only at the start, does not touch other %27 in the string.)
    """
    if encoded.startswith("%27+"):
        return "+" + encoded[4:]
    if encoded.startswith("%27%20"):
        # if user used --percent20, turn "%27%20" -> "%20"?? safest is just drop the %27
        return encoded[3:]
    return encoded


def main() -> None:
    p = argparse.ArgumentParser(
        description="URL query encoder/decoder helper (spaces -> + by default).",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    enc = sub.add_parser("enc", help="Encode payload for URL query usage.")
    enc.add_argument("payload", nargs="?", help="Payload string. If omitted, read from stdin or prompt.")
    enc.add_argument("--percent20", action="store_true", help="Use %%20 for spaces instead of '+'.")
    enc.add_argument("--safe", default=None, help="Characters to NOT encode (overrides --pretty).")
    enc.add_argument("--pretty", action="store_true", help=f"Keep readable chars unencoded (default: {DEFAULT_PRETTY_SAFE!r}).")
    enc.add_argument("--wsaplus", action="store_true", help="Convert leading '%27+' into '+' (WSA-style).")

    dec = sub.add_parser("dec", help="Decode a URL-encoded query string.")
    dec.add_argument("payload", nargs="?", help="Encoded string. If omitted, read from stdin or prompt.")
    dec.add_argument("--no-plus", action="store_true", help="Do not treat '+' as space.")

    url = sub.add_parser("url", help="Build full URL with a parameter and encoded payload.")
    url.add_argument("base_url", help="Base URL (e.g. https://target/filter)")
    url.add_argument("param", help="Parameter name (e.g. category)")
    url.add_argument("payload", nargs="?", help="Payload string. If omitted, read from stdin or prompt.")
    url.add_argument("--percent20", action="store_true", help="Use %%20 for spaces instead of '+'.")
    url.add_argument("--safe", default=None, help="Characters to NOT encode (overrides --pretty).")
    url.add_argument("--pretty", action="store_true", help=f"Keep readable chars unencoded (default: {DEFAULT_PRETTY_SAFE!r}).")
    url.add_argument("--wsaplus", action="store_true", help="Convert leading '%27+' into '+' (WSA-style).")

    args = p.parse_args()

    if args.cmd == "enc":
        raw = read_payload(args.payload)
        safe = args.safe if args.safe is not None else (DEFAULT_PRETTY_SAFE if args.pretty else "")
        out = encode_query(raw, plus=not args.percent20, safe=safe)
        if args.wsaplus:
            out = wsa_plus_transform(out)
        print(out)
        return

    if args.cmd == "dec":
        raw = read_payload(args.payload)
        print(decode_query(raw, plus=not args.no_plus))
        return

    if args.cmd == "url":
        raw = read_payload(args.payload)
        safe = args.safe if args.safe is not None else (DEFAULT_PRETTY_SAFE if args.pretty else "")
        encv = encode_query(raw, plus=not args.percent20, safe=safe)
        if args.wsaplus:
            encv = wsa_plus_transform(encv)
        print(build_url(args.base_url, args.param, encv))
        return


if __name__ == "__main__":
    main()
