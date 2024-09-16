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
from marshmallow import EXCLUDE, Schema, ValidationError, fields

from src.config_parser import ConfigParser


class Error_Schema_class(Schema):
    """This class will have the schema fields of Negative status codes"""

    result = fields.Str(
        strict=True, required=True, validate=lambda value: value in (["ERROR"])
    )
    code = fields.Str(strict=True, required=True)
    message = fields.Str(
        strict=True, required=True, validate=lambda value: value in ([message])
    )


class NegativeSchemaValidation:
    """This class having a method to invoke Negative schema validation
        and also to read the constant from YAML file"""

    def __init__(self):
        """Initialize a new instance of Negative SchemaValidation"""
        self.get_deploy_configuration = (
            []
        )  # taking an empty list to store the response

    def negative_schema(self, api_name, actual_response, status_code):
        """This method will validate parameters in the negative schema"""
        try:
            global message
            message = ConfigParser()._message(api_name, status_code)
            self.get_deploy_configuration.append(actual_response)
            Error_Schema_class(many=True).load(
                self.get_deploy_configuration, unknown=EXCLUDE
            )
            return True
        except ValidationError as err:
            return err
