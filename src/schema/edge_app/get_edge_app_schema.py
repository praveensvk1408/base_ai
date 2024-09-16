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

class GetEdgeAppSchema(Schema):
    """This class will have the schema fields of Get EdgeApp"""

    app_name = fields.Str(strict=True, required=True)
    app_version = fields.Str(strict=True, required=True)
    compiled_flg = fields.Bool(strict=True, required=True)
    deploy_count = fields.Int(strict=True, required=True)
    description = fields.Str(strict=True, required=True)
    ins_date = fields.DateTime(strict=True, required=True)
    ins_id = fields.Str(strict=True, required=True)
    root_dtmi = fields.Str(strict=True, required=True)
    status = fields.Str(strict=True, required=True)
    upd_date = fields.DateTime(strict=True, required=True)
    upd_id = fields.Str(strict=True, required=True)

class GetEdgeAppSchemaValidation:
    """This class having a method to invoke Get EdgeApp schema validation"""

    def __init__(self):
        """Initialize a new instance of SchemaValidation
        :param Get Firmware: Will store response
        """
        self.get_edge_app = []  # taking an empty list to store the response

    def get_edge_app_positive_schema(self, response):
        """This method will validate parameters in Get EdgeApp"""
        try:  # using try except blocks for validation purpose
            self.get_edge_app.append(
                response
            )  # appending the response to the list
            # Deserialize and validate the input data using the schema
            GetEdgeAppSchema(many=True).load(
                self.get_edge_app, 
                unknown=EXCLUDE,
            )  # loading the response
            return True  # if schema comparsion passes returns true
        except ValidationError as err:
            return err  # if schema comparsion fails returns error
