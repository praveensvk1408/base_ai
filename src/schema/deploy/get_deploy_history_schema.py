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

from marshmallow import (EXCLUDE, Schema, ValidationError, fields, pre_load,
                         validate)

sensor_flg = ["0", "1"]
status_flg = ["0", "1", "2", "3"]


class Sensorschema(Schema):
    """This class validate the parameters in Sensor"""

    host_os_target_flg = fields.Str(allow_none=True)
    host_os_status = fields.Str(allow_none=True)
    host_os_retry_count = fields.Int(allow_none=True)
    host_os_start_date = fields.Str(allow_none=True)
    host_os_end_date = fields.Str(allow_none=True)
    host_os_version_number = fields.Str(allow_none=True)
    host_os_version_comment = fields.Str(allow_none=True)

    sensor_loader_target_flg = fields.Str(
        allow_none=True, validate=lambda value: value in (sensor_flg)
    )
    sensor_loader_status = fields.Str(
        required=False,
        validate=lambda value: value in (status_flg),
        allow_none=True,
    )
    sensor_loader_retry_count = fields.Int(required=False, allow_none=True)
    sensor_loader_start_date = fields.Str(required=False, allow_none=True)
    sensor_loader_end_date = fields.Str(required=False, allow_none=True)
    sensor_loader_version_number = fields.Str(required=False, allow_none=True)
    sensor_loader_version_comment = fields.Str(
        validate=validate.Length(max=100), allow_none=True
    )
    sensor_target_flg = fields.Str(
        required=True,
        validate=lambda value: value in (sensor_flg),
        allow_none=True,
    )
    sensor_status = fields.Str(required=False)
    sensor_retry_count = fields.Int(required=False, allow_none=True)
    sensor_start_date = fields.Str(required=False, allow_none=True)
    sensor_end_date = fields.Str(required=False, allow_none=True)
    sensor_version_number = fields.Str(required=False, allow_none=True)
    sensor_version_comment = fields.Str(
        validate=validate.Length(max=100), allow_none=True
    )
    apfw_target_flg = fields.Str(
        required=False,
        validate=lambda value: value in (sensor_flg),
        allow_none=True,
    )
    apfw_status = fields.Str(required=False, allow_none=True)
    apfw_retry_count = fields.Int(required=False, allow_none=True)
    apfw_start_date = fields.Str(required=False, allow_none=True)
    apfw_end_date = fields.Str(required=False, allow_none=True)
    apfw_version_number = fields.Str(required=False, allow_none=True)
    apfw_version_comment = fields.Str(
        validate=validate.Length(max=100), allow_none=True
    )

    @pre_load
    def translate(self, data, *args, **kwargs):
        """This method will pre-set for various corresponding none value"""
        if (
            data.get("sensor_loader_target_flg") == ""
            or data.get("sensor_target_flg") == ""
            or data.get("apfw_target_flg") == ""
            or data.get("sensor_loader_start_date") == ""
            or data.get("sensor_loader_status") == ""
            or data.get("sensor_loader_end_date") == ""
            or data.get("sensor_start_date") == ""
            or data.get("sensor_end_date") == ""
            or data.get("apfw_start_date") == ""
            or data.get("apfw_end_date") == ""
        ):
            data["sensor_loader_target_flg"] = None
            data["sensor_target_flg"] = None
            data["apfw_target_flg"] = None
            data["sensor_loader_start_date"] = None
            data["sensor_loader_status"] = None
            data["sensor_loader_end_date"] = None
            data["sensor_start_date"] = None
            data["sensor_end_date"] = None
            data["apfw_start_date"] = None
            data["apfw_end_date"] = None
        return data


