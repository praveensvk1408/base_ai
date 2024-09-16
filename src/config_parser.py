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
# pylint: disable=broad-except

"""ConfigParser"""
import yaml
import os

EXE_DIR = os.path.dirname(__file__)

class ConfigParser:
    """This will read the constant from YAML file"""

    def __init__(self):
        """constructor"""
        self.config_file_path = (
            EXE_DIR + "/config.yaml"
        )
        self.config_data = None
        self._read_config_file()

    def _read_config_file(self):
        """
        Read config file
        """
        with open(self.config_file_path, "r", encoding="utf-8") as file:
            self.config_data = yaml.safe_load(file)

    def _message(self, api, status_code):
        """Returns the get_deploy_configurations_status_code
        from YAML config data"""
        try:
            return self.config_data[api][status_code]["message"]
        except (ValueError, Exception) as ex:
            print(str(ex))
            return None
