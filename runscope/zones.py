from .config import HR_ZONES, PACE_ZONES, CADENCE_ZONES
from typing import Optional
from collections import defaultdict
from .models import RunData


def get_zone(value: Optional[float], zones: list[tuple[int, int]]) -> Optional[int]:
    if value is None:
        return None
    for i, (low, high) in enumerate(zones, start=1):
        if (low <= value <= high) or (high <= value <= low):  # Handle both ascending and descending ranges
            return i
    return None


def get_hr_zone(hr: Optional[int]) -> Optional[int]:
    return get_zone(hr, HR_ZONES)


def get_pace_zone(pace: Optional[float]) -> Optional[int]:
    return get_zone(pace, PACE_ZONES)


def get_cadence_zone(cadence: Optional[int]) -> Optional[int]:
    return get_zone(cadence, CADENCE_ZONES)


def compute_zone_distribution(run_data: RunData, zone_type: str) -> dict[int, float]:
    """
    Returns a dict mapping zone number to total time (in seconds).
    zone_type: 'heart_rate', 'pace', or 'cadence'
    """
    zone_func = {
        "heart_rate": get_hr_zone,
        "pace": get_pace_zone,
        "cadence": get_cadence_zone,
    }.get(zone_type)

    if not zone_func:
        raise ValueError(f"Unsupported zone type: {zone_type}")

    time_in_zone = defaultdict(float)
    points = run_data.data_points

    for i in range(1, len(points)):
        prev, curr = points[i - 1], points[i]
        duration = (curr.timestamp - prev.timestamp).total_seconds()
        zone = zone_func(getattr(prev, zone_type))
        if zone:
            time_in_zone[zone] += duration

    return dict(time_in_zone)
