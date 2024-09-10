from dataclasses import dataclass
from .dataset import Dataset
from typing import List

import uuid
from datetime import datetime
from .datavalue import DataValue
from .datafile import File
from ..annotations.bbox import BoundingBox

@dataclass
class Image(File):
    bbox: List[BoundingBox] = None
    