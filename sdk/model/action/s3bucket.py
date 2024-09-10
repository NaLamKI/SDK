from dataclasses import dataclass

@dataclass
class S3Bucket():
    endpoint: str
    port: int 
    name: str
    accessId: str
    accessToken: str