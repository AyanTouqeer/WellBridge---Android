from enum import IntEnum


class Tab(IntEnum):
    """Bottom-nav order. Single source of truth for tab indexes."""

    DISCOVER = 0
    BOOKINGS = 1
    WELL_E = 2
    MY_CARE = 3
    PROFILE = 4