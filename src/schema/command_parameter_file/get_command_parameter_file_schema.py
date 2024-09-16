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


class HeaderSchema(Schema):
    """This class will validate parameters in HeaderSchema"""

    id = fields.Str(strict=True, required=True)
    version = fields.Str(strict=True, required=True)


class PPLParameterSchema(Schema):
    """This class will validate parameters in PPLParameterSchema"""

    header = fields.Nested(HeaderSchema, unknown=EXCLUDE, allow_none=True)
    dnn_output_detections = fields.Int(strict=True, required=True)
    max_detections = fields.Int(strict=True, required=True)
    threshold = fields.Float(strict=True, required=True)
    input_width = fields.Int(strict=True, required=True)
    input_height = fields.Int(strict=True, required=True)
    iou_threhold = fields.Int(strict=True, required=True)
    score_threshold = fields.Int(strict=True, required=True)


class ParametersListSchema(Schema):
    """This class will validate parameters in ParametersListSchema"""

    Mode = fields.Int(strict=True, required=True)
    UploadMethod = fields.Str(
        strict=False
    )  # specifies how to upload Input Image
    FileFormat = fields.Str(
        required=False,
        allow_none=True,
        validate=lambda s: s.lower().endswith((".jpg", ".bmp", ".jpeg")),
    )
    UploadMethodIR = fields.Str(strict=True, required=True)
    CropHOffset = fields.Int(strict=True, required=True)
    CropVOffset = fields.Int(strict=True, required=True)
    CropHSize = fields.Int(strict=True, required=True)
    CropVSize = fields.Int(strict=True, required=True)
    NumberOfImages = fields.Int(strict=False, required=False)
    UploadInterval = fields.Int(strict=True, required=True)
    NumberOfInferencesPerMessage = fields.Int(strict=False, required=False)
    MaxDetectionsPerFrame = fields.Int(strict=False, required=False)
    ModelId = fields.Str(strict=True, required=True)
    PPLParameter = fields.Nested(PPLParameterSchema, required=True)


class CommandParameterSchema(Schema):
    """This class will validate CommandParameterSchema"""

    command_name = fields.Str(
        required=True, many=True
    )  # 'command_name' is required
    parameters = fields.Nested(
        ParametersListSchema, unknown=EXCLUDE, allow_none=True
    )  # 'parameters' is required


class CommandSchema(Schema):
    """This class will validate parameters in CommandSchema"""

    commands = fields.List(
        fields.Nested(CommandParameterSchema, unknown=EXCLUDE, allow_none=True)
    )


class ParameterSchema(Schema):
    """This class will validate parameters in ParameterSchema"""

    parameter = fields.Nested(
        CommandSchema, unknown=EXCLUDE, allow_none=True
    )  # 'commands' is required
    file_name = fields.Str(required=True, strict=True)
    comment = fields.Str(strict=True, required=True)
    isdefault = fields.Str(
        dump_default="True",
        validate=validate.OneOf(["True", "False"]),
        required=True,
    )
    device_ids = fields.List(fields.Str(required=True), many=True)
    ins_id = fields.Str(strict=True, required=True)
    ins_date = fields.DateTime(metadata={"strict": True}, required=True)
    upd_id = fields.Str(metadata={"strict": True}, required=True)
    upd_date = fields.DateTime(metadata={"strict": True}, required=True)

    @pre_load
    def translate(self, data, *args, **kwargs):
        """This method will pre-set for various corresponding none value"""
        if data.get("file_name") == "":
            data["file_name"] = None
        return data


class GetCommandParameterList(Schema):
    """This class will validate parameters in Get Command Parameter File API"""

    parameter_list = fields.List(
        fields.Nested(ParameterSchema, unknown=EXCLUDE, allow_none=True)
    )  # 'parameter_list' is required


class GetCommandParameterFileSchemaValidation:
    """The class SchemaValidation is for validating schema for
    Get Command Parameter File"""

    def __init__(self):
        """Initialize a new instance of SchemaValidation
        :param get_command_parameter_file: Will store response
        """
        self.get_command_parameter_file = []

    def get_command_parameter_file_positive_schema(self, response):
        """This function is for validating with positive response"""
        # Implementation of schema
        try:
            # try block that may raise an exception
            # appending the response
            self.get_command_parameter_file.append(response)
            # Deserialize and validate the input data using the schema
            GetCommandParameterList(many=True).load(
                self.get_command_parameter_file, unknown=EXCLUDE
            )
            return True
        except ValidationError as err:
            # Handle the exception that has been raised
            return err


