# pylint:disable=wrong-import-position
# pylint:disable=duplicate-code
# pylint:disable=too-few-public-methods
# pylint:disable=missing-module-docstring
# pylint:disable=import-error
# pylint:disable=E1101
# pylint:disable=R0913
"""This module implements the test functions  API"""
import json
import os
import time
from datetime import datetime, timezone
from src.schema.device_command.start_upload_inference_result_schema import StartUploadInferenceResultSchemaValidation
from src.schema.device_command.stop_upload_inference_result_schema import StopUploadInferenceResultSchemaValidation
from src.schema.manage_devices.get_device_schema import GetDeviceSchemaValidation
from src.schema.command_parameter_file.bind_command_parameter_file_to_device_schema import BindCommandParameterFileToDeviceSchemaValidation
from src.schema.deploy.deploy_by_configuration_schema import DeploybyConfigurationSchemaValidation
from src.schema.deploy.get_deploy_history_schema import GetDeployHistorySchemaValidation
from src.schema.edge_app.deploy_edge_app_schema import DeployEdgeAppbyConfigurationSchemaValidation
from src.component.device_app import DeviceApp
from src.component.edge_app import EdgeApp
from src.schema.edge_app.get_edge_app_schema import GetEdgeAppSchemaValidation
from src.schema.edge_app.import_edge_app_schema import ImportEdgeAppSchemaValidation
from src.schema.utility.upload_file_schema import UploadFileSchemaValidation
from src.schema.command_parameter_file.get_command_parameter_file_schema import GetCommandParameterFileSchemaValidation
from src.schema.command_parameter_file.register_command_parameter_file_schema import RegisterCommandParameterFileSchemaValidation
from src.schema.deploy.create_deploy_configuration_schema import CreateDeployConfigurationSchemaValidation
from src.schema.deploy.get_deploy_configuration_schema import GetDeployConfigSchemaValidation
from src.schema.firmware.create_firmware_schema import CreateFirmwareSchemaValidation
from src.schema.firmware.get_firmware_schema import GetFirmwareSchemaValidation
from src.schema.negative_schema.negative_schema import NegativeSchemaValidation
from src.schema.train_model.get_base_model_status_schema import GetBaseModelStatusValidation
from src.schema.train_model.get_models_schema import GetModelsValidation
from src.schema.train_model.import_base_model_schema import ImportBaseModelSchema, ImportBaseModelValidation
from src.schema.train_model.publish_model_schema import PublishModelSchemaValidation
from src.component.insight import Insight
from src.component.command_parameter_file import CommandParameterFile
from src.component.configuration import Configuration
from src.component.device_command import DeviceCommand
from src.component.file_content_base64data import FileContentBase64

import pytest
import requests,sys

from src.component.deploy import Deploy
from src.component.firmware import Firmware
from src.component.manage_devices import ManageDevices
from src.component.train_model import TrainModel
from src.component.utility import Utility
sys.path.append(".")
# Constant Paramters
MODEL_ID = os.getenv("model_id")
MODEL_SAS = os.getenv("model_url")
DEVICE_ID = os.getenv("device_id")
APPFW_VERSION = os.getenv("MCU_AppFw_version")
SENESOR_LOADER_VERSION = os.getenv("IMX500_Sensor_Loader_version")
SENSOR_VER = os.getenv("IMX500_Sensor_version")
CMD_PARAM_FILE_NAME = os.getenv("command_parameter_file")
CMD_PARAM_FILE = os.getenv("command_parameter_file_cv")
CONFIG_ID = os.getenv("config_id")
FIRMWARE_VER = os.getenv('MCU_AppFw_version')
IMAGE_DIR = os.getenv("IMAGE_DIR")
APP_SASURL = os.getenv("EDGE_APP_URL")
APP_NAME = os.getenv("EDGE_APP_ID")
APP_FILE_NAME = os.getenv("EDGE_APP_FILE_NAME")
APP_VER = os.getenv("EDGE_APP_VERSION")

g_skip = False
converter_model_skip = False

@pytest.fixture()
def SkipCheck():
    global g_skip
    if g_skip:
        pytest.skip("This test is skipped because the firmware version is unchanged.")

