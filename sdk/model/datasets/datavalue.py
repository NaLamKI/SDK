
from dataclasses import dataclass
from .dataset import Dataset
import uuid

@dataclass
class DataValue:
    value: any
    name: str # unique in Dataset (Reference for Widgettemplate)
    unit: str = None
    type: str = None