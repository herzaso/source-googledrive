import s3v2
import mock
import boto3
import unittest

orig_client = boto3.client

class TestS3(unittest.TestCase):

    def tearDown(self):
        boto3.client = orig_client


    def test_credentials(self):
        "aws key and secret are passed to the s3 client"

        boto3.client = mock.MagicMock()
        s3v2.S3({
            "addr": "s3://panoply-test",
            "awskey": "S3-KEY",
            "awssecret": "S3-SECRET"
            # "awskey": "AKIAIHL3ZLRO7LOIVTVQ",
            # "awssecret": "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"
        }, {})

        boto3.client.assert_called_once_with("s3",
            aws_access_key_id = "S3-KEY",
            aws_secret_access_key = "S3-SECRET"
        )

    def test_get_files(self):
        "retrieves the list of files by address prefix"

        m = Object()
        m.list_objects = mock.MagicMock(return_value = {
            "Contents": [{
                "Key": "1234.csv",
                "E-Tag": "aabbff"
            }, {
                "Key": "5678.json",
                "E-Tag": "aabbff"
            }]
        })

        boto3.client = mock.MagicMock(return_value = m)
        files = s3v2.S3({
            "addr": "s3://panoply-test/myfiles/",
            "awskey": "S3-KEY",
            "awssecret": "S3-SECRET",
            "files": None
        }, {}).get_files()

        m.list_objects.assert_called_once_with(
            Bucket = "panoply-test",
            Prefix = "myfiles/"
        )

        self.assertEqual(files, ["1234.csv", "5678.json"])


    def test_read_file(self):
        "reads the data from the file"

        f = Object()
        f.read = mock.MagicMock(return_value = "hello,world")

        m = Object()
        m.get_object = mock.MagicMock(return_value = {
            "Body": f
        })

        boto3.client = mock.MagicMock(return_value = m)
        s = s3v2.S3({
            "addr": "s3://panoply-test",
            "awskey": "S3-KEY",
            "awssecret": "S3-SECRET",
            "files": [
                "roi/t123"
            ]
        }, {})

        data = s.read()
        self.assertEqual(data, "hello,world")
        m.get_object.assert_called_once_with(
            Bucket = "panoply-test",
            Key = "roi/t123"
        )



# empty object, used for mocking
class Object(object): pass

# fire it up.
if __name__ == "__main__":
    unittest.main()