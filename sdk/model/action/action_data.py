from dataclasses import dataclass
import dataclasses
import json

from ..encoder import NaLamKIDataEncoder

from .s3bucket import S3Bucket

@dataclass
class ActionData():
    bucket:S3Bucket
    inputData: [str]
    outputData: str