class Modelschema(Schema):
    """This class validate the parameters in Model"""

    model_target_flg = fields.Str(
        required=False,
        validate=lambda value: value in (sensor_flg),
        allow_none=True,
    )
    model_status = fields.Str(required=False, allow_none=True)
    model_retry_count = fields.Int(required=False, allow_none=True)
    model_start_date = fields.DateTime(allow_none=True)
    model_end_date = fields.DateTime(allow_none=True)
    model_id = fields.Str(required=False, allow_none=True)
    model_version_number = fields.Str(required=False, allow_none=True)
    model_comment = fields.Str(
        validate=validate.Length(max=100), allow_none=True
    )
    model_version_comment = fields.Str(
        validate=validate.Length(max=100), allow_none=True
    )
    dnn_param_setting_target_flg = fields.Str(
        required=False, validate=lambda value: value in (["", "0", "1"])
    )
    dnn_param_setting_status = fields.Str(required=False, allow_none=True)
    dnn_param_setting_retry_count = fields.Str(required=False, allow_none=True)
    dnn_param_setting_start_date = fields.DateTime(allow_none=True)
    dnn_param_setting_end_date = fields.DateTime(allow_none=True)

    @pre_load
    def translate(self, data, *args, **kwargs):
        """This method will pre-set for various corresponding none value"""
        if (
            data.get("dnn_param_setting_start_date") == ""
            or data.get("dnn_param_setting_end_date") == ""
            or data.get("model_start_date") == ""
            or data.get("model_end_date") == ""
            or data.get("model_target_flg") == ""
        ):
            data["dnn_param_setting_end_date"] = None
            data["dnn_param_setting_start_date"] = None
            data["model_start_date"] = None
            data["model_end_date"] = None
            data["model_target_flg"] = None
        return data


class Customschema(Schema):
    """This class validate the parameters in Custom"""

    color_matrix_target_flg = fields.Str(
        required=True,
        validate=lambda value: value in (sensor_flg),
        allow_none=True,
    )
    color_matrix_status = fields.Str(required=False, allow_none=True)
    color_matrix_retry_count = fields.Int(required=False, allow_none=True)
    color_matrix_start_date = fields.DateTime(allow_none=True)
    color_matrix_end_date = fields.DateTime(allow_none=True)
    color_matrix_mode = fields.Str(required=False)
    color_matrix_file_name = fields.Str(required=False)
    color_matrix_comment = fields.Str(validate=validate.Length(max=100))
    gamma_target_flg = fields.Str(
        required=False,
        validate=lambda value: value in (sensor_flg),
        allow_none=True,
    )
    gamma_status = fields.Str(required=False)
    gamma_retry_count = fields.Int(required=False)
    gamma_start_date = fields.DateTime(allow_none=True)
    gamma_end_date = fields.DateTime(allow_none=True)
    gamma_mode = fields.Str(required=False)
    gamma_file_name = fields.Str(required=False)
    gamma_comment = fields.Str(validate=validate.Length(max=100))
    lscisp_target_flg = fields.Str(
        required=False,
        validate=lambda value: value in (sensor_flg),
        allow_none=True,
    )
    lscisp_status = fields.Str(required=False)
    lscisp_retry_count = fields.Int(required=False)
    lscisp_start_date = fields.DateTime(allow_none=True)
    lscisp_end_date = fields.DateTime(allow_none=True)
    lscisp_mode = fields.Str(required=False)
    lscisp_file_name = fields.Str(required=False)
    lscisp_comment = fields.Str(validate=validate.Length(max=100))
    lscraw_target_flg = fields.Str(
        required=False,
        validate=lambda value: value in (sensor_flg),
        allow_none=True,
    )
    lscraw_status = fields.Str(required=False)
    lscraw_retry_count = fields.Int(required=False)
    lscraw_start_date = fields.DateTime(allow_none=True)
    lscraw_end_date = fields.DateTime(allow_none=True)
    lscraw_mode = fields.Str(required=False)
    lscraw_file_name = fields.Str(required=False)
    lscraw_comment = fields.Str(validate=validate.Length(max=100))
    prewb_target_flg = fields.Str(
        required=False,
        validate=lambda value: value in (sensor_flg),
        allow_none=True,
    )
    prewb_status = fields.Str(required=False)
    prewb_retry_count = fields.Int(allow_none=True)
    prewb_start_date = fields.DateTime(allow_none=True)
    prewb_end_date = fields.DateTime(allow_none=True)
    prewb_mode = fields.Str(required=False)
    prewb_file_name = fields.Str(required=False)
    prewb_comment = fields.Str(validate=validate.Length(max=100))
    dewarp_target_flg = fields.Str(
        required=False,
        validate=lambda value: value in (sensor_flg),
        allow_none=True,
    )
    dewarp_status = fields.Str(required=False)
    dewarp_retry_count = fields.Int(required=False)
    dewarp_start_date = fields.DateTime(allow_none=True)
    dewarp_end_date = fields.DateTime(allow_none=True)
    dewarp_mode = fields.Str(required=False)
    dewarp_file_name = fields.Str(required=False)
    dewarp_comment = fields.Str(
        validate=validate.Length(max=100), allow_none=True
    )
    picture_setting_ap_target_flg = fields.Str(allow_none=True)
    picture_setting_ap_status = fields.Str(allow_none=True)
    picture_setting_ap_retry_count = fields.Int(allow_none=True)
    picture_setting_ap_start_date = fields.Str(allow_none=True)
    picture_setting_ap_end_date = fields.Str(allow_none=True)
    picture_setting_ap_mode = fields.Str(allow_none=True)
    picture_setting_ap_file_name = fields.Str(allow_none=True)
    picture_setting_ap_comment = fields.Str(allow_none=True)

    @pre_load
    def translate(self, data, *args, **kwargs):
        """This method will pre-set for various corresponding none value"""
        if (
            data.get("color_matrix_start_date") == ""
            or data.get("color_matrix_end_date") == ""
            or data.get("color_matrix_target_flg") == ""
            or data.get("gamma_start_date") == ""
            or data.get("gamma_target_flg") == ""
            or data.get("gamma_end_date") == ""
            or data.get("lscisp_start_date") == ""
            or data.get("lscisp_end_date") == ""
            or data.get("lscraw_start_date") == ""
            or data.get("lscraw_end_date") == ""
            or data.get("lscisp_target_flg") == ""
            or data.get("prewb_start_date") == ""
            or data.get("prewb_end_date") == ""
            or data.get("prewb_target_flg") == ""
            or data.get("dewarp_start_date") == ""
            or data.get("dewarp_end_date") == ""
            or data.get("dewarp_target_flg") == ""
            or data.get("lscraw_target_flg") == ""
        ):
            data["color_matrix_start_date"] = None
            data["color_matrix_end_date"] = None
            data["color_matrix_target_flg"] = None
            data["gamma_target_flg"] = None
            data["gamma_start_date"] = None
            data["gamma_end_date"] = None
            data["lscisp_start_date"] = None
            data["lscisp_end_date"] = None
            data["lscraw_start_date"] = None
            data["lscraw_end_date"] = None
            data["lscisp_target_flg"] = None
            data["prewb_start_date"] = None
            data["prewb_end_date"] = None
            data["prewb_target_flg"] = None
            data["dewarp_start_date"] = None
            data["dewarp_end_date"] = None
            data["dewarp_target_flg"] = None
            data["lscraw_target_flg"] = None
        return data


