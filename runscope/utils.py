from .models import RunData, RunSummary


def compute_run_summary(run_data: RunData) -> RunSummary:
    data_points = run_data.data_points
    if not data_points:
        raise ValueError("No data points in run")

    total_distance = data_points[-1].distance
    total_time = (run_data.end_time - run_data.start_time).total_seconds()

    heart_rates = [dp.heart_rate for dp in data_points if dp.heart_rate is not None]
    cadences = [dp.cadence for dp in data_points if dp.cadence is not None]

    # Compute pace as seconds/km
    paces = []
    for i in range(1, len(data_points)):
        dt = (data_points[i].timestamp - data_points[i - 1].timestamp).total_seconds()
        dd = data_points[i].distance - data_points[i - 1].distance
        if dd > 0:
            pace = dt / (dd / 1000.0)
            paces.append(pace)

    # Elevation gain/loss
    elevations = [dp.elevation for dp in data_points if dp.elevation is not None]
    ascent = sum(
        max(e2 - e1, 0)
        for e1, e2 in zip(elevations[:-1], elevations[1:])
    ) if elevations else None
    descent = sum(
        max(e1 - e2, 0)
        for e1, e2 in zip(elevations[:-1], elevations[1:])
    ) if elevations else None

    return RunSummary(
        total_distance=total_distance,
        total_time=total_time,
        avg_heart_rate=sum(heart_rates) / len(heart_rates) if heart_rates else None,
        max_heart_rate=max(heart_rates) if heart_rates else None,
        avg_cadence=sum(cadences) / len(cadences) if cadences else None,
        max_cadence=max(cadences) if cadences else None,
        avg_pace=sum(paces) / len(paces) if paces else None,
        best_pace=min(paces) if paces else None,
        total_ascent=ascent,
        total_descent=descent
    )
