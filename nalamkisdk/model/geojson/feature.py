from dataclasses import dataclass
import uuid
from .geometry import GeoGeometry
from .property import GeoFeatureProperty
from typing import List

@dataclass
class GeoFeature:
    type:str
    geometry: GeoGeometry
    id: uuid = None
    property: GeoFeatureProperty = None

    def __post_init__(self):
        self.id = uuid.uuid4()