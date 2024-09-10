from dataclasses import dataclass
from .dataset import Dataset
from typing import List
import uuid

from .timeseriesItem import TimeSeriesItem

@dataclass
class Timeseries(Dataset):
    items: List[TimeSeriesItem]
    id: uuid = None
    type: str = None

    def __post_init__(self):
        self.id = uuid.uuid4()
        self.type = "TIMESERIES"