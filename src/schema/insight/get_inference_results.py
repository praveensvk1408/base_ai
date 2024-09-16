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


class InferencesSchema(Schema):
    """This class validate parameters in the Inference schema fields"""

    T = fields.Str(strict=False, required=False)
    O = fields.Str(strict=False, required=False)


class InferencesSchema2(Schema):
    """This class validate parameters in the Inference schema fields"""

    T = fields.Str(strict=False, required=False)
    O = fields.Str(strict=False, required=False)


class InferenceResultSchema(Schema):
    """This class validate parameters in the Inferenceresult schema fields"""

    DeviceID = fields.Str(strict=False, required=False)
    ModelID = fields.Str(strict=False, required=False)
    Image = fields.Boolean(strict=False, required=False)
    Inferences = fields.List(
        fields.Nested(InferencesSchema, unknown=EXCLUDE, allow_none=False)
    )
    id = fields.Str(strict=False, required=False)
    tt1 = fields.Integer(strict=False, required=False)
    _rid = fields.Str(strict=False, required=False)
    _self = fields.Str(strict=False, required=False)
    _etag = fields.Str(strict=False, required=False)
    _attachments = fields.Str(strict=False, required=False)
    _ts = fields.Integer(strict=False, required=False)
    inferences = fields.List(
        fields.Nested(InferencesSchema2, unknown=EXCLUDE, allow_none=False)
    )


class GetInferenceResultSchema(Schema):
    """This class will have the schema fields of  GetInferenceResult"""

    id = fields.Str(strict=True, required=True)
    device_id = fields.Str(strict=True, required=True)
    model_id = fields.Str(strict=True, required=True)
    version_number = fields.Str(strict=True, required=True)
    model_version_id = fields.Str(strict=True, required=True)
    model_type = fields.Str(strict=True, required=True)
    training_kit_name = fields.Str(strict=True, required=True)
    _ts = fields.Integer(strict=True, required=True)
    inference_result = fields.Nested(
        InferenceResultSchema, unknown=EXCLUDE, allow_none=False
    )


class ListSchema(Schema):
    """This class will have the schema fields of Models"""

    fields.List(
        fields.Nested(
            GetInferenceResultSchema, unknown=EXCLUDE, allow_none=False
        )
    )


class GetInferenceResultValidationSchema:
    """This class having a method to invoke Import Base Model API validation"""

    def __init__(self):
        """Initialize a new instance of SchemaValidation"""
        self.get_inference_results = (
            []
        )  # taking an empty list to store the response

    def get_inference_results_positive_schema(self, response):
        """This method will validate parameters in Get inference results API"""
        try:  # using try except blocks for validation purpose
            self.get_inference_results.append(
                response
            )  # appending the response to the list
            # Deserialize and validate the input data using the schema
            ListSchema(many=True).load(
                self.get_inference_results, unknown=EXCLUDE
            )
            return True  # if schema comparsion passes returns true
        except ValidationError as err:
            return err  # if schema comparsion fails returns error
