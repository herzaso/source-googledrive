import panoply
import httplib2
from apiclient.discovery import build
from oauth2client.client import AccessTokenCredentials

# TODO: implement call function from dataSource (call a function from the
# outside and return the result to a callback)
# TODO: check the CSV the fails in GD (unicode)
# TODO: validate_token should revalidate the token every time (regardless of its state)

# check https://developers.google.com/drive/v3/web/integrate-open for
# a list of available mime types
MIME_TYPES = ['text/csv',
              'text/tab-separated-values',
              'application/vnd.google-apps.script+json',
              'application/zip',
              'application/tar']
# 'application/vnd.ms-excel'
# 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'


class GD(panoply.DataSource):
    def __init__(self, source, options):
        super(GD, self).__init__(source, options)

        self._query = ' or '.join(['mimeType=\'{}\''
                                   .format(m) for m in MIME_TYPES])

        files = source.get("files") or []
        self._files = files[:]
        self._service = None
        self._init_service(source.get("access_token"))

    def _init_service(self, access_token):
        creds = AccessTokenCredentials(access_token, 'panoply/1.0')
        http = creds.authorize(http=httplib2.Http())
        self._service = build('drive', 'v3', http=http)

    @panoply.validate_token('_init_service')
    def read(self, n=None):
        if len(self._files) == 0:
            return None # no files left, we're done

        file = self._files.pop(0)
        print("Reading File {}".format(file))

        content = self._service.files().get_media(fileId=file['id']).execute()
        print(content)
        return content

    # read the next batch of data
    @panoply.validate_token('_init_service')
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
            raise Exception("No supported files detected")

        return result