@pytest.fixture()
def convert_skip_check():
    global converter_model_skip
    if converter_model_skip:
        pytest.skip("This test is skipped because the model is already converted.")

def test_FW_SkipCheck(device_id=DEVICE_ID, firmware_version=FIRMWARE_VER):
    global g_skip
    check = False
    try:
        for count in range(3):
            response = ManageDevices().get_device(device_id)
            response_data = response.json()        
            if response.status_code == 200:
                for i, module in enumerate(response_data["modules"]):
                    sys_mod_index = i
                    if module["module_id"] == "$system":
                        break
                else:
                    assert(False), "System module not found."
                deploy_pack_version = response_data['modules'][sys_mod_index]['property']['configuration']['PRIVATE_deploy_firmware']['version']
                check = deploy_pack_version == firmware_version
                break
    except KeyError: #The device is initialized.
        check = False
    except:
        assert(False), "For some reason, skip check failed."
    if check:
        g_skip = True

@pytest.mark.create_firmware_1
@pytest.mark.parametrize(
    "firmware_type,version_number,file_name,comment,sas_url",
    [
        pytest.param(
            "00",
            APPFW_VERSION,
            "ota.bin",
            "App_Fw",
            os.getenv("MCU_AppFw_sasurl"),
            marks=pytest.mark.dependency(name='app_firmware'),
        ),
        pytest.param(
            "01",
            SENSOR_VER,
            "sensor.fpk",
            "Sensor_Fw",
            os.getenv("IMX500_Sensor_sasurl"),
            marks=pytest.mark.dependency(name='sensor_firmware'),
        ),
        pytest.param(
            "02",
            SENESOR_LOADER_VERSION,
            "sensor_loader.fpk",
            "Sensor_Loader_Fw",
            os.getenv("IMX500_Sensor_Loader_sasurl"),
            marks=pytest.mark.dependency(name='sensor_loader_firmware'),
        )
]
)
def test_create_firmware(
    firmware_type, version_number, file_name, comment, sas_url
):
    """This test validates the '''Create firmware''' API"""
    firmware_response = Firmware().get_firmware(firmware_type, version_number)
    if firmware_response.status_code == 200:
        pytest.skip("Firmware already exists")
    response = Firmware().create_firmware(
        firmware_type, version_number, file_name, comment, sas_url
    )
    response_data = response.json()
    if response.status_code == 200:
        schema = CreateFirmwareSchemaValidation().create_firmware_positive_schema(
            response_data
        )
    else:
        schema = NegativeSchemaValidation().negative_schema(
            "CreateFirmware", response_data, response.status_code
        )
    print(response_data)
    assert (
        response.status_code == 200 and schema == True
    ) , "Unexpected response."


@pytest.mark.get_firmware_2
@pytest.mark.parametrize(
        "firmware_type,version_number",
        [
            pytest.param(
            "00", APPFW_VERSION, marks=pytest.mark.dependency(depends=['app_firmware'],name='get_app_firmware')
        ),
        pytest.param(
            "01",
            SENSOR_VER,
            marks=pytest.mark.dependency(depends=['sensor_firmware'],name='get_sensor_firmware')
        ),
        pytest.param(
            "02",
            SENESOR_LOADER_VERSION,
            marks=pytest.mark.dependency(depends=['sensor_loader_firmware'],name='get_sensor_loader_firmware')
        )]
)         
def test_get_firmware(SkipCheck,firmware_type, version_number):
    """This test validates Get firmware API"""
    response = Firmware().get_firmware(firmware_type, version_number)
    response_data = response.json()
    response_firmware_type = response_data["firmware_type"]
    response_version_number = response_data["versions"][0]["version_number"]
    if response.status_code == 200:
        schema = GetFirmwareSchemaValidation().get_firmware_positive_schema(
            response_data
            )
    else:
        schema = NegativeSchemaValidation().negative_schema(
            "GetFirmware", response_data, response.status_code
            )
    assert (
        response.status_code == 200 and schema == True
    ), "Unexpected response."
    assert (response_firmware_type, response_version_number) == (
        firmware_type,
        version_number,
    )  # asserting the registered firmware type and version number

