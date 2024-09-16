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
"""This module implements all the API's related to '''Manage Device''' """
import os

import requests

from src.component.get_token import GetToken


class ManageDevices:
    """This class implements the '''Get device''' API"""

    def __init__(self):
        """This constructor initializes the base url"""
        self.REST_API_URL = os.getenv(
            "REST_API_URL"
        )  # Azure Blob Storage common.json

    def get_device(self, device_id):
        """This function implements the Get device API"""
        # Base url with end points
        url = f"{self.REST_API_URL}/devices/{device_id}?grant_type=client_credentials"
        token = "Bearer "+GetToken().get_token().json()["access_token"]  # fetching the token
        response = requests.get(
            url, headers={"authorization": token}, timeout=30
        )  # request body of the Create Firmware API
        return response  # returning the response
