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


class StartUploadInferenceResultSchema(Schema):
    """This class will have the schema fields of \
        StartUploadInferenceResultSchemaValidation  File API"""

    result = fields.Str(strict=True, required=True)
    outputSubDirectory = fields.Str(
        strict=False, required=False, allow_None=True
    )
    outputSubDirectoryIR = fields.Str(
        strict=False, required=False, allow_None=True
    )


class StartUploadInferenceResultSchemaValidation:
    """This class having a method to invoke  \
    StartUploadInferenceResultSchemaValidation File schema validation"""

    def __init__(self):
        """Initialize a new instance of SchemaValidation"""
        self.start_upload_inference_result = (
            []
        )  # taking an empty list to store the response

    def start_upload_inference_result_schema(self, response):
        """This method will validate parameters
        in start_upload_inference_result_schema"""
        try:  # using try except blocks for validation purpose
            self.start_upload_inference_result.append(
                response
            )  # appending the response to the list
            # Deserialize and validate the input data using the schema
            StartUploadInferenceResultSchema(many=True).load(
                self.start_upload_inference_result,
                unknown=EXCLUDE,  # loading the response
            )
            return True  # if schema comparsion passes returns true
        except ValidationError as err:
            return err  # if schema comparsion fails returns error