class Idschema(Schema):
    """This class validate the parameters in Ids"""

    id = fields.Int(strict=True, required=True)
    deploy_type = fields.Str(required=True)
    deploy_status = fields.Str(
        validate=validate.Length(max=100), required=True
    )
    deploy_comment = fields.Str(allow_none=True)
    config_id = fields.Str(allow_none=True)
    replace_network_id = fields.Str(allow_none=True, required=True)
    current_target = fields.Str(allow_none=True, required=True)
    total_status = fields.Str(allow_none=True)
    update_progress = fields.Str(allow_none=True)
    deploy_device_comment = fields.Str(allow_none=True)
    version_number = fields.Str(required=False)
    firmware = fields.Nested(Sensorschema, required=True)
    model = fields.Nested(Modelschema)
    custom_setting = fields.Nested(
        Customschema, unknown=EXCLUDE, allow_none=True
    )
    ins_id = fields.Str(required=False, allow_none=True)
    ins_date = fields.Str(required=True)
    upd_id = fields.Str(required=False, allow_none=True)
    upd_date = fields.Str(required=True, allow_none=True)


class GetDeployHistory(Schema):
    """This class validate the parameters in Get Deploy History"""

    deploys = fields.List(fields.Nested(Idschema, required=True))


class GetDeployHistorySchemaValidation:
    """This class having a method to invoke
    schema validation get deploy history"""

    def __init__(self):
        """Initialize a new instance of SchemaValidation
        :param get_deploy_history: Will store response
        """
        self.get_deploy_history = []

    def get_deploy_history_positive_schema(self, response):
        """This method will invoke Schema to Validate"""
        try:
            # try block that may raise an exception
            self.get_deploy_history.append(response)
            # Deserialize and validate the input
            # data using the GetDeployHistory
            GetDeployHistory(many=True).load(
                self.get_deploy_history, unknown=EXCLUDE
            )
            return True

        except ValidationError as err:
            return err
