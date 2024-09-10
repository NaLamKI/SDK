from dataclasses import dataclass

@dataclass
class BoundingBox():
    x:int
    y:int
    h:int
    w:int
    color: str = None
    classification: str = None
    label: str = None
    accuracy: int = None
    