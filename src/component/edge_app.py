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

from src.component.get_token import GetToken


class EdgeApp:
    """this class implements Train Model API"""

    def __init__(self):
        """This constructor initializes the base url"""
        self.REST_API_URL = os.getenv(
            "REST_API_URL"
        )  # Azure Blob Storage common.json

    def import_edge_app(self, edge_app_package_id, 
                          app_name="",
                          app_version=0,
                          description=""):
        """This function implements '''ImportEdgeApp''' API"""
        # Base url with end point
        url = f"{self.REST_API_URL}/edge_apps?grant_type=client_credentials"
        token = "Bearer "+GetToken().get_token().json()["access_token"]  # fetching the token
        req_data = {  # request body of theImport base Model API
            "edge_app_package_id": edge_app_package_id,
            "app_name": app_name,
            "description": description,
        }
        get_edge_apps = (
            self.get_edge_apps().json()
        )  # check if the model already exists
        if "apps" in get_edge_apps:
            for item in get_edge_apps["apps"]:
                if item["app_name"] == app_name:
                    self.delete_edge_app(app_name, app_version)
        response = requests.post(
            url,
            headers={"authorization": token},
            json=req_data,
            timeout=30,  # sending request to the server
        )
        return response

    def get_edge_apps(self):
        """This function implements GetEdgeApps API"""
        # Base url with end point
        url = f"{self.REST_API_URL}/edge_apps?grant_type=client_credentials"
        token = "Bearer "+GetToken().get_token().json()["access_token"]  # fetching the token
        # sending request to the server
        response = requests.get(
            url, headers={"authorization": token}, timeout=30
        )
        return response  # returning the response

    def get_edge_app(self, app_name, app_version):
        """This function implements GetEdgeApps API"""
        # Base url with end point
        url = f"{self.REST_API_URL}/edge_apps/{app_name}/{app_version}?\
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
            status != "compiled"
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
        url = f"{self.REST_API_URL}/edge_apps/{app_name}/{app_version}?grant_type=client_credentials"
        token = "Bearer "+GetToken().get_token().json()["access_token"]  # fetching the token
        # sending request to the server
        response = requests.delete(
            url, headers={"authorization": token}, timeout=30
        )
        return response  # returning the response
