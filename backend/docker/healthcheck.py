#!/usr/bin/env python3

"""
Health check script for the backend application.

This script performs a simple HTTP GET request to the /api/health endpoint
of the backend application to verify its health and availability.
"""

import os
import sys
import urllib.request

port = os.environ.get("UVICORN_PORT")
url = f"http://localhost:{port}/api/health"
req = urllib.request.Request(url)

# noinspection PyBroadException
try:
    with urllib.request.urlopen(req, timeout=5) as r:
        sys.exit(0 if r.status == 200 else 1)
except Exception:
    sys.exit(1)
