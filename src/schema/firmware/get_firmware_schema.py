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


class VersionsSchema(Schema):
    """This class will have the schema fields of Get Firmware"""

    file_name = fields.Str(strict=True, required=True)
    version_number = fields.Str(strict=True, required=True)
    ppl = fields.Str(strict=True, required=True)
    stored_type = fields.Str(strict=True, required=True)
    stored_uri = fields.Str(strict=True, required=True)
    comment = fields.Str(strict=True, required=True)
    ins_id = fields.Str(strict=True, required=True)
    ins_date = fields.DateTime(strict=True)
    upd_id = fields.Str(
        strict=True,
        required=True,
    )
    upd_date = fields.Str(strict=True, required=True)


class GetFirmwareSchema(Schema):
    """This class will have the schema fields of Get Firmware"""

    firmware_id = fields.Str(
        strict=True,
        required=True,
    )
    firmware_type = fields.Str(strict=True, required=True)
    comment = fields.Str(strict=True, required=True)
    ins_id = fields.Str(strict=True, required=True)
    ins_date = fields.DateTime(strict=True, required=True)
    upd_id = fields.Str(strict=True, required=True)
    upd_date = fields.DateTime(strict=True, required=True)
    versions = fields.List(
        fields.Nested(VersionsSchema, unknown=EXCLUDE, allow_none=True)
    )


class Testdatetime:
    """This class implements the format validation for date and time"""

    def test_date_time_validation(self):
        """This method implements the format validation for date and time"""
        schema = GetFirmwareSchema()
        valid_data = {"ins_date": "2024-02-07T12:12:28.045104+00:00"}
        assert schema.load(valid_data) == valid_data


class GetFirmwareSchemaValidation:
    """This class having a method to invoke Get Firmware schema validation"""

    def __init__(self):
        """Initialize a new instance of SchemaValidation
        :param Get Firmware: Will store response
        """
        self.get_firmware = []  # taking an empty list to store the response

    def get_firmware_positive_schema(self, response):
        """This method will validate parameters in Get Firmware"""
        try:  # using try except blocks for validation purpose
            self.get_firmware.append(
                response
            )  # appending the response to the list
            # Deserialize and validate the input data using the schema
            GetFirmwareSchema(many=True).load(
                self.get_firmware, unknown=EXCLUDE
            )  # loading the response
            return True  # if schema comparsion passes returns true
        except ValidationError as err:
            return err  # if schema comparsion fails returns error
