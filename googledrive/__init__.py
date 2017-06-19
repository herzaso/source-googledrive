import source

Stream = source.GoogleDrive

from conf import CONFIG, REFRESH_URL

def get_files(*args, **kwargs):
    return Stream(*args, **kwargs).get_files()

CONFIG['params'][-1]['values'] = get_files
