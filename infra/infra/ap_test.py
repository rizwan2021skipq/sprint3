import pytest

import requests
import json


     
def test_contenttype():
     response = requests.post("https://rcz2qevuo1.execute-api.us-east-2.amazonaws.com/prod/{proxy+}")
     assert response.headers["Content-Type"] == "application/json"