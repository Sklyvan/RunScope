from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


@dataclass
class DataPoint:
    timestamp: datetime
    distance: float  # meters
    heart_rate: Optional[int] = None  # bpm
    cadence: Optional[int] = None  # spm
    power: Optional[int] = None  # watts
    elevation: Optional[float] = None  # meters
    pace: Optional[float] = None  # seconds per km
    speed: Optional[float] = None  # meters per second
    ground_contact_time: Optional[int] = None  # ms
    vertical_oscillation: Optional[float] = None  # cm
    stride_length: Optional[float] = None  # meters
    temperature: Optional[float] = None  # Celsius

@dataclass
class RunData:
    data_points: List[DataPoint] = field(default_factory=list)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    file_name: Optional[str] = None

@dataclass
class RunSummary:
    total_distance: float  # meters
    total_time: float  # seconds
    avg_heart_rate: Optional[float]
    max_heart_rate: Optional[int]
    avg_cadence: Optional[float]
    max_cadence: Optional[int]
    avg_pace: Optional[float]  # seconds per km
    best_pace: Optional[float]  # seconds per km
    total_ascent: Optional[float]
    total_descent: Optional[float]

@dataclass
class RunMetrics:
    training_effect_aerobic: Optional[float]
    training_effect_anaerobic: Optional[float]
    ground_contact_balance: Optional[tuple]  # (left %, right %)
    vertical_ratio: Optional[float]  # %
    form_power: Optional[float]  # estimated
    vo2max_estimation: Optional[float]  # ml/kg/min
    running_efficiency: Optional[float]  # watts per kg
    execution_score: Optional[float]  # %
    fatigue_index: Optional[float]  # unitless score
