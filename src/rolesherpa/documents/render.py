"""HTML/CSS -> PDF rendering via WeasyPrint (design.md D6).

macOS/Homebrew note (design.md D8): WeasyPrint's wheel imports cleanly but
fails to dlopen libgobject-2.0 unless /opt/homebrew/lib is on
DYLD_FALLBACK_LIBRARY_PATH, even though Pango/cairo/glib are already
installed via Homebrew. This is a known dynamic-linking quirk, not a
missing dependency - set the env var before the first `import weasyprint`
in the process so callers never have to discover this themselves.
"""

import os
import sys

if sys.platform == "darwin":
    _HOMEBREW_LIB = "/opt/homebrew/lib"
    if os.path.isdir(_HOMEBREW_LIB):
        _existing = os.environ.get("DYLD_FALLBACK_LIBRARY_PATH", "")
        if _HOMEBREW_LIB not in _existing.split(":"):
            os.environ["DYLD_FALLBACK_LIBRARY_PATH"] = (
                f"{_HOMEBREW_LIB}:{_existing}" if _existing else _HOMEBREW_LIB
            )

from weasyprint import CSS, HTML  # noqa: E402


def render(html: str, css: str | None = None) -> bytes:
    document = HTML(string=html)
    stylesheets = [CSS(string=css)] if css else None
    return document.write_pdf(stylesheets=stylesheets)
