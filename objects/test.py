#!/usr/bin/env python3

import zlib

payload = b"commit 1086\x00" + (b"a" * 1086)
compressed = zlib.compress(payload)


