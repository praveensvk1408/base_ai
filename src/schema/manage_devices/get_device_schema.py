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
# pylint:disable=unused-argument
# pylint:disable=too-many-arguments
# pylint:disable=W0603


# import necessary libraries
from marshmallow import EXCLUDE, Schema, ValidationError, fields

# variables as per constraint of fields
connection_state = ["Connected", "Disconnected"]


class PropertySchema(Schema):
    """This class validate paramters in property field"""

    device_name = fields.Str(metadata={"strict": True}, required=True)
    internal_device_id = fields.Str(metadata={"strict": True}, required=True)


class DeviceGroupsSchema(Schema):
    """This class validate paramters in Device Groups fields"""

    device_group_id = fields.Str(metadata={"strict": True}, required=True)
    device_type = fields.Str(metadata={"strict": True}, required=True)
    comment = fields.Str(metadata={"strict": True}, allow_none=True)
    ins_id = fields.Str(metadata={"strict": True}, required=True)
    ins_date = fields.DateTime(
        metadata={"strict": True},
        required=True,
        format="%Y-%m-%dT%H:%M:%S.%f%z",
    )
    upd_id = fields.Email(metadata={"strict": True}, required=True)
    upd_date = fields.DateTime(
        metadata={"strict": True},
        required=True,
        format="%Y-%m-%dT%H:%M:%S.%f%z",
    )


class OTASchema(Schema):
    """This class validate parameters in the configuration->OTA fields"""

    UpdateModule = fields.Str(allow_none=True)
    DeleteNetworkID = fields.Str(allow_none=True)
    ReplaceNetworkID = fields.Str(allow_none=True)
    PackageUri = fields.Str(allow_none=True)
    DesiredVersion = fields.Str(allow_none=True)
    HashValue = fields.Str(allow_none=True)


class ConfigurationSchema(Schema):
    """This class validate parameters in the configuration fields"""

    OTA = fields.Nested(OTASchema, unknown=EXCLUDE)


class HardwareSchema(Schema):
    """This class validate parameters in the state->Hardware fields"""

    Sensor = fields.Str(strict=True, required=True, allow_none=True)
    SensorId = fields.Str(allow_none=True)
    KG = fields.Str(allow_none=True)
    ApplicationProcessor = fields.Str(allow_none=True)
    LedOn = fields.Bool(allow_none=True)


class VersionSchema(Schema):
    """This class validate parameters in the state->Version fields"""

    SensorFwVersion = fields.Str(allow_none=True)
    SensorLoaderVersion = fields.Str(allow_none=True)
    DnnModelVersion = fields.List(fields.Str(allow_none=True))
    ApFwVersion = fields.Str(allow_none=True)
    ApLoaderVersion = fields.Str(allow_none=True)


class StatusSchema(Schema):
    """This class validate parameters in the state->Status fields"""

    Sensor = fields.Str(allow_none=True)
    ApplicationProcessor = fields.Str(allow_none=True)
    SensorTemperature = fields.Int(allow_none=True)
    HoursMeter = fields.Int(allow_none=True)


class OTAStateSchema(Schema):
    """This class validate parameters in the state->OTA fields"""

    SensorFwLastUpdatedDate = fields.Str(
        metadata={"strict": False}, required=False, format="%Y%m%d%H%M%S"
    )
    SensorLoaderLastUpdatedDate = fields.Str(
        allow_none=True, metadata={"format": "%Y%m%d%H%M%S"}, unknown=EXCLUDE
    )
    DnnModelLastUpdatedDate = fields.List(
        fields.Str(allow_none=True, format="%Y%m%d%H%M%S")
    )
    ApFwLastUpdatedDate = fields.DateTime(
        metadata={"strict": True},
        required=False,
        format="%Y%m%d%H%M%S",
        allow_none=True,
    )
    UpdateProgress = fields.Int(allow_none=True)
    UpdateStatus = fields.Str(allow_none=True)


class ImageSchema(Schema):
    """This class validate parameters in the state->Image fields"""

    FrameRate = fields.Int(allow_none=True)
    DriveMode = fields.Int(allow_none=True)


class ExposureSchema(Schema):
    """This class validate parameters in the state->Exposure fields"""

    ExposureMode = fields.Str(allow_none=True)
    ExposureMaxExposureTime = fields.Int(allow_none=True)
    ExposureMinExposureTime = fields.Int(allow_none=True)
    ExposureMaxGain = fields.Int(allow_none=True)
    AESpeed = fields.Int(allow_none=True)
    ExposureCompensation = fields.Int(allow_none=True)
    ExposureTime = fields.Int(allow_none=True)
    ExposureGain = fields.Int(allow_none=True)
    FlickerReduction = fields.Int(allow_none=True)


