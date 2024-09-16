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
"""This module implements all the API's related to '''Firmware''' """
import os, requests

from src.component.file_content_base64data import FileContentBase64
from src.component.get_token import GetToken

class Firmware:
    """this class implements '''Create firmware''' '''Get firmware''' '''Delete firmware''' API"""
    rest_api_url = os.getenv('REST_API_URL')

    def create_firmware(
        self, firmware_type, version_number, file_name, comment, sas_url
    ):
        """This function implements '''Create firmware''' API"""
        print("inside create_firmware")
        rest_api_url =  os.getenv('REST_API_URL')
        url = f"{rest_api_url}/firmwares?grant_type=client_credentials"  # Base url with end point
        token = "Bearer "+GetToken().get_token().json()["access_token"]  # fetching the token
        data = {  # request body of the Create Firmware API
            "firmware_type": firmware_type,
            "version_number": version_number,
            "comment": comment,
            "file_name": file_name,
            "file_content": FileContentBase64().file_content_base64data(
                sas_url
            ),
        }
        # check if the firmware already exists
        get_firmware = self.get_firmware(firmware_type, version_number)
        if get_firmware.status_code == 200:
            # delete the firmware if it is already exists
            self.delete_firmware(firmware_type, version_number)
        response = requests.post(
            url,
            headers={"authorization": token},
            json=data,
            timeout=30,  # sending request to the server
        )
        return response  # returning the response

    def get_firmwares(self):
        """This function implements '''Get firmwares''' API"""
        rest_api_url = os.getenv('REST_API_URL')
        url = f"{rest_api_url}/firmwares?grant_type=client_credentials" # Base url with end point
        token = "Bearer "+GetToken().get_token().json()["access_token"] # fetching the token
        res_dev = requests.get(url, headers={"authorization": token}, timeout=30) # sending request to the server
        return res_dev # returning the response

    def get_firmware_id(self, description):
        """This function implements '''Get firmware id with comment''' API"""
        response = self.get_firmwares()
        if response.status_code == 200 and "firmwares" in response.json():
            firmwares = response.json()["firmwares"]
        else:
            return False
        for firmware in firmwares:
            if firmware["description"] == description:
                return firmware["firmware_id"]
        return False

    def get_firmware(self, firmware_type, version_number):
        """This function implements '''Get firmware''' API"""
        url = f"{self.rest_api_url}/firmwares/{firmware_type}/\
{version_number}?grant_type=client_credentials"  # Base url with end point
        token = "Bearer "+GetToken().get_token().json()["access_token"]  # fetching the token
        # sending request to the server
        response = requests.get(
            url, headers={"authorization": token}, timeout=30
        )
        return response  # returning the response

    def delete_firmware(self, firmware_type, version_number):
        """This function implements '''Delete firmware''' API"""
        url = f"{self.rest_api_url}/firmwares/{firmware_type}/\
{version_number}?grant_type=client_credentials"  # Base url with end point
        token = "Bearer "+GetToken().get_token().json()["access_token"]  # fetching the token
        # sending request to the server
        response = requests.delete(
            url, headers={"authorization": token}, timeout=30
        )
        return response  # returning the response
