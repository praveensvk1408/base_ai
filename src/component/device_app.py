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
"""This module implements all the API's related to '''Edge App''' """
import os, time
from timeit import default_timer as timer

import requests

from src.component.file_content_base64data import FileContentBase64
from src.component.get_token import GetToken


class DeviceApp:
    """this class implements Train Model API"""

    def __init__(self):
        """This constructor initializes the base url"""
        self.REST_API_URL = os.getenv(
            "REST_API_URL"
        )  # Azure Blob Storage common.json

    def import_device_app(self, 
                          app_name="",
                          app_version=0,
                          description="",
                          file_name="",
                          entry_point="ppl",
                          compiled_flag="0",
                          file_content=""):
        """This function implements '''ImportEdgeApp''' API"""
        # Base url with end pointfile:///device_apps
        url = f"{self.REST_API_URL}/device_apps?grant_type=client_credentials"
        token = "Bearer "+GetToken().get_token().json()["access_token"]  # fetching the token
        app_content = FileContentBase64().file_content_base64data(file_content)
        req_data = {  # request body of theImport base Model API
                "compiled_flg": compiled_flag,
                "entry_point": entry_point,
                "app_name": app_name,
                "version_number": app_version,
                "comment": description,
                "file_name": file_name,
                "file_content": app_content
        }
        get_edge_apps = (
            self.get_edge_apps().json()
        )  # check if the model already exists
        if "apps" in get_edge_apps:
            for item in get_edge_apps["apps"]:
                if item["name"] == app_name:
                    self.delete_edge_app(app_name, app_version)
        response = requests.post(
            url,
            headers={"authorization": token},
            json=req_data,
            timeout=30,  # sending request to the server
        )
        print("response", response.json())
        return response

    def get_edge_apps(self):
        """This function implements GetEdgeApps API"""
        # Base url with end point
        url = f"{self.REST_API_URL}/device_apps?grant_type=client_credentials"
        token = "Bearer "+GetToken().get_token().json()["access_token"]  # fetching the token
        # sending request to the server
        response = requests.get(
            url, headers={"authorization": token}, timeout=30
        )
        return response  # returning the response

    def get_edge_app(self, app_name, app_version):
        """This function implements GetEdgeApps API"""
        # Base url with end point
        url = f"{self.REST_API_URL}/device_apps/{app_name}/{app_version}?\
            grant_type=client_credentials"
        token = "Bearer "+GetToken().get_token().json()["access_token"]  # fetching the token
        # sending request to the server
        response = requests.get(
            url, headers={"authorization": token}, timeout=30
        )
        return response  # returning the response

    def edge_app_status_check(self, app_name, app_version):
        """This function implements GetEdgeApp Status Check"""
        start_time = timer()  # start the timer
        status = None
        while (
            status != "2"
        ):  # wait for the publish model to complete within 10 minutes
            response = self.get_edge_app(
                app_name, app_version
            )
            if response.status_code == 200:
                response_data = response.json()
                status = response_data["status"]
            end_time = timer()
            total_time = (
                end_time - start_time
            ) / 60  # total time to deploy in minutes
            if total_time > 10:
                return "Time out"
            time.sleep(10)
        return status  # returning the response

    def delete_edge_app(self, app_name, app_version):
        """This function implements '''DeleteEdgeApp''' API"""
        # Base url with end point
        url = f"{self.REST_API_URL}/device_apps/{app_name}/{app_version}?grant_type=client_credentials"
        token = "Bearer "+GetToken().get_token().json()["access_token"]  # fetching the token
        # sending request to the server
        response = requests.delete(
            url, headers={"authorization": token}, timeout=30
        )
        return response  # returning the response
    
    def deploy_edge_app(self, app_name, app_version, device_id):
        """This function implements '''DeployEdgeApp''' API"""
        # Base url with end point
        url = f"{self.REST_API_URL}/device_apps_deploys?grant_type=client_credentials"
        token = "Bearer "+GetToken().get_token().json()["access_token"]
        req_data = {  # request body of theImport base Model API
                "app_name": app_name,
                "version_number": app_version,
                "device_ids": device_id,
        }
        response = requests.post(
            url,
            headers={"authorization": token},
            json=req_data,
            timeout=30,  # sending request to the server
        )
        return response
    
    def get_deployed_edge_app_status(self,app_name, version_number):
        """This function implements GetDeployedEdgeApps API"""
        # Base url with end point
        start_time = timer()
        status = None
        while (
            status != "1"
        ):
            response = self.get_deployed_edge_app(app_name, version_number)
            if response.status_code == 200:
                response_data = response.json()
                status = response_data["deploys"][0]["total_status"]
            end_time = timer()
            total_time = (
                end_time - start_time
            ) / 60
            if total_time > 20:
                return "Time out"
            time.sleep(10)
        return status
    
    def get_deployed_edge_app(self, app_name, version_number):
        url = f"{self.REST_API_URL}/device_apps/{app_name}/{version_number}/deploys?grant_type=client_credentials"
        token = "Bearer "+GetToken().get_token().json()["access_token"]
        response = requests.get(
            url, headers={"authorization": token}, timeout=30
        )
        return response
