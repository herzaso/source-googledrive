import source
from conf import CONFIG, REFRESH_URL

Stream = source.GoogleDrive


def get_files(source, *args, **kwargs):
    return Stream(source, *args, **kwargs).get_files()

files_param = [x for x in CONFIG['params'] if x['name'] == 'files'][0]
files_param['values'] = get_files