class DirectionSchema(Schema):
    """This class validate parameters in the state->Direction fields"""

    Vertical = fields.Str(allow_none=True)
    Horizontal = fields.Str(allow_none=True)


class NetworkSchema(Schema):
    """This class validate parameters in the state->Network fields"""

    ProxyURL = fields.Str(allow_none=True)
    ProxyPort = fields.Int(allow_none=True)
    ProxyUserName = fields.Str(allow_none=True)
    IPAddress = fields.Str(allow_none=True)
    SubnetMask = fields.Str(allow_none=True)
    Gateway = fields.Str(allow_none=True)
    DNS = fields.Str(allow_none=True)
    NTP = fields.Str(allow_none=True)


class PermissionSchema(Schema):
    """This class validate parameters in the state->Permission fields"""

    FactoryReset = fields.Bool(allow_none=True)


class CommandResultsSchema(Schema):
    """This class validate parameters in the command fields"""

    command_name = fields.Str(allow_none=True)
    result = fields.Str(allow_none=True)
    execute_time = fields.Str(allow_none=True)


class AppsSchema(Schema):
    """This class validate parameters in the apps fields"""

    name = fields.Str(allow_none=True)
    version = fields.Str(allow_none=True)
    comment = fields.Str(allow_none=True)


class StateSchema(Schema):
    """This class validate parameters in the state fields"""

    Hardware = fields.Nested(HardwareSchema)
    Version = fields.Nested(VersionSchema)
    Status = fields.Nested(StatusSchema)
    OTA = fields.Nested(OTAStateSchema)
    Image = fields.Nested(ImageSchema)
    Exposure = fields.Nested(ExposureSchema)
    Direction = fields.Nested(DirectionSchema)
    Network = fields.Nested(NetworkSchema)
    Permission = fields.Nested(PermissionSchema)


class ModelSchema(Schema):
    """This class validate paramters in model_version_id fields"""

    model_version_id = fields.Str(required=True, Strict=True)


class GetDevice(Schema):
    """This class validate paramters in Get Devices fields"""

    device_id = fields.Str(
        metadata={"strict": True},
        required=True,
    )
    place = fields.Str(metadata={"strict": True})
    comment = fields.Str(required=True)
    property = fields.Nested(PropertySchema, unknown=EXCLUDE, allow_none=True)
    device_type = fields.Str(metadata={"strict": True})
    display_device_type = fields.Str(metadata={"strict": True})
    ins_id = fields.Str(metadata={"strict": True}, required=True)
    ins_date = fields.DateTime(
        metadata={"strict": True},
        required=True,
        format="%Y-%m-%dT%H:%M:%S.%f%z",
    )
    upd_id = fields.Str(metadata={"strict": True}, required=True)
    upd_date = fields.DateTime(
        metadata={"strict": True},
        required=True,
        format="%Y-%m-%dT%H:%M:%S.%f%z",
    )
    connectionState = fields.Str(
        required=True, validate=lambda check: check in (connection_state)
    )
    lastActivityTime = fields.Str(required=True, allow_none=True)
    models = fields.List(
        fields.Nested(ModelSchema, unknown=EXCLUDE, allow_none=True)
    )
    devices_groups = fields.List(
        fields.Nested(DeviceGroupsSchema, unknown=EXCLUDE),
        metadata={"strict": True},
    )
    configuration = fields.Nested(ConfigurationSchema, unknown=EXCLUDE)
    state = fields.Nested(StateSchema)
    command_results = fields.List(fields.Nested(CommandResultsSchema))
    apps = fields.List(fields.Nested(AppsSchema))


class GetDeviceSchemaValidation:
    """This class having a method to invoke schema validation"""

    def __init__(self):
        """Initialize a new instance of SchemaValidation
        :param get_project_by_id_response: Will store response
        """
        self.get_project_by_id_response = []

    def get_device_positive_schema(self, response):
        """This method invoke schema validation for get devices"""
        # try block that may raise an exception
        try:
            self.get_project_by_id_response.append(response)
            # Deserialize and validate the input data using the GetDevice
            GetDevice(many=True).load(
                self.get_project_by_id_response, unknown=EXCLUDE
            )
            return True
        except ValidationError as err:
            # Handle the exception that has been raised
            return err