@pytest.mark.get_firmware_id_3
def test_import_base_model(model_id=MODEL_ID,model_url=MODEL_SAS):
    """This test validates the '''ImportBaseModel''' API"""
    converted = "False" if ".tflite" in model_url else "True"
    global converter_model_skip
    if converted == "True":
        converter_model_skip = True
    response = TrainModel().import_base_model_setparam(model_id,
                                              model=model_url,
                                              format_param="",
                                              converted=converted,
                                              network_type="1")
    if response.status_code == 200:
        schema = ImportBaseModelValidation().import_base_model_positive_schema(
            response.json()
        )
    else:
        schema = NegativeSchemaValidation().negative_schema(
            "ImportBaseModel", response, response.status_code
        )
    assert(response.status_code == 200 and schema == True), "Unexpected response."

@pytest.mark.get_firmware_id_4
def test_publish_model(convert_skip_check,model_id=MODEL_ID):
    """This function validates publish model API"""
    response = TrainModel().publish_model(model_id)
    response_data = response.json()
    model_status = TrainModel().publish_model_status_check(model_id)
    if response.status_code == 200:
        schema = PublishModelSchemaValidation().publish_model_schema(
            response_data
        )
    else:
        schema = NegativeSchemaValidation().negative_schema(
            "PublishModel", response, response.status_code
        )
    assert(response.status_code == 200 and schema == True), "Unexpected response."
    assert(model_status == "Import completed"), "import failed"

@pytest.mark.get_firmware_id_5
def test_get_base_model_status(model_id=MODEL_ID):
    """This function validates publish model convertion status"""
    response = TrainModel().get_base_model_status(model_id)
    response_data = response.json()
    if response.status_code == 200:
        schema = GetBaseModelStatusValidation().get_base_model_positive_schema(
            response_data
        )
    else:
        schema = NegativeSchemaValidation().negative_schema(
            "GetBaseModelStatus", response, response.status_code
        )
    assert(response.status_code == 200 and schema == True), "Unexpected response."

@pytest.mark.get_firmware_id_6
def test_get_models(model_id=MODEL_ID):
    """This function validates published model in the model list"""
    response = TrainModel().get_models()
    response_data = response.json()
    if response.status_code == 200:
        schema = GetModelsValidation().get_models_positive_schema(
            response_data
        )
    else:
        schema = NegativeSchemaValidation().negative_schema(
            "GetModels", response, response.status_code
        )
    assert(response.status_code == 200 and schema is True), "Unexpected response."
    response_model_id = []
    for model in response_data["models"]:
        response_model_id.append(model["model_id"])
    assert(model_id in response_model_id), "AI modele registration failed."

# @pytest.mark.get_firmware_id_7
# def test_upload_edge_app():
#     """UploadFile edge system software packages."""
#     app_content = requests.get(
#         APP_SASURL, timeout=30).content
#     response = Utility().upload_file(
#         type_code="",
#         file_name=APP_NAME,
#         file_content=app_content)
#     response_data = response.json()
#     print(response_data)
#     if response.status_code == 200:
#         schema = (
#             UploadFileSchemaValidation().upload_file_positive_schema(
#                 response_data
#             )
#         )
#         global file_id_app
#         file_id_app = response_data["file_info"]["file_id"]
#     else:
#         schema = NegativeSchemaValidation().negative_schema(
#             "UploadFile", response_data, response.status_code
#         )
#     assert(response.status_code == 200 and schema is True), "Unexpected response."

@pytest.mark.Customvision_start_and_end_inference_9
def test_import_edge_app():
    """This test validates the '''ImportEdgeApp''' API"""
    response = DeviceApp().import_device_app(
        app_name=APP_NAME,
        app_version=APP_VER,
        description="",
        file_name=APP_FILE_NAME,
        file_content=APP_SASURL,
        compiled_flag="0"
    )
    response_data = response.json()
    if response.status_code == 200:
        schema = ImportEdgeAppSchemaValidation().import_edge_app_positive_schema(
            response_data
        )
    else:
        schema = NegativeSchemaValidation().negative_schema(
            "ImportEdgeApp", response_data, response.status_code
        )
    assert(response.status_code == 200 and schema is True), "Unexpected response."

