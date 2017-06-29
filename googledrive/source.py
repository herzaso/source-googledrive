import panoply
import httplib2
import io
from conf import CONFIG, REFRESH_URL
from apiclient.http import MediaIoBaseDownload
from apiclient.discovery import build
from oauth2client.client import AccessTokenCredentials, \
                                AccessTokenCredentialsError
from panoply.errors import PanoplyException

# silence warnings from oauth2client logger
import logging
_helpers_log = logging.getLogger('oauth2client._helpers')
_helpers_log.addHandler(logging.NullHandler())

# check https://developers.google.com/drive/v3/web/integrate-open for
# a list of available mime types
MIME_TYPES = ['text/csv',
              'text/tab-separated-values',
              'application/vnd.google-apps.script+json',
              'application/zip',
              'application/tar']

CHUNK_SIZE = 0.5 * 1024 * 1024 # 0.5MB
BATCH_MAX_SIZE = 5 * 1024 * 1024 # 5MB
DEST = 'google_drive'
ERRORS = (AccessTokenCredentialsError)


class GoogleDrive(panoply.DataSource):
    def __init__(self, *args, **kwargs):
        super(GoogleDrive, self).__init__(*args, **kwargs)

        self.source["destination"] = self.source.get("destination") or DEST

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
        self._init_service(self.source.get('access_token'))
        self.fh = None # file handler
        self.downloader = None

    @panoply.validate_token(REFRESH_URL, exceptions=ERRORS)
    def _init_service(self, token=None):
        creds = AccessTokenCredentials(token, 'panoply/1.0')
        http = creds.authorize(http=httplib2.Http())
        self._service = build('drive', 'v3', http=http)

    @panoply.validate_token(REFRESH_URL, '_init_service', exceptions=ERRORS)
    def read(self, n=None):
        if len(self._files) == 0:
            return None # no files left, we're done

        file = self._files[0]
        count = self._total - len(self._files)
        msg = '{}/{} files loaded'.format(count, self._total)

        # if we're not in the middle of downloading a file, start downloading
        if not self.fh or not self.downloader:
            request = self._service.files().get_media(fileId=file['id'])
            self.fh = io.BytesIO()
            self.downloader = MediaIoBaseDownload(self.fh, request, CHUNK_SIZE)
        else:
            # otherwise, just truncate the content - get ready to a new batch
            self.fh.seek(0)
            self.fh.truncate()

        # read until BATCH_MAX_SIZE is reached
        # notice that the chunks are quite big
        done = False
        content = ''
        while not done and len(content) < BATCH_MAX_SIZE:
            status, done = self.downloader.next_chunk()
            content = self.fh.getvalue()
            self.progress(count, self._total, msg)

        self.log('Read {} bytes from file {}'
                 .format(len(content), file['name']))

        if done:
            self._files.pop()
            self.fh = None
            self.downloader = None

        return content

    @panoply.validate_token(REFRESH_URL, '_init_service', exceptions=ERRORS)
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
