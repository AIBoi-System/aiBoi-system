"""Compatibility exports for the inventory application layer.

The canonical pasture implementation lives in ``pasture_service``. Keeping a
single implementation prevents tenant-filter rules from drifting between two
services with the same name.
"""

from app.modules.inventory.application.pasture_service import (
    PastureService,
    pasture_service,
)

__all__ = ["PastureService", "pasture_service"]