@pytest.mark.Customvision_start_and_end_inference_10
def test_get_edge_app():
    """This test validates the '''GetEdgeApp''' API"""
    response = DeviceApp().get_edge_app(APP_NAME, APP_VER)
    response_data = response.json()
    if response.status_code == 200:
        schema = GetEdgeAppSchemaValidation().get_edge_app_positive_schema(
            response_data,
        )
    else:
        schema = NegativeSchemaValidation().negative_schema(
            "GetEdgeApp", response_data, response.status_code
        )
    assert(response.status_code == 200 and schema is True), "Unexpected response."
    assert(DeviceApp().edge_app_status_check(APP_NAME, APP_VER) == "2"), "EdgeApp compilation failed."

@pytest.mark.Customvision_start_and_end_inference_11
def test_deploy_edge_app():
    """This test validates the '''DeployEdgeApp''' API"""
    response = DeviceApp().deploy_edge_app(APP_NAME, APP_VER, DEVICE_ID)
    response_data = response.json()
    if response.status_code == 200:
        schema = DeployEdgeAppbyConfigurationSchemaValidation().deploy_by_configuration_positive_schema(
            response_data
        )
    else:
        schema = NegativeSchemaValidation().negative_schema(
            "DeployEdgeApp", response_data, response.status_code
            )
    assert(response.status_code == 200 and schema == True), "Unexpected response."
    deploy_status = None
    counter = 0
    while deploy_status != "success":  # execute until deploy status is equal to 1 within 3 counts
        counter += 1
        deploy_status = DeviceApp().get_deployed_edge_app_status(APP_NAME, APP_VER) \
            # check the deployment status
        if deploy_status != "1":
            DeviceApp().deploy_edge_app(APP_NAME, APP_VER, DEVICE_ID) \
                # execute deploy by configuration again if deployment is not success with 20 mins
        if counter == 3:
            break
    assert(deploy_status == "1"), "Deploy status is not success."

@pytest.mark.get_firmware_id_7
def test_create_command_parameter_file(filename=CMD_PARAM_FILE_NAME, parameter=CMD_PARAM_FILE):
    """This function validates the '''Create command parameter file''' API"""
    response = CommandParameterFile().register_command_parameter_file(
        filename, parameter
    )
    if response.status_code == 200:
        schema = RegisterCommandParameterFileSchemaValidation().register_command_parameter_file_schema(
            response.json()
        )
    else:
        schema = NegativeSchemaValidation().negative_schema(
            "RegisterCommandParameterFile", response, response.status_code
            )
    assert(response.status_code == 200 and schema == True), "Unexpected response."

@pytest.mark.get_firmware_id_8
def test_get_command_parameter_file():
    """This function validates the '''Get command parameter file''' API"""
    response = CommandParameterFile().get_command_parameter_file()
    response_data = response.json()
    print(response_data)
    for parameter in response_data["parameter_list"]:
        if parameter["file_name"] == CMD_PARAM_FILE_NAME:
            assert(parameter["file_name"] == CMD_PARAM_FILE_NAME), "Unexpected response."
            break
    else:
        assert(False), "Command parameter file not found."
    if response.status_code == 200:
        schema = GetCommandParameterFileSchemaValidation().get_command_parameter_file_positive_schema(
            response.json()
        )
    else:
        schema = NegativeSchemaValidation().negative_schema(
            "RegisterCommandParameterFile", response, response.status_code
        )
    assert(response.status_code == 200 and schema == True), "Unexpected response."

@pytest.mark.get_firmware_id_9
def test_create_deploy_configuration():
    """This function validates the '''Create deploy configuration''' API"""
    response = Deploy().create_deploy_configuration(CONFIG_ID,
        SENESOR_LOADER_VERSION,
        SENSOR_VER,
        APPFW_VERSION,
        MODEL_ID)
    response_data = response.json()
    if response.status_code == 200:
        schema = CreateDeployConfigurationSchemaValidation().create_deploy_configuration_positive_schema(
            response_data
        )
    else:
        schema = NegativeSchemaValidation().negative_schema(
            "CreateDeployConfiguration", response, response.status_code)
    assert(response.status_code == 200 and schema == True), "Unexpected response."

