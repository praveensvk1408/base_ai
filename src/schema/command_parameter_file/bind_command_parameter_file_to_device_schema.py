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

from marshmallow import EXCLUDE, Schema, ValidationError, fields


class BindCommandParameterFileToDeviceSchema(Schema):
    """This class will have the schema fields of
    Bind Command Parameter File To Device API"""

    result = fields.Str(strict=True, required=True)


class BindCommandParameterFileToDeviceSchemaValidation:
    """This class having a method to invoke Bind Command Parameter File
    To Device schema validation"""

    def __init__(self):
        """Initialize a new instance of SchemaValidation
        :param Bind Command Parameter File To Device: Will store response
        """
        self.bind_command_parameter_file_to_device = []
        # taking an empty list to store the response

    def bind_command_parameter_file_to_device_schema(self, response):
        """This method will validate parameters in
        Bind Command Parameter File To Device"""
        try:  # using try except blocks for validation purpose
            self.bind_command_parameter_file_to_device.append(
                response
            )  # appending the response to the list
            # Deserialize and validate the input data using the schema
            BindCommandParameterFileToDeviceSchema(many=True).load(
                self.bind_command_parameter_file_to_device,
                unknown=EXCLUDE,  # loading the response
            )
            return True  # if schema comparsion passes returns true
        except ValidationError as err:
            return err  # if schema comparsion fails returns error
