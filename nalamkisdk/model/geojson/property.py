from typing import List
from dataclasses import dataclass, field
import uuid
from ..datasets.dataset import Dataset

@dataclass
class GeoFeatureProperty:
    type: str
    elevation: float = None # Elevation over 0 
    roiID: uuid = None
    datasets: List[Dataset] = field(default_factory=list)

    def __post_init__(self):
        self.roiID = uuid.uuid4()