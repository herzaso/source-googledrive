import mock
import unittest
import googledrive
import apiclient
import requests_mock

from googledrive.source import MediaIoBaseDownload
from panoply.errors import PanoplyException
from oauth2client.client import AccessTokenCredentialsError


counter = 0


def next_chunk(self, num_retries=1):
    global counter

    counter += 1
    if counter == 2:
        raise AccessTokenCredentialsError()

    self._fd.write('Lorem ipsum dolor sit amet')
    return 200, True


class TestGoogleDrive(unittest.TestCase):

    def test_get_files(self):
        "retrieves the list of files from google drive"

        res = {
            "nextPageToken": None,
            "files": [{
                "name": "1234.csv",
                "id": "aabbff"
            }, {
                "name": "5678.json",
                "id": "aabbff"
            }]
        }

        apiclient.discovery.build = mock.MagicMock()
        with mock.patch('apiclient.http.HttpRequest.execute') as mock_exec:
            mock_exec.return_value = res
            files = googledrive.Stream({
                "type": "googledrive",
                "access_token": "654321",
                "files": [{u'id': u'12345', u'name': u'file1.csv'}]
            }, {'refresh': {}}).get_files()

        self.assertEqual(files, res['files'])

    @mock.patch.object(MediaIoBaseDownload, 'next_chunk', next_chunk)
    def test_read_one_file(self):
        "reads one file from google drive"

        s = googledrive.Stream({
            "type": "googledrive",
            "access_token": "654321",
            "files": [{u'id': u'12345', u'name': u'file1.csv'}]
        }, {'refresh': {}})
        content = s.read()

        self.assertEqual(content, 'Lorem ipsum dolor sit amet')

    # notice that next_chunk mock was designed to throw an exception on its
    # second run (which is the first run in this test)
    @mock.patch.object(MediaIoBaseDownload, 'next_chunk', next_chunk)
    def test_refresh_token_and_read_one_file(self):
        "reads one file from google drive after refreshing an expired token"

        with requests_mock.mock() as m:
            m.post(googledrive.conf.REFRESH_URL, text='{"access_token": "1"}')

            s = googledrive.Stream({
                "type": "googledrive",
                "access_token": "654321",
                "files": [{u'id': u'12345', u'name': u'file1.csv'}]
            }, {'refresh': {}})
            content = s.read()

        self.assertEqual(content, 'Lorem ipsum dolor sit amet')

if __name__ == "__main__":
    unittest.main()
