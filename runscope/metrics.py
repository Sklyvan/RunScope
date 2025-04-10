from .models import RunData, RunMetrics
from statistics import mean
from typing import Optional


def compute_gct_balance(run_data: RunData) -> Optional[tuple[float, float]]:
    left_gct = [dp.ground_contact_time for dp in run_data.data_points if dp.ground_contact_time and dp.timestamp.second % 2 == 0]
    right_gct = [dp.ground_contact_time for dp in run_data.data_points if dp.ground_contact_time and dp.timestamp.second % 2 == 1]

    if not left_gct or not right_gct:
        return None

    total = sum(left_gct) + sum(right_gct)
    return 100 * sum(left_gct) / total, 100 * sum(right_gct) / total


def compute_vertical_ratio(run_data: RunData) -> Optional[float]:
    ratios = []
    for dp in run_data.data_points:
        if dp.vertical_oscillation and dp.stride_length:
            ratio = (dp.vertical_oscillation / (dp.stride_length * 100)) * 100
            ratios.append(ratio)
    return sum(ratios) / len(ratios) if ratios else None


def estimate_vo2max_speed_based(pace_s_per_km: float) -> float:
    velocity_m_per_min = 1000 / (pace_s_per_km / 60)
    return (velocity_m_per_min * 0.2) + 3.5


def estimate_vo2max_heart_rate_based(vo2_submax: float, heart_rate: int, hr_rest: int, hr_max: int) -> Optional[float]:
    if hr_max == hr_rest:
        return None  # Prevent division by zero
    vo2_percent = (heart_rate - hr_rest) / (hr_max - hr_rest)
    if vo2_percent == 0:
        return None
    return vo2_submax / vo2_percent


def estimate_vo2max_power_based(power: float, body_mass_kg: float, running_economy_kj_per_kg_km: float = 1.0) -> Optional[float]:
    if running_economy_kj_per_kg_km <= 0 or body_mass_kg <= 0:
        return None
    velocity_kmh = (power / (running_economy_kj_per_kg_km * body_mass_kg)) * 3.6
    vo2 = (velocity_kmh * 1000 / 60) * 0.2 + 3.5
    return vo2


def estimate_vo2max(method: str = "speed", **kwargs) -> Optional[float]:
    method = method.lower()
    if method == "speed":
        return estimate_vo2max_speed_based(kwargs.get("pace_s_per_km"))
    elif method == "heart_rate":
        return estimate_vo2max_heart_rate_based(
            kwargs.get("vo2_submax"),
            kwargs.get("heart_rate"),
            kwargs.get("hr_rest"),
            kwargs.get("hr_max")
        )
    elif method == "power":
        return estimate_vo2max_power_based(
            kwargs.get("power"),
            kwargs.get("body_mass_kg"),
            kwargs.get("running_economy_kj_per_kg_km", 1.0)
        )
    return None


def compute_vo2max_auto(
    run_data: RunData,
    body_mass_kg: Optional[float] = None,
    hr_rest: Optional[int] = None,
    hr_max: Optional[int] = None
) -> Optional[float]:
    """
    Auto-selects the best available VO2max estimation method.
    """
    # Try power-based
    powers = [dp.power for dp in run_data.data_points if dp.power is not None]
    if powers and body_mass_kg:
        avg_power = mean(powers)
        return estimate_vo2max(method="power", power=avg_power, body_mass_kg=body_mass_kg)

    # Try HR-based
    heart_rates = [dp.heart_rate for dp in run_data.data_points if dp.heart_rate is not None]
    paces = [dp.pace for dp in run_data.data_points if dp.pace is not None]

    if heart_rates and hr_rest and hr_max and paces:
        avg_hr = mean(heart_rates)
        avg_pace = mean(paces)
        vo2_submax = estimate_vo2max(method="speed", pace_s_per_km=avg_pace)
        return estimate_vo2max(
            method="heart_rate",
            vo2_submax=vo2_submax,
            heart_rate=avg_hr,
            hr_rest=hr_rest,
            hr_max=hr_max
        )

    # Fallback to speed-based
    if paces:
        avg_pace = mean(paces)
        return estimate_vo2max(method="speed", pace_s_per_km=avg_pace)

    return None

def compute_form_power(run_data: RunData, body_mass_kg: float = 65.0) -> Optional[float]:
    g = 9.81
    verticals = [dp.vertical_oscillation for dp in run_data.data_points if dp.vertical_oscillation]
    gcts = [dp.ground_contact_time for dp in run_data.data_points if dp.ground_contact_time]

    if not verticals or not gcts:
        return None

    avg_vo = sum(verticals) / len(verticals) / 100  # cm to m
    avg_gct = sum(gcts) / len(gcts) / 1000  # ms to s

    return (body_mass_kg * g * avg_vo) / avg_gct


def compute_running_efficiency(run_data: RunData) -> Optional[float]:
    powers = [dp.power for dp in run_data.data_points if dp.power]
    if not powers:
        return None
    avg_power = sum(powers) / len(powers)
    total_distance = run_data.data_points[-1].distance
    total_time = (run_data.end_time - run_data.start_time).total_seconds()
    speed = total_distance / total_time if total_time else 0
    return avg_power / speed if speed else None


def compute_fatigue_index(run_data: RunData) -> Optional[float]:
    dps = [dp for dp in run_data.data_points if dp.heart_rate]
    if len(dps) < 4:
        return None

    n = len(dps)
    first = [dp.heart_rate for dp in dps[:n//4]]
    last = [dp.heart_rate for dp in dps[-n//4:]]
    overall = [dp.heart_rate for dp in dps]

    return (sum(last)/len(last) - sum(first)/len(first)) / (sum(overall)/len(overall))


def compute_run_metrics(run_data: RunData) -> RunMetrics:
    return RunMetrics(
        training_effect_aerobic=None,  # Reserved for future
        training_effect_anaerobic=None,
        ground_contact_balance=compute_gct_balance(run_data),
        vertical_ratio=compute_vertical_ratio(run_data),
        form_power=compute_form_power(run_data),
        vo2max_estimation=compute_vo2max_auto(run_data, body_mass_kg=60, hr_rest=45, hr_max=190), # TODO: These values should be passed from the user
        running_efficiency=compute_running_efficiency(run_data),
        execution_score=None,
        fatigue_index=compute_fatigue_index(run_data)
    )
