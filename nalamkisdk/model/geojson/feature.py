from dataclasses import dataclass
import uuid
from .geometry import GeoGeometry, GeoPoint, GeoPolygon
from .property import GeoFeatureProperty
from typing import List

@dataclass
class GeoFeature:
    geometry: GeoGeometry
    id: uuid = None
    properties: GeoFeatureProperty = None
    type: str = "Feature"

    def __post_init__(self):
        self.id = uuid.uuid4()
