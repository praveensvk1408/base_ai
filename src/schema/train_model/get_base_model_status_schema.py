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


class VersionSchema(Schema):
    """This class will have the Nested schema \
    fields of Get Base Model Status"""

    version_number = fields.Str(strict=True, required=True)
    iteration_id = fields.Str(strict=True, required=True)
    iteration_name = fields.Str(strict=True, required=True)
    accuracy = fields.Str(strict=True, required=True)
    model_performances = fields.Dict(
        strict=True, required=True, allow_none=True
    )
    latest_flg = fields.Str(strict=True, required=True)
    publish_latest_flg = fields.Str(strict=True, required=True)
    version_status = fields.Str(strict=True, required=True)
    org_file_name = fields.Str(strict=True, required=True)
    org_file_size = fields.Integer(strict=True, required=True)
    publish_file_name = fields.Str(strict=True, required=True)
    publish_file_size = fields.Integer(strict=True, required=True)
    model_file_size = fields.Integer(strict=True, required=True)
    model_framework = fields.Str(strict=True, required=True)
    conv_id = fields.Str(strict=True, required=True)
    labels = fields.List(fields.Str(strict=True, required=True))
    stage = fields.Str(strict=True, required=True)
    result = fields.Str(strict=True, required=True)
    kpi = fields.Dict(strict=True, required=True)
    converter_log = fields.List(fields.Dict(strict=False, required=False))
    convert_start_date = fields.Str(strict=False, required=False)
    convert_end_date = fields.Str(strict=False, required=False)
    publish_start_date = fields.Str(strict=False, required=False)
    publish_end_date = fields.Str(strict=False, required=False)
    version_comment = fields.Str(strict=False, required=False)
    version_ins_date = fields.Str(strict=False, required=False)
    version_upd_date = fields.Str(strict=False, required=False)


class ProjectSchema(Schema):
    """This class will have the Nested schema \
    fields of Get Base Model Status"""

    model_project_name = fields.Str(strict=True, required=True)
    model_project_id = fields.Str(strict=True, required=True)
    model_platform = fields.Str(strict=True, required=True)
    model_type = fields.Str(strict=True, required=True)
    project_type = fields.Str(strict=True, required=True)
    dt_import_flg = fields.Str(strict=False, required=False)
    device_id = fields.Str(strict=True, required=True)
    versions = fields.List(
        fields.Nested(VersionSchema, unknown=EXCLUDE, allow_none=True)
    )


class GetBaseModelStatusSchema(Schema):
    """"This class will have the schema fields \
    of Get Base Model Status"""

    model_id = fields.Str(strict=True, required=True)
    device_type = fields.Str(strict=True, required=True)
    functionality = fields.Str(strict=True, required=True)
    vendor_name = fields.Str(strict=True, required=True)
    model_comment = fields.Str(strict=True, required=True)
    network_type = fields.Str(strict=True, required=True)
    create_by = fields.Str(strict=False, required=False)
    package_id = fields.Str(strict=False, required=False)
    product_id = fields.Str(strict=False, required=False)
    metadata_format_id = fields.Str(strict=False, required=False)
    projects = fields.List(
        fields.Nested(ProjectSchema, unknown=EXCLUDE, allow_none=True)
    )


class GetBaseModelStatusValidation:
    """This class having a method to invoke schema validation"""

    def __init__(self):
        """Initialize a new instance of SchemaValidation
        :param Get Deploy Configuration: Will store response
        """
        self.get_base_model = []  # taking an empty list to store the response

    def get_base_model_positive_schema(self, response):
        """This method will validate parameters in \
        Get Base Model status API"""
        try:  # using try except blocks for validation purpose
            self.get_base_model.append(
                response
            )  # appending the response to the list
            # Deserialize and validate the input data using the schema
            GetBaseModelStatusSchema(many=True).load(
                self.get_base_model, unknown=EXCLUDE
            )
            return True  # if schema comparsion passes returns true
        except ValidationError as err:
            return err  # if schema comparsion fails returns error
