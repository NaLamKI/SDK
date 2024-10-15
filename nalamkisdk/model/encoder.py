import json
from datetime import datetime
from uuid import UUID

from .geojson.geometry import GeoCoordinates, GeoPolygon, GeoPoint

class NaLamKIDataEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return obj.hex
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, GeoCoordinates):
            return obj.tojson()
        return json.JSONEncoder.default(self, obj)
