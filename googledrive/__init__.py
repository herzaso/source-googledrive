import source
from conf import CONFIG, REFRESH_URL

Stream = source.GoogleDrive


def get_files(source, *args, **kwargs):
    return Stream(source, *args, **kwargs).get_files()

CONFIG['params'][-1]['values'] = get_files
