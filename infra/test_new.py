import json
import unittest
import boto3
from moto import mock_s3
import lambda_folder.constants as constants

S3_BUCKET_NAME = "motobucket"
DEFAULT_REGION = 'us-east-2'

S3_TEST_FILE_KEY = 'pokemon.json'
S3_TEST_FILE_CONTENT = [
    {"name": "lucario", "type": "steel/fight"},
    {"name": "squirtle", "type":"water" }
]

@mock_s3
class TestLambdaFunction(unittest.TestCase):

    def setUp(self):
        self.s3 = boto3.resource('s3', region_name=DEFAULT_REGION)
        self.s3_bucket = self.s3.create_bucket(Bucket=S3_BUCKET_NAME)
        self.s3_bucket.put_object(Key=S3_TEST_FILE_KEY,
                                  Body=json.dumps(S3_TEST_FILE_CONTENT))

    def test_get_data_from_file(self):
        from index import get_data_from_file

        file_content = get_data_from_file(S3_BUCKET_NAME, S3_TEST_FILE_KEY)
        self.assertEqual(file_content, S3_TEST_FILE_CONTENT)