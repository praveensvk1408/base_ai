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

"""This module implements base64 conversion"""

import base64

import requests


class FileContentBase64:
    """This class implements base64 conversion"""

    def file_content_base64data(self, sas_url):
        """This method is used to convert data into base64 format"""

        response = requests.get(sas_url, timeout=30)
        encoded_zip = base64.b64encode(response.content)
        file_base_64 = encoded_zip.decode()
        return file_base_64
