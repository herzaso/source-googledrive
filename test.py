import mock
import unittest
import googledrive
import apiclient
import oauth2client
import requests_mock

from panoply.errors import PanoplyException


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
            try:
                files = googledrive.Stream({
                    "type": "googledrive",
                    "access_token": "654321",
                    "files": [{u'id': u'12345', u'name': u'file1.csv'}]
                }, {'refresh':{}}).get_files()
            except oauth2client.client.AccessTokenCredentialsError:
                pass

        self.assertEqual(files, res['files'])


# empty object, used for mocking
class Object(object): pass

# fire it up.
if __name__ == "__main__":
    unittest.main()
