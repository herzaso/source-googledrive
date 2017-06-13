import source

Stream = source.GD

from conf import CONFIG

def get_files(*args, **kwargs):
    return Stream(*args, **kwargs).get_files()

CONFIG['params'][-1]["values"] = get_files
