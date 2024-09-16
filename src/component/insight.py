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
"""This module implements all the API's related to '''Insight''' """
import os
import time

import requests

from src.component.get_token import GetToken

class Insight:
    """this class implements Insight API"""

    def __init__(self):
        """This constructor initializes the base url"""
        self.REST_API_URL = os.getenv(
            "REST_API_URL"
        )  # Azure Blob Storage common.json

    # def get_image_directories(self):
    #     """This function implements '''GetImageDirectories''' API"""
    #     # Base url with end point
    #     url = f"{self.REST_API_URL}/images/devices/directories?grant_type=client_credentials"
    #     token = "Bearer "+GetToken().get_token().json()["access_token"]  # fetching the token
    #     response = requests.get(
    #         url,
    #         headers={"authorization": token},
    #         timeout=60,  # sending request to the server
    #     )
    #     return response
    
    def get_inference_results(self, device_id):
        """This method is used to get the inference results"""
        url = f"{self.rest_api_url}/devices/{device_id}/inferenceresults?grant_type=client_credentials&raw=1"
        token = GetToken().get_token()
        response = requests.get(
            url, headers={"authorization": token}, timeout=30
        )
        return response
    
    def get_images(self, device_id, sub_directory_name):
        """This function implements '''GetImages''' API"""
        # Base url with end point
        url = f"{self.REST_API_URL}/images/devices/{device_id}/directories/{sub_directory_name}?limit=256&grant_type=client_credentials"
        token = "Bearer "+GetToken().get_token().json()["access_token"]  # fetching the token
        response = requests.get(
            url,
            headers={"authorization": token},
            timeout=60,  # sending request to the server
        )
        return response
    
    def get_images_of_next_page(self, device_id, sub_directory_name, continuation_token:str):
        """This function implements '''GetImages''' API, with continuation token to get next portion of images"""
        # Base url with end point
        url = f"{self.REST_API_URL}/images/devices/{device_id}/directories/{sub_directory_name}?limit=256&starting_after={continuation_token}&grant_type=client_credentials"
        token = "Bearer "+GetToken().get_token().json()["access_token"]  # fetching the token
        response = requests.get(
            url,
            headers={"authorization": token},
            timeout=60,  # sending request to the server
        )
        return response

    def get_images_of_last_page(self, device_id, sub_directory_name):
        """This function implements '''GetImages''' API, keep fetching until nothing to fetch"""
        try:
            res = self.get_images(device_id, sub_directory_name)
            while True:
                payload = res.json()
                # get continuation_token
                continuation_token = payload["continuation_token"]
                print(f"continuation token: {continuation_token}")
                # "continuation_token" wil be None, if there is no more images to fetch.
                if continuation_token is None:
                    return res

                print(f"fetch next images")
                # fetch next portion of images with continuation_token
                res = self.get_images_of_next_page(device_id, sub_directory_name, continuation_token)
                # sleep in order to reduce workloads to server.
                time.sleep(2)
        except KeyError as e:
            print(f"get_images_of_last {e}")
            raise KeyError(e)
        except Exception as e:
            print(f"get_images_of_last {e}")
            raise Exception(e)

    def get_inference_results(self, device_id):
        """This function implements '''GetInferenceResults''' API"""
        # Base url with end point
        url = f"{self.REST_API_URL}/inferenceresults/devices/{device_id}?grant_type=client_credentials"
        token = "Bearer "+GetToken().get_token().json()["access_token"]  # fetching the token
        response = requests.get(
            url,
            headers={"authorization": token},
            timeout=60,  # sending request to the server
        )
        return response

    def get_inference_result(self, device_id, id):
        """This function implements '''GetInferenceResult''' API"""
        # Base url with end point
        url = f"{self.REST_API_URL}/inferenceresults/devices/{device_id}/{id}?grant_type=client_credentials"
        token = "Bearer "+GetToken().get_token().json()["access_token"]  # fetching the token
        response = requests.get(
            url,
            headers={"authorization": token},
            timeout=60,  # sending request to the server
        )
        return response