"""Journal IF Lookup package — wraps the JCR 2025 index.

Public entry point: `lookup(query, top=5)`.
"""
from .query import lookup, _format_result  # noqa: F401
