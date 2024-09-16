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
# pylint:disable=line-too-long
# pylint:disable=R0913
"""This module implements all the API's related to '''Configuration''' """

import os
from timeit import default_timer as timer

import requests

from src.component.get_token import GetToken


class Deploy:
    """This class implements Deploy APIs"""

    def __init__(self):
        """This constructor initializes the base url"""
        self.REST_API_URL = os.getenv(
            "REST_API_URL"
        )  # Azure Blob Storage common.json

    def create_deploy_configuration(
        self,
        config_id,
        sensor_loader_version_number,
        sensor_version_number,
        ap_fw_version_number,
        model_id,
    ):
        """This method implements '''Create deploy configuration''' API"""

        get_config = self.get_deploy_configuration(
            config_id
        )  # fetch the config id
        if get_config.status_code == 200:
            response = self.delete_deploy_configuration(
                config_id
            )  # delete if config id is already present
        url = f"{self.REST_API_URL}/deployconfigurations?grant_type=client_credentials&config_id={config_id}&ap_fw_version_number={ap_fw_version_number}&sensor_version_number={sensor_version_number}&model_id={model_id}&sensor_loader_version_number={sensor_loader_version_number}"  # Base url with end point
        token = "Bearer "+GetToken().get_token().json()["access_token"]  # fetching the token
        response = requests.post(
            url, headers={"authorization": token}, timeout=30
        )  # sending request to the server
        return response

    def delete_deploy_configuration(self, config_id):
        """This method implements '''Delete deploy configuration''' API"""
        url = f"{self.REST_API_URL}/deployconfigurations/{config_id}?grant_type=client_credentials"  # Base url with end point
        token = "Bearer "+GetToken().get_token().json()["access_token"]  # fetching the token
        response = requests.delete(
            url, headers={"authorization": token}, timeout=30
        )  # sending request to the server
        return response  # returning the response

    def get_deploy_configuration(self, config_id):
        """This method implements '''Get deploy configuration''' API"""
        url = f"{self.REST_API_URL}/deployconfigurations/{config_id}?grant_type=client_credentials"  # Base url with end point
        token = "Bearer "+GetToken().get_token().json()["access_token"]  # fetching the token
        response = requests.get(
            url, headers={"authorization": token}, timeout=30
        )  # sending request to the server
        return response  # returning the response

    def deploy_by_configuration(self, config_id, device_id):
        """This method implements '''Deploy by configuration''' API"""
        url = f"{self.REST_API_URL}/deployconfigurations/{config_id}?grant_type=client_credentials&device_ids={device_id}"  # Base url with end point
        token = "Bearer "+GetToken().get_token().json()["access_token"]  # fetching the token
        response = requests.put(
            url,
            headers={"authorization": token},
            timeout=30,  # sending request to the server
        )
        return response  # returning the response

    def get_deploy_history(self, device_id):
        """This method implements '''Get deploy history''' API"""
        url = f"{self.REST_API_URL}/devices/{device_id}/deploys?grant_type=client_credentials"  # Base url with end point
        token = "Bearer "+GetToken().get_token().json()["access_token"]  # fetching the token
        response = requests.get(
            url, headers={"authorization": token}, timeout=30
        )  # sending request to the server
        return response  # returning the response

    def deployment_status_check(self, device_id):
        """This method is used to check the deploy status"""
        # call this for 3 times if the deployment is not happened in 20 mins
        start_time = timer()  # start the timer
        deploy_status = None
        while (
            deploy_status != "1"
        ):  # wait for the deployment to complete within 20 minutes
            response = self.get_deploy_history(
                device_id
            )  # fetch the deploy history
            response_data = response.json()
            deploy_status = response_data["deploys"][0][
                "deploy_status"
            ]  # fetch the deploy status
            deploy_id = response_data["deploys"][0][
                "id"
            ]  # fetch the deploy id
            end_time = timer()
            total_time = (
                end_time - start_time
            ) / 60  # total time to deploy in minutes
            if total_time > 20:
                self.cancel_deployment(
                    device_id, deploy_id
                )  # cancel the deployment if it is taking more than 20 minutes
                break
            if deploy_status == "3":
                break
        return deploy_status

    def cancel_deployment(self, device_id, deploy_id):
        """This method is used to cancel the deployment"""
        url = f"{self.REST_API_URL}/devices/{device_id}/deploys/{deploy_id}?grant_type=client_credentials"
        token = "Bearer "+GetToken().get_token().json()["access_token"]
        response = requests.put(
            url, headers={"authorization": token}, timeout=30
        )
        return response

    def undeploy_model(self, device_id, model_id):
        """This method is used for undeploying the model"""
        url = f"{self.REST_API_URL}/devices/{device_id}/models/{model_id}"
        token = "Bearer "+GetToken().get_token().json()["access_token"]
        response = requests.delete(
            url, headers={"authorization": token}, timeout=30
        )
        return response
