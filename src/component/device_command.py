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
"""This module implements all the API's related to '''Device Command''' """
import os

import requests

from src.component.get_token import GetToken

class DeviceCommand:
    """this class implements Utility API"""

    def __init__(self):
        """This constructor initializes the base url"""
        self.REST_API_URL = os.getenv(
            "REST_API_URL"
        )  # Azure Blob Storage common.json

    def execute_command(self, device_id, module_id, command_name, parameters={}):
        """This function implements '''ExecuteCommand''' API"""
        # Base url with end point
        url = f"{self.REST_API_URL}/devices/{device_id}/modules/{module_id}/command?grant_type=client_credentials"
        token = "Bearer "+GetToken().get_token().json()["access_token"]  # fetching the token
        req_data = {  # request body of UploadFile API
            "command_name": command_name,
        }
        if parameters != {}:
            req_data["parameters"] = parameters
        try:
            response = requests.post(
                url,
                headers={"authorization": token},
                json=req_data,
                timeout=60,  # sending request to the server
            )
        except requests.exceptions.ReadTimeout:
            response = requests.post(
                url,
                headers={"authorization": token},
                json=req_data,
                timeout=60,  # sending request to the server
            )
        return response

    def update_configuration(self, device_id, module_id, configuration):
        """This function implements '''UpdateConfiguration''' API"""
        # Base url with end point
        url = f"{self.REST_API_URL}/devices/{device_id}/modules/{module_id}?grant_type=client_credentials"
        token = "Bearer "+GetToken().get_token().json()["access_token"]  # fetching the token
        try:
            response = requests.patch(
                url,
                headers={"authorization": token},
                json=configuration,
                timeout=60,  # sending request to the server
            )
        except requests.exceptions.ReadTimeout:
            response = requests.patch(
                url,
                headers={"authorization": token},
                json=configuration,
                timeout=60,  # sending request to the server
            )
        return response
    
    def start_upload_inference_result(self,device_id):
        """This function implements '''StartUploadInferenceResult''' API"""
        # Base url with end point
        url = f"{self.REST_API_URL}/devices/{device_id}/inferenceresults/collectstart?grant_type=client_credentials"
        token = "Bearer "+GetToken().get_token().json()["access_token"]
        try:
            response = requests.post(
                url,
                headers={"authorization": token},
                timeout=60,  # sending request to the server
            )
        except requests.exceptions.ReadTimeout:
            response = requests.post(
                url,
                headers={"authorization": token},
                timeout=60,  # sending request to the server
            )
        return response
    
    def stop_upload_inference_result(self,device_id):
        """This function implements '''StopUploadInferenceResult''' API"""
        # Base url with end point
        url = f"{self.REST_API_URL}/devices/{device_id}/inferenceresults/collectstop?grant_type=client_credentials"
        token = "Bearer "+GetToken().get_token().json()["access_token"]
        try:
            response = requests.post(
                url,
                headers={"authorization": token},
                timeout=60,  # sending request to the server
            )
        except requests.exceptions.ReadTimeout:
            response = requests.post(
                url,
                headers={"authorization": token},
                timeout=60,  # sending request to the server
            )
        return response
    