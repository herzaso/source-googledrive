import panoply
import httplib2
from conf import CONFIG, REFRESH_URL
from apiclient.discovery import build
from oauth2client.client import AccessTokenCredentials
from panoply.errors import PanoplyException

# check https://developers.google.com/drive/v3/web/integrate-open for
# a list of available mime types
MIME_TYPES = ['text/csv',
              'text/tab-separated-values',
              'application/vnd.google-apps.script+json',
              'application/zip',
              'application/tar']
# 'application/vnd.ms-excel'
# 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

class GoogleDrive(panoply.DataSource):
    def __init__(self, *args, **kwargs):
        super(GD, self).__init__(*args, **kwargs)

        # fetch only non trashed files with acceptable mime types
        self._query = 'and'.join([
            'trashed = false',
            ' or '.join(['mimeType=\'{}\''
                        .format(m) for m in MIME_TYPES])
        ])

        files = self.source.get('files', [])
        self._files = files[:]
        self._total = len(self._files)
        self._service = None
        self._init_service()

    @panoply.invalidate_token(REFRESH_URL)
    def _init_service(self, token=None):
        token = token or self.source.get('access_token')
        creds = AccessTokenCredentials(token, 'panoply/1.0')
        http = creds.authorize(http=httplib2.Http())
        self._service = build('drive', 'v3', http=http)

    @panoply.invalidate_token(REFRESH_URL, '_init_service')
    def read(self, n=None):
        if len(self._files) == 0:
            return None # no files left, we're done

        file = self._files.pop(0)
        self.log('Reading File {}'.format(file))
        content = self._service.files().get_media(fileId=file['id']).execute()

        count = self._total - len(self._files)
        msg = '{}/{} files loaded'.format(count, self._total)
        self.progress(count, self._total, msg)

        return content

    # read the next batch of data
    @panoply.invalidate_token(REFRESH_URL, '_init_service')
    def get_files(self):
        result = []
        page_token = None
        while True:
            response = self._service.files().list(
                spaces='drive',
                fields='nextPageToken, files(id, name)',
                q=self._query,
                orderBy='name',
                pageToken=page_token
            ).execute()

            result.extend(response.get('files', []))
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break

        if not result:
            raise PanoplyException(
                'No supported files detected',
                retryable=False)

        return result
