import json
import os,sys
from flair.models import SequenceTagger
from pathlib import Path

def load_model(id_type):
    with open("./model_list.json","r") as f:
        model_dict=json.load(f)
        # print(model_dict)
    if id_type in model_dict.keys():
        model = SequenceTagger.load_from_file(model_file=Path(
            './models/'+id_type+'.pt'))
        # print(model_dict[id_type])
        return model,model_dict[id_type]
    else :
        return None
