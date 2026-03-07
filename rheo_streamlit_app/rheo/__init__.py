"""RheoDB core package.

This package provides:
- SQLite schema + helpers
- Import of rheometer export files (CSV/XLSX)
- Flow-curve analysis (up/down split, fits, hysteresis area)
- Partial-yield / wide-gap Couette interpretation (tau1c, r0/r2)

Used by the Streamlit app (app.py).
"""

__all__ = ["db"]
__version__ = "0.1.0"
