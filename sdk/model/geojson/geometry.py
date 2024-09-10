from dataclasses import dataclass
import uuid
from .coordinates import GeoCoordinates

@dataclass
class GeoGeometry:
    type:str
    coordinates: GeoCoordinates