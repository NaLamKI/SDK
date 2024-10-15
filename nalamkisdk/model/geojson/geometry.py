from dataclasses import dataclass
import uuid
from .coordinates import GeoCoordinates
from typing import List

@dataclass
class GeoGeometry:
    coordinates: GeoCoordinates
    type: str

@dataclass
class GeoPoint:
    coordinates: GeoCoordinates
    type: str = "Point"

@dataclass
class GeoPolygon:
    coordinates: List[GeoCoordinates]
    type: str = "Polygon"
