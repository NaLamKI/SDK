from dataclasses import dataclass
import uuid

from datetime import datetime
from typing import List

from .geojson import GeoFeature, GeoGeometry, GeoCoordinates, GeoFeatureProperty

from .datasets import Dataset, Timeseries, TimeSeriesItem, DataValue, File, Image

@dataclass
class OutputData: 
    type: str
    
@dataclass
class GeoOutputData(OutputData):
    features: List[GeoFeature]

@dataclass
class Datasets(OutputData):
    dataset: List[Dataset]