@pytest.mark.get_firmware_id_10
def test_get_deploy_configuration():
    """This function validates the '''Get deploy configuration''' API"""
    response = Deploy().get_deploy_configuration(CONFIG_ID)
    response_data = response.json()
    if response.status_code == 200:
        schema = GetDeployConfigSchemaValidation().get_deply_config_positive_schema(
            response_data, CONFIG_ID, APPFW_VERSION, SENESOR_LOADER_VERSION, SENSOR_VER, MODEL_ID
        )
    else:
        schema = NegativeSchemaValidation().negative_schema(
            "GetDeployConfiguration", response_data, response.status_code
        )
    assert(response.status_code == 200 and schema == True), "Unexpected response."

def deploy_by_cofiguration_func(conf, dev):
    """This function deploys the configuration"""
    response = Deploy().deploy_by_configuration(conf, dev)
    response_data = response.json()
    if response.status_code == 200:
        schema = DeploybyConfigurationSchemaValidation().deploy_by_configuration_positive_schema(
            response_data
        )
    else:
        schema = NegativeSchemaValidation().negative_schema(
            "DeployByConfiguration", response_data, response.status_code
        )
    assert(response.status_code == 200 and schema == True), "Unexpected response."
    deploy_status = None
    counter = 0
    while deploy_status != "1":  # execute until deploy status is equal to 1 within 3 counts
        counter += 1
        deploy_status = Deploy().deployment_status_check(dev) \
            # check the deployment status
        if deploy_status != "1":
            deploy_by_cofiguration_func(conf, dev) \
                # execute deploy by configuration again if deployment is not success with 20 mins
        if counter == 3:
            break
    assert(deploy_status == "1"), "Deploy status is not success."

def get_device(device_id):
    """This function retrieves the device information"""
    time.sleep(10)
    device_responce = ManageDevices().get_device(device_id)
    if device_responce.status_code == 200:
        schema = GetDeviceSchemaValidation().get_device_positive_schema(
            device_responce.json()
        )
    else:
        schema = NegativeSchemaValidation().negative_schema(
            "GetDevice", device_responce.json(), device_responce.status_code
        )
    assert(device_responce.status_code == 200 and schema == True), "Unexpected response."
    device_data = device_responce.json()
    print("get_device",device_data)
    return device_data

@pytest.mark.get_firmware_id_11
def test_deploy_by_configuration():
    """This function validates the '''Deploy by configuration''' API"""
    deploy_by_cofiguration_func(CONFIG_ID, DEVICE_ID)

@pytest.mark.get_firmware_id_12
def test_get_deploy_history():
    """This function validates the '''Get deploy history''' API"""
    response = Deploy().get_deploy_history(DEVICE_ID)
    response_data = response.json()
    if response.status_code == 200:
        schema = GetDeployHistorySchemaValidation().get_deploy_history_positive_schema(
            response_data
        )
    else:
        schema = NegativeSchemaValidation().negative_schema(
            "GetDeployHistory", response_data, response.status_code
        )
    assert(response.status_code == 200 and schema == True), "Unexpected response."

@pytest.mark.get_firmware_id_13
def test_bind_command_parameter_file_to_device():
    """This function validates the '''Bind command parameter file to device''' API"""
    response = CommandParameterFile().bind_command_parameter_file_to_device(
        CMD_PARAM_FILE_NAME, DEVICE_ID
    )
    if response.status_code == 200:
        schema = BindCommandParameterFileToDeviceSchemaValidation().bind_command_parameter_file_to_device_schema(
            response.json()
        )
    else:
        schema = NegativeSchemaValidation().negative_schema(
            "BindCommandParameterFileToDevice", response, response.status_code
        )
    assert(response.status_code == 200 and schema == True), "Unexpected response."

