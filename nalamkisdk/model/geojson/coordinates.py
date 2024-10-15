from dataclasses import dataclass
import uuid

@dataclass
class GeoCoordinates:
    latitude: float
    longitude: float

    def tojson(self):
        return [self.longitude, self.latitude]
