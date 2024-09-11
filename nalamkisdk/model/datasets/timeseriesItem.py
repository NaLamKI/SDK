from dataclasses import dataclass
from .dataset import Dataset
from typing import List

import uuid
from datetime import datetime
from .datavalue import DataValue
from .dataimage import DataImage

@dataclass
class TimeSeriesItem:
    timestamp: datetime
    values: List[DataValue] = None
    images: List[DataImage] = None
    id: uuid = None
    def __post_init__(self):
        self.id = uuid.uuid4()
