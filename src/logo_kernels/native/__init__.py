"""Native backend discovery. Returns the first loadable shim name, or None."""
from __future__ import annotations

import ctypes
import logging
from pathlib import Path

log = logging.getLogger("logo_kernels.native")

_HERE = Path(__file__).resolve().parent

def _try_cpp() -> str | None:
    lib = _HERE / "liblogo_vec.dll"
    if not lib.exists():
        return None
    ctypes.CDLL(str(lib))
    return "native_cpp"

def _try_csharp() -> str | None:
    try:
        import clr  # type: ignore  # pythonnet
    except ImportError:
        return None
    return "native_csharp"

def _try_java() -> str | None:
    try:
        import py4j  # type: ignore
    except ImportError:
        return None
    return "native_java"

def load_native() -> str | None:
    for probe in (_try_cpp, _try_csharp, _try_java):
        try:
            hit = probe()
        except Exception as exc:  # noqa: BLE001
            log.debug("native probe %s failed: %s", probe.__name__, exc)
            continue
        if hit:
            return hit
    return None