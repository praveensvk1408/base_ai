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
# pylint: disable=line-too-long
"""This module implements all the API's related to '''Configuration''' """

import os
import time
from timeit import default_timer as timer

import requests
from src.component.get_token import GetToken

class Configuration:
    """This class implements all the '''create_deploy_configuration'''  '''delete_deploy_configuration''' '''get_deploy_configuration''' '''deploy_by_configuration''' '''get_deploy_history''' API"""

    def create_deploy_configuration(
        self,
        config_id,
        models=[],
        edge_system_sw_package={},
        edge_apps=[],
    ):
        """This function implements '''Create deploy configuration''' API"""
        data = {  # request body of the Create Configuration API
            "config_id": config_id,
            "models": models,
            "edge_system_sw_package": edge_system_sw_package,
            "edge_apps": edge_apps,
        }
        get_config = self.get_deploy_configuration(config_id)  # fetch the config id
        if get_config.status_code == 200:
            self.delete_deploy_configuration(
                config_id
            )  # delete if config id is already present
        REST_API_URL = os.getenv("REST_API_URL")  # Azure Blob Storage common.json
        url = f"{REST_API_URL}/deploy_configs?grant_type=client_credentials"  # Base url with end point
        token = "Bearer "+GetToken().get_token().json()["access_token"]  # fetching the token
        response = requests.post(
            url,
            headers={"authorization": token}, 
            json=data,            
            timeout=30
        )  # sending request to the server
        return response

    def delete_deploy_configuration(self, config_id):
        """This function implements '''Delete deploy configuration''' API"""
        REST_API_URL = os.getenv("REST_API_URL")  # Azure Blob Storage common.json
        url = f"{REST_API_URL}/deploy_configs/{config_id}?grant_type=client_credentials"  # Base url with end point
        token = "Bearer "+GetToken().get_token().json()["access_token"]  # fetching the token
        res_dev = requests.delete(
            url, headers={"authorization": token}, timeout=30
        )  # sending request to the server
        return res_dev  # returning the response

    def get_deploy_configuration(self, config_id):
        """This function implements '''Get deploy configuration''' API"""
        REST_API_URL = os.getenv("REST_API_URL")  # Azure Blob Storage common.json
        url = f"{REST_API_URL}/deploy_configs/{config_id}?grant_type=client_credentials"  # Base url with end point
        token = "Bearer "+GetToken().get_token().json()["access_token"]  # fetching the token
        res_dev = requests.get(
            url, headers={"authorization": token}, timeout=30
        )  # sending request to the server
        return res_dev  # returning the response

    def deploy_by_configuration(self, config_id, device_id):
        """This function implements '''Deploy by configuration''' API"""
        REST_API_URL = os.getenv("REST_API_URL")  # Azure Blob Storage common.json
        url = f"{REST_API_URL}/deploy_configs/{config_id}/apply?grant_type=client_credentials&device_ids={device_id}"  # Base url with end point
        token = "Bearer "+GetToken().get_token().json()["access_token"]  # fetching the token
        data = {  # request body of deploy_by_configuration API
            "device_ids" : [device_id]
        }
        res_dev = requests.post(
            url,
            headers={"authorization": token},
            json=data,
            timeout=60,  # sending request to the server
        )
        return res_dev  # returning the response

    def get_deploy_history(self, device_id):
        """This function implements '''Get deploy history''' API"""
        REST_API_URL = os.getenv("REST_API_URL")  # Azure Blob Storage common.json
        url = f"{REST_API_URL}/devices/{device_id}/deploys?grant_type=client_credentials"  # Base url with end point
        token = "Bearer "+GetToken().get_token().json()["access_token"]  # fetching the token
        try:
            res_dev = requests.get(
                url, headers={"authorization": token}, timeout=150
            )  # sending request to the server
        except requests.exceptions.ReadTimeout:
            print("Deploy History API Timeout, Retry")
            res_dev = requests.get(
                url, headers={"authorization": token}, timeout=150
            )  # sending request to the server
        return res_dev  # returning the response

    def deployment_status_check(self, device_id):
        """This method is used to check the deploy status"""
        # call this for 3 times if the deployment is not happened in 20 mins
        start_time = timer()  # start the timer
        deploy_status = None
        while (
            deploy_status != "success"
        ):  # wait for the deployment to complete within 20 minutes
            response = self.get_deploy_history(device_id)  # fetch the deploy history
            if response.status_code == 200:
                response_data = response.json()
                deploy_status = response_data["deploys"][0][
                    "deploy_status"
                ]  # fetch the deploy status
                deploy_id = response_data["deploys"][0]["deploy_id"]  # fetch the deploy id
            end_time = timer()
            total_time = (end_time - start_time) / 60  # total time to deploy in minutes
            if total_time > 20:
                self.cancel_deployment(
                    device_id, deploy_id
                )  # cancel the deployment if it is taking more than 20 minutes
                break
            elif  response.status_code == 200 and deploy_status == "fail":
                break
            time.sleep(10)
        return deploy_status

    def cancel_deployment(self, device_id, deploy_id):
        """This method is used to cancel the deployment"""
        REST_API_URL = os.getenv("REST_API_URL")  # Azure Blob Storage common.json
        url = f"{REST_API_URL}/devices/{device_id}/deploys/{deploy_id}/cancel?grant_type=client_credentials"
        token = "Bearer "+GetToken().get_token().json()["access_token"]
        res_dev = requests.post(url, headers={"authorization": token}, timeout=150)
        return res_dev
