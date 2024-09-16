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


class FirmwareSchema(Schema):
    """This class will have the Nested schema fields
    of Get Deploy Configuration"""

    host_os_file_name = fields.Str(strict=False, required=False)
    host_os_version_number = fields.Str(strict=False, required=False)
    host_os_firmware_comment = fields.Str(strict=False, required=False)
    sensor_loader_file_name = fields.Str(strict=True, required=True)
    sensor_loader_version_number = fields.Str(
        strict=True,
        required=True,
        validate=lambda value: value in [sensor_loader_version_number],
    )
    sensor_loader_firmware_comment = fields.Str(strict=True, required=True)
    sensor_file_name = fields.Str(strict=True, required=True)
    sensor_version_number = fields.Str(
        strict=True,
        required=True,
        validate=lambda value: value in [sensor_fw_version_number],
    )
    sensor_firmware_comment = fields.Str(strict=True, required=True)
    apfw_file_name = fields.Str(strict=True, required=True)
    apfw_version_number = fields.Str(
        strict=True,
        required=True,
        validate=lambda value: value in [ap_fw_version_number],
    )
    apfw_firmware_comment = fields.Str(strict=True, required=True)


class ModelSchema(Schema):
    """This class will have the Nested schema fields
    of Get Deploy Configuration"""

    model_id = fields.Str(
        strict=True, required=True, validate=lambda value: value in (model_ids)
    )
    model_version_number = fields.Str(strict=True, required=True)
    model_comment = fields.Str(strict=True, required=True)
    model_version_comment = fields.Str(strict=True, required=True)


class CustomsetupSchema(Schema):
    """This class will have the Nested schema fields
    of Get Deploy Configuration"""

    color_matrix_mode = fields.Str(strict=False, required=False)
    color_matrix_file_name = fields.Str(strict=False, required=False)
    color_matrix_comment = fields.Str(strict=False, required=False)
    gamma_mode = fields.Str(strict=False, required=False)
    gamma_file_name = fields.Str(strict=False, required=False)
    gamma_comment = fields.Str(strict=False, required=False)
    lscisp_mode = fields.Str(strict=False, required=False)
    lscisp_file_name = fields.Str(strict=False, required=False)
    lscisp_comment = fields.Str(strict=False, required=False)
    lscraw_mode = fields.Str(strict=False, required=False)
    lscraw_file_name = fields.Str(strict=False, required=False)
    lscraw_comment = fields.Str(strict=False, required=False)
    prewb_mode = fields.Str(strict=False, required=False)
    prewb_file_name = fields.Str(strict=False, required=False)
    prewb_comment = fields.Str(strict=False, required=False)
    dewarp_mode = fields.Str(strict=False, required=False)
    dewarp_file_name = fields.Str(strict=False, required=False)
    dewarp_comment = fields.Str(strict=False, required=False)
    picture_setting_ap_mode = fields.Str(strict=False, required=False)
    picture_setting_ap_file_name = fields.Str(strict=False, required=False)
    picture_setting_ap_comment = fields.Str(strict=False, required=False)


class ConfigSchema(Schema):
    """This class will have the schema fields of Get Deploy Configuration"""

    config_id = fields.Str(
        strict=True,
        required=True,
        validate=lambda value: value in (config_ids),
    )
    device_type = fields.Str(strict=True, required=True)
    config_comment = fields.Str(strict=True, required=True)
    running_cnt = fields.Integer(strict=False, required=False)
    success_cnt = fields.Integer(strict=False, required=False)
    fail_cnt = fields.Integer(strict=False, required=False)
    firmware = fields.Nested(FirmwareSchema, unknown=EXCLUDE, allow_none=True)
    model = fields.Nested(ModelSchema, unknown=EXCLUDE, allow_none=True)
    custom_setup = fields.Nested(
        CustomsetupSchema, unknown=EXCLUDE, allow_none=True
    )
    ins_id = fields.Str(strict=True, required=True)
    ins_date = fields.Str(strict=True, required=True)
    upd_id = fields.Str(strict=True, required=True)
    upd_date = fields.Str(strict=True, required=True)


class GetDeployConfigSchemaValidation:
    """This class having a method to invoke schema validation"""

    def __init__(self):
        """Initialize a new instance of SchemaValidation
        :param Get Deploy Configuration: Will store response
        """
        self.get_deploy_configuration = (
            []
        )  # taking an empty list to store the response

    def get_deply_config_positive_schema(
        self,
        response,
        config_id,
        ap_fw_vn,
        sensor_loader_vn,
        sensor_vn,
        model_id,
    ):
        """This method will validate parameters in
        Create Deploy Configuration"""
        try:  # using try except blocks for validation purpose
            global config_ids, model_ids, sensor_fw_version_number
            global sensor_loader_version_number, ap_fw_version_number
            config_ids = config_id
            model_ids = model_id
            sensor_fw_version_number = sensor_vn
            sensor_loader_version_number = sensor_loader_vn
            ap_fw_version_number = ap_fw_vn
            self.get_deploy_configuration.append(
                response
            )  # appending the response to the list
            # Deserialize and validate the input data using the schema
            ConfigSchema(many=True).load(
                self.get_deploy_configuration, unknown=EXCLUDE
            )  # loading the response
            return True  # if schema comparsion passes returns true
        except ValidationError as err:
            return err  # if schema comparsion fails returns error
