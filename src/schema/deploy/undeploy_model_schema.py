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


class UndeployModel(Schema):
    """This class will validate parameters in undeply Configuration"""

    result = fields.Str(required=True)


class UndeployModelSchemaValidation:
    """The class SchemaValidation is for validating schema for
    UndeployModelSchemaValidation"""

    def __init__(self):
        """Initialize a new instance of SchemaValidation
        :param undeploy_model: Will store response
        """
        self.undeploy_model = []

    def undeploy_model_positive_schema(self, response):
        """This function is for validating with positive response"""
        # Implementation of schema
        try:
            # try block that may raise an exception
            self.undeploy_model.append(response)  # appending the response
            # Deserialize and validate the input data using the schema
            UndeployModel(many=True).load(self.undeploy_model, unknown=EXCLUDE)
            return True
        except ValidationError as err:
            # Handle the exception that has been raised
            return err
