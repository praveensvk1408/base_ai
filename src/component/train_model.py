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
"""This module implements all the API's related to '''Train model''' """
import os, time
from timeit import default_timer as timer

import requests

from src.component.get_token import GetToken


class TrainModel:
    """this class implements Train Model API"""

    def __init__(self):
        """This constructor initializes the base url"""
        self.REST_API_URL = os.getenv(
            "REST_API_URL"
        )  # Azure Blob Storage common.json

    def import_base_model(self, model_id, 
                          model="",
                          file_id="",
                          converted="False",
                          network_type="1"):
        """This function implements '''Import base model''' API"""
        # Base url with end point
        print(f"model_id: {model_id}")
        url = f"{self.REST_API_URL}/models?grant_type=client_credentials"
        token = "Bearer "+GetToken().get_token().json()["access_token"]  # fetching the token
        if file_id != "":
            req_data = {  # request body of theImport base Model API
                "model_id": model_id,
                "model_file_id": file_id,
                "converted": converted,
                "network_type": network_type,
            }
        else:
            req_data = {  # request body of theImport base Model API
                "model_id": model_id,
                "model": model,
                "converted": converted,
                "network_type": network_type,
            }
        get_models = (
            self.get_models().json()
        )  # check if the model already exists
        for item in get_models["models"]:
            if item["model_id"] == model_id:
                print("Model already exists")
                self.delete_model(model_id)
        response = requests.post(
            url,
            headers={"authorization": token},
            json=req_data,
            timeout=30,  # sending request to the server
        )
        return response

    def get_models(self):
        """This function implements Get models API"""
        # Base url with end point
        url = f"{self.REST_API_URL}/models?grant_type=client_credentials"
        token = "Bearer "+GetToken().get_token().json()["access_token"]  # fetching the token
        # sending request to the server
        response = requests.get(
            url, headers={"authorization": token}, timeout=30
        )
        return response  # returning the response

    def publish_model(self, publish_model_id):
        """This function implements '''Publish model''' API"""
        # Base url with end point
        url = f"{self.REST_API_URL}/models/{publish_model_id}?grant_type=client_credentials"
        token = "Bearer "+GetToken().get_token().json()["access_token"]  # fetching the token
        response = requests.post(
            url,
            headers={"authorization": token},
            timeout=30,  # sending request to the server
        )
        return response

    def get_base_model_status(self, model_id):
        """This function implements Get Base Model Status API"""
        # Base url with end point
        url = f"{self.REST_API_URL}/models/{model_id}/base?grant_type=client_credentials"
        token = "Bearer "+GetToken().get_token().json()["access_token"]  # fetching the token
        # sending request to the server
        response = requests.get(
            url, headers={"authorization": token}, timeout=30
        )
        return response  # returning the response

    def publish_model_status_check(self, model_id):
        """This method checks publish model status"""
        # call this for 3 times if the publish model is not happened in 20 mins
        start_time = timer()  # start the timer
        model_status = None
        while (
            model_status != "Import completed"
        ):  # wait for the publish model to complete within 10 minutes
            response = self.get_base_model_status(
                model_id
            )  # fetch the deploy history
            if response.status_code == 200:
                response_data = response.json()
                model_status = response_data["projects"][0]["versions"][0][
                    "result"
                ]  # fetch the model status
            end_time = timer()
            total_time = (
                end_time - start_time
            ) / 60  # total time to deploy in minutes
            if total_time > 10:
                return "Time out"
            time.sleep(10)
        return model_status  # returning the response

    def delete_model(self, delete_model_model_id):
        """This function implements '''Delete model''' API"""
        # Base url with end point
        url = f"{self.REST_API_URL}/models/{delete_model_model_id}?grant_type=client_credentials"
        token = "Bearer "+GetToken().get_token().json()["access_token"]  # fetching the token
        # sending request to the server
        response = requests.delete(
            url, headers={"authorization": token}, timeout=30
        )
        return response  # returning the response

    # add method ImportBaseModel, support parameter input_format_param
    def import_base_model_setparam(self, model_id, format_param,
                          model="",
                          file_id="",
                          converted="False",
                          network_type="1"):
        """This function implements '''ImportBaseModel''' API with input_format_parameter"""
        # Base url with end point
        url = f"{self.REST_API_URL}/models?grant_type=client_credentials"
        token = "Bearer "+GetToken().get_token().json()["access_token"]  # fetching the token
        # print(f"url: {url}")
        if file_id != "":
            req_data = {  # request body of theImport base Model API
                "model_id": model_id,
                "model_file_id": file_id,
                "converted": converted,
                "network_type": network_type,
            }
        else:
            req_data = {  # request body of theImport base Model API
                "model": model,
                "model_id": model_id,
                "converted": converted,
                "network_type": network_type,
            }
        if format_param != "":
            add_entry = {
                "input_format_param": format_param,
            }
            req_data.update(add_entry)
        else:
            print('Error: format_param not set.')
        get_models = (
            self.get_models().json()
        )  # check if the model already exists
        # print(f"get_models: {get_models}")
        for item in get_models["models"]:
            if item["model_id"] == model_id:
                self.delete_model(model_id)
        response = requests.post(
            url,
            headers={"authorization": token},
            json=req_data,
            timeout=30,  # sending request to the server
        )
        return response
