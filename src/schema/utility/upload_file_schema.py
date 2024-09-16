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
from marshmallow import EXCLUDE, Schema, ValidationError, fields,validate


class FileInfoSchema(Schema):
    """This class validate parameters in file_info fields"""

    file_id = fields.Str(required=True, metadata={"strict": True})
    def validate_name(name):
        if not name.endswith(".zip"):
            raise ValidationError("name must end with .zip")
        
    name = fields.Str(required=True, metadata={"strict": True})
    type_code = fields.Str(required=True, metadata={"strict": True},
    validate=validate.OneOf(choices=["non_converted_model","converted_model","input_format_param","network_config","firmware","edge_app_pkg","dcpu_firmware","dcpu_manifest","dcpu_postprocess"]))
    size = fields.Int(required=True, metadata={"strict": True})

class UploadFile(Schema):
    """This class will have the schema fields of UploadFile"""

    result = fields.Str(required=True, metadata={"strict": True})
    file_info = fields.Nested(FileInfoSchema)


class UploadFileSchemaValidation:
    """This class having a method to invoke
    UploadFile schema validation"""

    def __init__(self):
        """Initialize a new instance of SchemaValidation
        :param UploadFile: Will store response
        """
        self.upload_file = []  # taking an empty list to store the response

    def upload_file_positive_schema(self, response):
        """This method will validate parameters in UploadFile"""
        try:  # using try except blocks for validation purpose
            self.upload_file.append(
                response
            )  # appending the response to the list
            # Deserialize and validate the input data using the schema
            UploadFile(many=True).load(
                self.upload_file, unknown=EXCLUDE
            )
            return True  # if schema comparsion passes returns true
        except ValidationError as err:
            return err  # if schema comparsion fails returns error