# data = {
#     "parameter_list": [
#         {
#             "parameter": {
#                 "commands": [
#                     {
#                         "command_name": "StartUploadInferenceData",
#                         "parameters": {
#                             "ModelId": "HumanDetectionAttribution_v1.2.0",
#                             "Mode": 2,
#                             "UploadMethod": "BlobStorage",
#                             "FileFormat": "JPG",
#                             "UploadMethodIR": "MQTT",
#                             "CropHOffset": 0,
#                             "CropVOffset": 0,
#                             "CropHSize": 4056,
#                             "CropVSize": 3040,
#                             "NumberOfImages": 0,
#                             "NumberOfInferencesPerMessage": 5,
#                             "UploadInterval": 1,
#                             "PPLParameter": {
#                                 "log_level": "close",
#                                 "max_body_detection": 30,
#                                 "body_detection_ROI": {
#                                     "left": 0,
#                                     "top": 0,
#                                     "right": 512,
#                                     "bottom": 384
#                                 },
#                                 "body_detection_threshold": 0.4,
#                                 "body_detection_iou_nms_threshold": 0.5,
#                                 "gender_threshold": 0.57,
#                                 "track_iou_threshold": 0.9,
#                                 "kalman_filter_enable": true,
#                                 "cluster_ROI": [
#                                     {
#                                         "x": 0,
#                                         "y": 0
#                                     },
#                                     {
#                                         "x": 512,
#                                         "y": 0
#                                     },
#                                     {
#                                         "x": 512,
#                                         "y": 384
#                                     },
#                                     {
#                                         "x": 0,
#                                         "y": 384
#                                     }
#                                 ],
#                                 "attribute_ROI": [],
#                                 "trajectory_db_lifetime": 10
#                             }
#                         }
#                     }
#                 ]
#             },
#             "file_name": "HumanDetectionAttribution_WASMStep3.json",
#             "isdefault": "false",
#             "comment": "",
#             "device_ids": [],
#             "ins_id": "0oagplyjar2nouTw51d7",
#             "ins_date": "2024-09-16 08: 44: 46.644248+00: 00",
#             "upd_id": "0oagplyjar2nouTw51d7",
#             "upd_date": "2024-09-16 08: 44: 46.644248+00: 00"
#         },
#         {
#             "parameter": {
#                 "commands": [
#                     {
#                         "command_name": "StartUploadInferenceData",
#                         "parameters": {
#                             "ModelId": "GazeDetction_SARD_Test_20240723",
#                             "Mode": 1,
#                             "UploadMethod": "BlobStorage",
#                             "FileFormat": "JPG",
#                             "UploadMethodIR": "BlobStorage",
#                             "CropHOffset": 0,
#                             "CropVOffset": 0,
#                             "CropHSize": 4056,
#                             "CropVSize": 3040,
#                             "NumberOfImages": 0,
#                             "UploadInterval": 1,
#                             "NumberOfInferencesPerMessage": 1,
#                             "PPLParameter": {
#                                 "log_level": "close",
#                                 "face_detection_nms_threshold": 0.5,
#                                 "max_body_detection": 30,
#                                 "body_detection_threshold": 0.32,
#                                 "face_detection_threshold": 0.315,
#                                 "face_detection_ROI": [
#                                     [
#                                         0,
#                                         0
#                                     ],
#                                     [
#                                         640,
#                                         0
#                                     ],
#                                     [
#                                         640,
#                                         480
#                                     ],
#                                     [
#                                         0,
#                                         480
#                                     ]
#                                 ],
#                                 "cluster_ROI": [
#                                     [
#                                         0,
#                                         0
#                                     ],
#                                     [
#                                         640,
#                                         0
#                                     ],
#                                     [
#                                         640,
#                                         480
#                                     ],
#                                     [
#                                         0,
#                                         480
#                                     ]
#                                 ],
#                                 "trajectory_db_lifetime": 10.0,
#                                 "cluster_iou_threshold": 0.65,
#                                 "id_creation_threshold": 0.6,
#                                 "gender_threshold": 0.6,
#                                 "gaze_focus_threshold": 0,
#                                 "enable_watching_region": true,
#                                 "watching_region": {
#                                     "min_yaw": -19,
#                                     "max_yaw": 45,
#                                     "min_pitch": -15,
#                                     "max_pitch": 15
#                                 },
#                                 "enable_gaze_time_functions": true,
#                                 "inference_result_filter_enable": true
#                             }
#                         }
#                     }
#                 ]
#             },
#             "file_name": "TS1_Azure_Mode1_summary.json",
#             "isdefault": "false",
#             "comment": "",
#             "device_ids": [
#                 "Aid-80010003-0000-2000-9002-000000000327"
#             ],
#             "ins_id": "00ufwv21ofMnEZmoE1d7",
#             "ins_date": "2024-09-10 07: 35: 41.741114+00: 00",
#             "upd_id": "00ufwv21ofMnEZmoE1d7",
#             "upd_date": "2024-09-10 09: 56: 56.356027+00: 00"
#         },
#         {
#             "parameter": {
#                 "commands": [
#                     {
#                         "command_name": "StartUploadInferenceData",
#                         "parameters": {
#                             "ModelId": "GazeDetction_SARD_Test_20240723",
#                             "Mode": 1,
#                             "UploadMethod": "BlobStorage",
#                             "FileFormat": "JPG",
#                             "UploadMethodIR": "MQTT",
#                             "CropHOffset": 0,
#                             "CropVOffset": 0,
#                             "CropHSize": 4056,
#                             "CropVSize": 3040,
#                             "NumberOfImages": 0,
#                             "UploadInterval": 1,
#                             "NumberOfInferencesPerMessage": 1,
#                             "PPLParameter": {
#                                 "log_level": "close",
#                                 "face_detection_nms_threshold": 0.5,
#                                 "max_body_detection": 30,
#                                 "body_detection_threshold": 0.32,
#                                 "face_detection_threshold": 0.315,
#                                 "face_detection_ROI": [
#                                     [
#                                         0,
#                                         0
#                                     ],
#                                     [
#                                         640,
#                                         0
#                                     ],
#                                     [
#                                         640,
#                                         480
#                                     ],
#                                     [
#                                         0,
#                                         480
#                                     ]
#                                 ],
#                                 "cluster_ROI": [
#                                     [
#                                         0,
#                                         0
#                                     ],
#                                     [
#                                         640,
#                                         0
#                                     ],
#                                     [
#                                         640,
#                                         480
#                                     ],
#                                     [
#                                         0,
#                                         480
#                                     ]
#                                 ],
#                                 "trajectory_db_lifetime": 10.0,
#                                 "cluster_iou_threshold": 0.65,
#                                 "id_creation_threshold": 0.6,
#                                 "gender_threshold": 0.6,
#                                 "gaze_focus_threshold": 0,
#                                 "enable_watching_region": true,
#                                 "watching_region": {
#                                     "min_yaw": -19,
#                                     "max_yaw": 45,
#                                     "min_pitch": -15,
#                                     "max_pitch": 15
#                                 },
#                                 "enable_gaze_time_functions": true,
#                                 "inference_result_filter_enable": true
#                             }
#                         }
#                     }
#                 ]
#             },
#             "file_name": "gazedetection_summary.json",
#             "isdefault": "false",
#             "comment": "",
#             "device_ids": [
#                 "Aid-80010003-0000-2000-9002-00000000031b"
#             ],
#             "ins_id": "00u6tqmuvtadoVPGQ1d7",
#             "ins_date": "2024-07-25 06: 37: 56.952810+00: 00",
#             "upd_id": "00u6tqmuvtadoVPGQ1d7",
#             "upd_date": "2024-07-25 06: 37: 56.952810+00: 00"
#         },
#         {
#             "parameter": {
#                 "commands": [
#                     {
#                         "command_name": "StartUploadInferenceData",
#                         "parameters": {
#                             "ModelId": "Coffee_pod",
#                             "Mode": 1,
#                             "UploadMethod": "BlobStorage",
#                             "FileFormat": "JPG",
#                             "UploadMethodIR": "MQTT",
#                             "CropHOffset": 0,
#                             "CropVOffset": 0,
#                             "CropHSize": 4056,
#                             "CropVSize": 3040,
#                             "NumberOfImages": 10,
#                             "UploadInterval": 1,
#                             "NumberOfInferencesPerMessage": 1
#                         }
#                     }
#                 ]
#             },
#             "file_name": "ssd_mobilenet_cmd_param.json",
#             "isdefault": "false",
#             "comment": "",
#             "device_ids": [],
#             "ins_id": "00u6tqmuvtadoVPGQ1d7",
#             "ins_date": "2024-07-24 12: 19: 13.849929+00: 00",
#             "upd_id": "00u6tqmuvtadoVPGQ1d7",
#             "upd_date": "2024-07-24 12: 19: 13.849929+00: 00"
#         },
#         {
#             "parameter": {
#                 "commands": [
#                     {
#                         "command_name": "StartUploadInferenceData",
#                         "parameters": {
#                             "ModelId": "GazeDetction_SARD_Test_20240723",
#                             "Mode": 2,
#                             "UploadMethod": "BlobStorage",
#                             "FileFormat": "JPG",
#                             "UploadMethodIR": "MQTT",
#                             "CropHOffset": 0,
#                             "CropVOffset": 0,
#                             "CropHSize": 4056,
#                             "CropVSize": 3040,
#                             "NumberOfImages": 0,
#                             "UploadInterval": 1,
#                             "NumberOfInferencesPerMessage": 30,
#                             "PPLParameter": {
#                                 "log_level": "close",
#                                 "face_detection_nms_threshold": 0.5,
#                                 "max_body_detection": 30,
#                                 "body_detection_threshold": 0.32,
#                                 "face_detection_threshold": 0.315,
#                                 "face_detection_ROI": [
#                                     [
#                                         0,
#                                         0
#                                     ],
#                                     [
#                                         640,
#                                         0
#                                     ],
#                                     [
#                                         640,
#                                         480
#                                     ],
#                                     [
#                                         0,
#                                         480
#                                     ]
#                                 ],
#                                 "cluster_ROI": [
#                                     [
#                                         0,
#                                         0
#                                     ],
#                                     [
#                                         640,
#                                         0
#                                     ],
#                                     [
#                                         640,
#                                         480
#                                     ],
#                                     [
#                                         0,
#                                         480
#                                     ]
#                                 ],
#                                 "trajectory_db_lifetime": 10.0,
#                                 "cluster_iou_threshold": 0.65,
#                                 "id_creation_threshold": 0.6,
#                                 "gender_threshold": 0.6,
#                                 "gaze_focus_threshold": 0,
#                                 "enable_watching_region": true,
#                                 "watching_region": {
#                                     "min_yaw": -19,
#                                     "max_yaw": 45,
#                                     "min_pitch": -15,
#                                     "max_pitch": 15
#                                 },
#                                 "enable_gaze_time_functions": true,
#                                 "inference_result_filter_enable": false
#                             }
#                         }
#                     }
#                 ]
#             },
#             "file_name": "byframe_fps.json",
#             "isdefault": "false",
#             "comment": "",
#             "device_ids": [],
#             "ins_id": "00u6tqmuvtadoVPGQ1d7",
#             "ins_date": "2024-07-24 05: 04: 54.396120+00: 00",
#             "upd_id": "00u6tqmuvtadoVPGQ1d7",
#             "upd_date": "2024-07-24 05: 04: 54.396120+00: 00"
#         },
#         {
#             "parameter": {
#                 "commands": [
#                     {
#                         "command_name": "StartUploadInferenceData",
#                         "parameters": {
#                             "ModelId": "GazeDetction_SARD_Test_20240723",
#                             "Mode": 1,
#                             "UploadMethod": "BlobStorage",
#                             "FileFormat": "JPG",
#                             "UploadMethodIR": "MQTT",
#                             "CropHOffset": 0,
#                             "CropVOffset": 0,
#                             "CropHSize": 4056,
#                             "CropVSize": 3040,
#                             "NumberOfImages": 1,
#                             "UploadInterval": 1,
#                             "NumberOfInferencesPerMessage": 1,
#                             "PPLParameter": {
#                                 "log_level": "close",
#                                 "face_detection_nms_threshold": 0.5,
#                                 "max_body_detection": 30,
#                                 "body_detection_threshold": 0.32,
#                                 "face_detection_threshold": 0.315,
#                                 "face_detection_ROI": [
#                                     [
#                                         0,
#                                         0
#                                     ],
#                                     [
#                                         640,
#                                         0
#                                     ],
#                                     [
#                                         640,
#                                         480
#                                     ],
#                                     [
#                                         0,
#                                         480
#                                     ]
#                                 ],
#                                 "cluster_ROI": [
#                                     [
#                                         0,
#                                         0
#                                     ],
#                                     [
#                                         640,
#                                         0
#                                     ],
#                                     [
#                                         640,
#                                         480
#                                     ],
#                                     [
#                                         0,
#                                         480
#                                     ]
#                                 ],
#                                 "trajectory_db_lifetime": 10.0,
#                                 "cluster_iou_threshold": 0.65,
#                                 "id_creation_threshold": 0.6,
#                                 "gender_threshold": 0.6,
#                                 "gaze_focus_threshold": 0,
#                                 "enable_watching_region": true,
#                                 "watching_region": {
#                                     "min_yaw": -19,
#                                     "max_yaw": 45,
#                                     "min_pitch": -15,
#                                     "max_pitch": 15
#                                 },
#                                 "enable_gaze_time_functions": true,
#                                 "inference_result_filter_enable": false
#                             }
#                         }
#                     }
#                 ]
#             },
#             "file_name": "byframe_Image1.json",
#             "isdefault": "false",
#             "comment": "",
#             "device_ids": [],
#             "ins_id": "00u6tqmuvtadoVPGQ1d7",
#             "ins_date": "2024-07-24 05: 00: 45.371442+00: 00",
#             "upd_id": "00u6tqmuvtadoVPGQ1d7",
#             "upd_date": "2024-07-24 05: 04: 18.635117+00: 00"
#         },
#         {
#             "parameter": {
#                 "commands": [
#                     {
#                         "command_name": "StartUploadInferenceData",
#                         "parameters": {
#                             "ModelId": "Tetras_Gaze_Patch3_0531",
#                             "Mode": 1,
#                             "UploadMethod": "BlobStorage",
#                             "FileFormat": "JPG",
#                             "UploadMethodIR": "MQTT",
#                             "CropHOffset": 0,
#                             "CropVOffset": 0,
#                             "CropHSize": 4056,
#                             "CropVSize": 3040,
#                             "NumberOfImages": 0,
#                             "UploadInterval": 1,
#                             "NumberOfInferencesPerMessage": 1,
#                             "PPLParameter": {
#                                 "log_level": "close",
#                                 "face_detection_nms_threshold": 0.5,
#                                 "max_body_detection": 30,
#                                 "body_detection_threshold": 0.32,
#                                 "face_detection_threshold": 0.315,
#                                 "face_detection_ROI": [
#                                     [
#                                         0,
#                                         0
#                                     ],
#                                     [
#                                         640,
#                                         0
#                                     ],
#                                     [
#                                         640,
#                                         480
#                                     ],
#                                     [
#                                         0,
#                                         480
#                                     ]
#                                 ],
#                                 "cluster_ROI": [
#                                     [
#                                         0,
#                                         0
#                                     ],
#                                     [
#                                         640,
#                                         0
#                                     ],
#                                     [
#                                         640,
#                                         480
#                                     ],
#                                     [
#                                         0,
#                                         480
#                                     ]
#                                 ],
#                                 "trajectory_db_lifetime": 10.0,
#                                 "cluster_iou_threshold": 0.65,
#                                 "id_creation_threshold": 0.6,
#                                 "gender_threshold": 0.6,
#                                 "gaze_focus_threshold": 0,
#                                 "enable_watching_region": true,
#                                 "watching_region": {
#                                     "min_yaw": -19,
#                                     "max_yaw": 45,
#                                     "min_pitch": -15,
#                                     "max_pitch": 15
#                                 },
#                                 "enable_gaze_time_functions": true,
#                                 "inference_result_filter_enable": true
#                             }
#                         }
#                     }
#                 ]
#             },
#             "file_name": "summary.json",
#             "isdefault": "false",
#             "comment": "",
#             "device_ids": [],
#             "ins_id": "00u6tqmuvtadoVPGQ1d7",
#             "ins_date": "2024-07-24 04: 59: 57.383951+00: 00",
#             "upd_id": "00u6tqmuvtadoVPGQ1d7",
#             "upd_date": "2024-07-24 04: 59: 57.383951+00: 00"
#         }
#     ]
# }