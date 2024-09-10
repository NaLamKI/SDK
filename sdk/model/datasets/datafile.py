from dataclasses import dataclass

@dataclass
class File:
    uri:str
    name:str = None
    type:str = None # NaLamKI Type (z.B. DROHNENBILD 10m)
     
    