#!/usr/bin/env python3
"""quote‑fetcher – fetch a random quote from https://api.quotable.io.

The script is deliberately tiny but fully typed and includes basic error handling.
"""

import sys
import json
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

API_URL = "https://api.quotable.io/random"


def fetch_quote() -> str:
    """Return the quote text from the API or raise a descriptive error."""
    req = Request(API_URL, headers={"Accept": "application/json"})
    try:
        with urlopen(req, timeout=10) as resp:
            if resp.status != 200:
                raise RuntimeError(f"Unexpected HTTP status: {resp.status}")
            data = json.loads(resp.read().decode())
            return f"\"{data['content']}\" — {data['author']}"
    except (URLError, HTTPError) as exc:
        raise RuntimeError(f"Failed to contact quote service: {exc}") from exc
    except (KeyError, json.JSONDecodeError) as exc:
        raise RuntimeError("Malformed response from quote service") from exc


def main() -> int:
    try:
        print(fetch_quote())
        return 0
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