@pytest.mark.get_firmware_id_14
def test_get_command_parameter_file():
    """This function validates the '''Get command parameter file''' API"""
    response = CommandParameterFile().get_command_parameter_file()
    response_data = response.json()
    for parameter in response_data["parameter_list"]:
        if parameter["file_name"] == CMD_PARAM_FILE_NAME:
            assert(parameter["device_ids"][0] == DEVICE_ID), "Unexpected response."
            break
    else:
        assert(False), "Command parameter file not found or not binded to the device."
    assert(response.status_code == 200), "Unexpected response."

@pytest.mark.get_firmware_id_15
def test_inference_start():
    """This function validates the '''Inference start''' API"""
    device_data = get_device(DEVICE_ID)
    status = device_data["state"]["Status"]["Sensor"]
    if status == "Streaming":
        DeviceCommand().stop_upload_inference_result(DEVICE_ID)
    time.sleep(5)
    response = DeviceCommand().start_upload_inference_result(DEVICE_ID)
    if response.status_code == 200:
        schema = StartUploadInferenceResultSchemaValidation().start_upload_inference_result_schema(
            response.json()
        )
    else:
        schema = NegativeSchemaValidation().negative_schema(
            "StartUploadInferenceResult", response, response.status_code
        )
    time.sleep(30)
    global GetDataTime
    GetDataTime = datetime.now(timezone.utc)
    assert(response.status_code == 200 and schema == True), "Unexpected response."

@pytest.mark.get_firmware_id_16
def test_get_device():
    """This function validates the '''Get device''' API"""
    device_data = get_device(DEVICE_ID)
    status = device_data["state"]["Status"]["Sensor"]
    assert(status == "Streaming"), "Unexpected response."

@pytest.mark.get_firmware_id_17
def test_inference_stop():
    """This function validates the '''Inference stop''' API"""
    response = DeviceCommand().stop_upload_inference_result(DEVICE_ID)
    if response.status_code == 200:
        schema = StopUploadInferenceResultSchemaValidation().stop_upload_inference_result_schema(
            response.json()
        )
    else:
        schema = NegativeSchemaValidation().negative_schema(
            "StopUploadInferenceResult", response, response.status_code
        )
    assert(response.status_code == 200 and schema == True), "Unexpected response."

@pytest.mark.get_firmware_id_18
def test_get_inference_results(device_id=DEVICE_ID,
                              save_image_dir=IMAGE_DIR):
    """This test validates '''Get inference data Check''' """
    res_get_image = Insight().get_images_of_last_page(device_id, save_image_dir)
    assert(res_get_image.status_code == 200), "Unexpected response."
    assert("data" in res_get_image.json() and 
           len(res_get_image.json()["data"]) > 0), "Image data not found"    
    latest_image_date_str = os.path.splitext(res_get_image.json()["data"][-1]["name"])[0]
    latest_image_date = datetime.strptime(latest_image_date_str, "%Y%m%d%H%M%S%f").replace(tzinfo=timezone.utc)
    image_delta_time = (latest_image_date - GetDataTime).total_seconds()
    res_get_meta_id = Insight().get_inference_results(device_id)
    latest_meta_id = res_get_meta_id.json()["data"][0]["id"]
    res_get_meta = Insight().get_inference_result(DEVICE_ID, latest_meta_id)
    assert(res_get_meta.status_code == 200), "Unexpected response."
    latest_meta_date_str = res_get_meta.json()["Inferences"][0]["T"]
    latest_meta_date = datetime.strptime(latest_meta_date_str, "%Y%m%d%H%M%S%f").replace(tzinfo=timezone.utc)
    meta_delta_time = (latest_meta_date - GetDataTime).total_seconds()
    assert(meta_delta_time >= 0), "No meta data retrieved from the last inference."
    assert(image_delta_time >= 0), "No image data retrieved from the last inference."

@pytest.mark.get_firmware_id_19
def test_unbind_command_parameter_file_to_device():
    """This function validates the '''Unbind command parameter file to device''' API"""
    response = CommandParameterFile().unbind_command_parameter_file_to_device(
        CMD_PARAM_FILE_NAME, DEVICE_ID
    )
    assert(response.status_code == 200), "Unexpected response."
    