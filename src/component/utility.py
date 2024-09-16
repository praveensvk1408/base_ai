# ------------------------------------------------------------------------
# Copyright 2024 Sony Semiconductor Solutions Corp. All rights reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------
# pylint:disable=wrong-import-position
# pylint:disable=duplicate-code
# pylint:disable=too-few-public-methods
# pylint:disable=missing-module-docstring
# pylint:disable=import-error
"""This module implements all the API's related to '''Utility''' """
import os

import requests

from src.component.get_token import GetToken

class Utility:
    """this class implements Utility API"""

    def __init__(self):
        """This constructor initializes the base url"""
        self.REST_API_URL = os.getenv(
            "REST_API_URL"
        )  # Azure Blob Storage common.json

    def upload_file(self, type_code, file_name, file_content):
        """This function implements '''UploadFile''' API"""
        # Base url with end points
        url = f"{self.REST_API_URL}/files?grant_type=client_credentials"
        token = "Bearer "+GetToken().get_token().json()["access_token"]  # fetching the token
        file_data = {"file" : (file_name, file_content)}
        req_data = {  # request body of UploadFile API
            "type_code": type_code,
        }
        response = requests.post(
            url,
            headers={"authorization": token},
            data=req_data,
            files=file_data,
            timeout=30,  # sending request to the server
        )
        return response