# ------------------------------------------------------------------------
# Copyright 2022 Sony Semiconductor Solutions Corp. All rights reserved.
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
# pylint:disable=line-too-long

import os
import sys

import requests

from src.component.file_content_base64data import FileContentBase64
from src.component.get_token import GetToken

sys.path.append("../..")
# constant
DEVICE_IDS = os.getenv("device_id")


class CommandParameterFile:
    """This class implements the command parameter file API's"""

    def __init__(self):
        """This constructor initializes the base url"""
        self.REST_API_URL = os.getenv(
            "REST_API_URL"
        )  # Azure Blob Storage common.json

    def register_command_parameter_file(self, file_name, parameter):
        """This method is used to register the
        command paramter file to the Aitrios console"""
        # check if the command parameter file already exists
        get_command_param_file_name = self.get_command_parameter_file()
        get_command_param_file_name = get_command_param_file_name.json()
        get_command_param_file_name = get_command_param_file_name[
            "parameter_list"
        ][0]["file_name"]
        if get_command_param_file_name == file_name:
            # unbind the command parameter file
            self.unbind_command_parameter_file_to_device(
                get_command_param_file_name, DEVICE_IDS
            )
            # delete the firmware if it is already exists
            self.delete_command_parameter_file_to_device(file_name)
        url = f"{self.REST_API_URL}/command_parameter_files?grant_type=client_credentials"
        token = "Bearer "+GetToken().get_token().json()["access_token"]
        print(type(token))
        data = {
            "file_name": file_name,
            "parameter": FileContentBase64().file_content_base64data(
                parameter
            ),
        }
        response = requests.post(
            url, headers={"authorization": token}, json=data, timeout=30
        )
        return response

    def get_command_parameter_file(self):
        """This method is used to fetch the command paramter files from the Aitrios console"""
        url = f"{self.REST_API_URL}/command_parameter_files?grant_type=client_credentials"
        token = "Bearer "+GetToken().get_token().json()["access_token"]
        response = requests.get(
            url, headers={"authorization": token}, timeout=30
        )
        return response

    def bind_command_parameter_file_to_device(
        self,
        bind_cmd_param_file,
        device_ids,
    ):
        """This method is used to bind the command paramter files
        to the specified device"""
        url = f"{self.REST_API_URL}/devices/configuration/command_parameter_files/{bind_cmd_param_file}?grant_type=client_credentials"
        token = "Bearer "+GetToken().get_token().json()["access_token"]
        data = {"device_ids": device_ids}
        get_command_param_file = self.get_command_parameter_file().json()
        for item in get_command_param_file["parameter_list"]:
            file_name = item["file_name"]
            if len(item["device_ids"]) != 0:
                self.unbind_command_parameter_file_to_device(
                    file_name, device_ids
                )
        response = requests.put(
            url, headers={"authorization": token}, json=data, timeout=30
        )
        return response

    def unbind_command_parameter_file_to_device(
        self,
        unbind_command_parameter_file_name,
        device_ids,
    ):
        """This method is used to bind the
        command paramter files to the specified device"""
        url = f"{self.REST_API_URL}/devices/configuration/command_parameter_files/{unbind_command_parameter_file_name}?grant_type=client_credentials"
        token = "Bearer "+GetToken().get_token().json()["access_token"]
        data = {"device_ids": device_ids}
        response = requests.delete(
            url, headers={"authorization": token}, json=data, timeout=30
        )
        return response

    def delete_command_parameter_file_to_device(
        self,
        command_parameter_file_name,
    ):
        """This method is used to delete the command paramter files from the Aitrios console"""
        url = f"{self.REST_API_URL}/command_parameter_files/{command_parameter_file_name}?grant_type=client_credentials"
        token = "Bearer "+GetToken().get_token().json()["access_token"]
        response = requests.delete(
            url, headers={"authorization": token}, timeout=30
        )
        return response
