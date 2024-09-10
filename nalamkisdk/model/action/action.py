from dataclasses import dataclass
import dataclasses
import json

from ..encoder import NaLamKIDataEncoder

from .s3bucket import S3Bucket
from .action_data import ActionData


@dataclass
class Action():
    pattern:str
    data: ActionData

    @classmethod
    def from_json(cls,json_string):
        json_dict = json.loads(json_string)
        if json_dict['pattern'] == "start":
            action_data = ActionData(S3Bucket(json_dict['data']['bucket']['endpoint'], json_dict['data']['bucket']['port'], json_dict['data']['bucket']['name'], json_dict['data']['bucket']['accessId'], json_dict['data']['bucket']['accessToken']), json_dict['data']['inputData'], json_dict['data']['outputData'])
        else:
            action_data = None
            
        action = Action(json_dict['pattern'], action_data)
        return action

