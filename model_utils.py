from os import listdir
from os.path import isfile, join


PRIM_DELIM = ','
SEC_DELIM = ';'
EXT_DELIM = '.'

ID_IDX = 0
NAME_IDX = 1
POINTERS_IDX = 2
TYPE_IDX = 3
OPTIONS_IDX = 4

MODELS_DIR_NAME = 'models'
MODEL_FILE_FORMAT = MODELS_DIR_NAME + '/%s.frmdl'

def load_form_model(form_model_name):
    global PRIM_DELIM, ID_IDX, NAME_IDX, POINTERS_IDX, TYPE_IDX, OPTIONS_IDX

    form_model_path = path_for_model(form_model_name)

    form_model = {}

    with open(form_model_path, 'r') as form_model_file:
        lines = form_model_file.readlines()
        for i, line in enumerate(lines):
            line = line.replace('\n', '')
            line_arr = line.split(PRIM_DELIM)
            field_id = line_arr[ID_IDX]
            field_name = line_arr[NAME_IDX]
            field_pointers = split_str(line_arr[POINTERS_IDX])
            field_type = line_arr[TYPE_IDX]
            field_options = split_str(line_arr[OPTIONS_IDX])
            field_idx = i
            field = {'id': field_id, 'name': field_name, 'pointers': field_pointers, 'type': field_type, 'options': field_options, 'idx': i}
            form_model[field_id] = field

    return form_model

def available_models():
    global EXT_DELIM, MODELS_DIR_NAME

    path = MODELS_DIR_NAME
    files = [f for f in listdir(path) if isfile(join(path, f))]
    models = [f.split(EXT_DELIM)[0] for f in files]

    return models


def split_str(as_str):
    global SEC_DELIM

    if not as_str:
        return []

    return as_str.split(SEC_DELIM)

def path_for_model(form_model_name):
    global MODEL_FILE_FORMAT

    return MODEL_FILE_FORMAT % form_model_name

    
