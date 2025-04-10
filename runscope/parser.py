from .models import RunData, DataPoint
import xml.etree.ElementTree as ET
from datetime import datetime


def parse_tcx(file_path: str) -> RunData:
    """
    Parses a TCX file and extracts data points.
    :param file_path: Path to the TCX file.
    :return: RunData object containing the parsed data points.
    """
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Strip namespace
    ns = {
        'ns': 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2',
        'ns1': 'http://www.garmin.com/xmlschemas/ActivityExtension/v2'
    }

    data_points = []
    start_time = None
    end_time = None

    for trackpoint in root.findall('.//ns:Trackpoint', ns):
        # Timestamp
        time_elem = trackpoint.find('ns:Time', ns)
        if time_elem is None:
            continue
        timestamp = datetime.fromisoformat(time_elem.text.replace('Z', '+00:00'))

        if start_time is None:
            start_time = timestamp
        end_time = timestamp

        # Distance (in meters)
        distance_elem = trackpoint.find('ns:DistanceMeters', ns)
        distance = float(distance_elem.text) if distance_elem is not None else 0.0

        # Speed (in meters per second)
        speed_elem = trackpoint.find('ns:Extensions/ns1:TPX/ns1:Speed', ns)
        speed = float(speed_elem.text) if speed_elem is not None else None

        # Pace (in seconds per km)
        pace = 1000 / speed if speed is not None and speed > 0 else None

        # Heart Rate
        hr_elem = trackpoint.find('ns:HeartRateBpm/ns:Value', ns)
        heart_rate = int(hr_elem.text) if hr_elem is not None else None

        # Cadence
        cadence_elem = trackpoint.find('ns:Extensions/ns1:TPX/ns1:RunCadence', ns)
        cadence = int(cadence_elem.text) if cadence_elem is not None else None

        # Elevation
        ele_elem = trackpoint.find('ns:AltitudeMeters', ns)
        elevation = float(ele_elem.text) if ele_elem is not None else None

        # Temperature (some TCX files include this)
        temp_elem = trackpoint.find('ns:Extensions/ns1:TPX/ns1:Temperature', ns)
        temperature = float(temp_elem.text) if temp_elem is not None else None

        # Ground Contact Time
        gct_elem = trackpoint.find('ns:Extensions/ns1:TPX/ns1:GroundContactTime', ns)
        ground_contact_time = int(gct_elem.text) if gct_elem is not None else None

        # Vertical Oscillation
        vo_elem = trackpoint.find('ns:Extensions/ns1:TPX/ns1:VerticalOscillation', ns)
        vertical_oscillation = float(vo_elem.text) if vo_elem is not None else None

        # Stride Length
        stride_elem = trackpoint.find('ns:Extensions/ns1:TPX/ns1:StrideLength', ns)
        stride_length = float(stride_elem.text) if stride_elem is not None else None

        # Power
        power_elem = trackpoint.find('ns:Extensions/ns1:TPX/ns1:Watts', ns)
        power = int(power_elem.text) if power_elem is not None else None

        dp = DataPoint(
            timestamp=timestamp,
            distance=distance,
            heart_rate=heart_rate,
            pace=pace,
            speed=speed,
            cadence=cadence,
            power=power,
            elevation=elevation,
            temperature=temperature,
            ground_contact_time=ground_contact_time,
            vertical_oscillation=vertical_oscillation,
            stride_length=stride_length
        )

        data_points.append(dp)

    return RunData(
        data_points=data_points,
        start_time=start_time,
        end_time=end_time,
        file_name=file_path
    )
