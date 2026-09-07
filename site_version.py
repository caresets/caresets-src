"""
The one version number the published resources carry.

The glossary CodeSystems, the model-to-glossary ConceptMap and the per-guide
FSH all state a version, and they are read side by side: three resources that
disagreed about which release they belonged to would be worse than three that
carried none. VERSION is that single source, and _config.yml's content_version
mirrors it for the site footer.

Raise VERSION and rebuild; nothing else needs editing.
"""

import io
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
VERSION_FILE = os.path.join(ROOT, "VERSION")

# Used only when VERSION is missing, which should not happen in a checkout.
# Deliberately not a plausible version: a resource stamped 0.0.0 is visibly
# wrong, where one stamped 0.1 would quietly look like a real release.
UNKNOWN = "0.0.0"


def read(default=UNKNOWN):
    try:
        value = io.open(VERSION_FILE, encoding="utf-8").read().strip()
    except OSError:
        return default
    return value or default
