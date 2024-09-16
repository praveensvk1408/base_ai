
import os
import pytest

def pytest_configure(config):
    os.environ['REST_API_URL'] = "https://scs.saas-sqa2-t3p.scs-app-jpeast.com/api/v1"
    os.environ['model_id'] = "TS1_SI2_1.7.0"
    os.environ['device_id'] = "Aid-80010003-0000-2000-9002-00000000031b"
    os.environ['MCU_AppFw_version'] = "0700F9"
    os.environ['MCU_AppFw_sasurl'] = "https://sardbaseai.blob.core.windows.net/fwai/ts1si2/Camera/T3W/AIH-IVRW2_20231019_00_030007_010701_020301/ota.bin?sp=r&st=2024-09-16T05:53:56Z&se=2024-12-31T13:53:56Z&spr=https&sv=2022-11-02&sr=b&sig=UFsjZG5jNmoXQteUMG8ZqWTOJQfpOfF1%2FEM05IhQkqg%3D"
    os.environ['IMX500_Sensor_Loader_version'] = "020301"
    os.environ['IMX500_Sensor_Loader_sasurl'] = "https://sardbaseai.blob.core.windows.net/fwai/ts1si2/Camera/T3W/AIH-IVRW2_20231019_00_030007_010701_020301/loader.fpk?sp=r&st=2024-09-16T05:55:45Z&se=2024-12-31T13:55:45Z&spr=https&sv=2022-11-02&sr=b&sig=AdBI2c%2BYDv5ALs6iSLscfKyn7uI02rWcJM62RFObLiY%3D"
    os.environ['IMX500_Sensor_version'] = "010707"
    os.environ['IMX500_Sensor_sasurl'] = "https://sardbaseai.blob.core.windows.net/fwai/ts1si2/Camera/T3W/AIH-IVRW2_20231019_00_030007_010701_020301/firmware.fpk?sp=r&st=2024-09-16T05:55:04Z&se=2024-12-31T13:55:04Z&spr=https&sv=2022-11-02&sr=b&sig=ZoSB7i0YKRR5sI5HkBoUHKmjJR0UIdvcCThkLENddXQ%3D"
    os.environ['command_parameter_file'] = "HumanDetectionAttribution_WASMStep3.json"
    os.environ["command_parameter_file_cv"] = "https://sardbaseai.blob.core.windows.net/fwai/ts1si2/CommandParameterFile/HumanDetectionAttribution_WASMStep3.json?sp=r&st=2024-09-16T06:16:58Z&se=2024-12-31T14:16:58Z&spr=https&sv=2022-11-02&sr=b&sig=A7OXLqcyz8tQ1eBLtwjgGkziekNrLx15oyPO1B3Rydg%3D"
    os.environ['config_id'] = "App_config"
    os.environ['model_url'] = "https://sardbaseai.blob.core.windows.net/fwai/ts1si2/AI-Model/packerOut.zip?sp=r&st=2024-09-16T05:56:27Z&se=2024-12-31T13:56:27Z&spr=https&sv=2022-11-02&sr=b&sig=22tO4l2TErsxGZsR9tDPG6oE68eiOKxpZh89R%2B1oJYM%3D"
    os.environ['IMAGE_DIR'] = '20240807065739939'
    os.environ['EDGE_APP_ID'] = 'APP_WSAM'
    os.environ['EDGE_APP_FILE_NAME'] = 'vision_app.4.0.7.wasm'
    os.environ["EDGE_APP_URL"] = "https://sardbaseai.blob.core.windows.net/fwai/ts1si2/WasmApp/vision_app.4.0.7.wasm?sp=r&st=2024-09-16T05:58:53Z&se=2024-12-31T13:58:53Z&spr=https&sv=2022-11-02&sr=b&sig=cKvnH%2Br3GPkvADsQMIoC1A3R2%2B1zLPYeio3tTNkLcVI%3D"
    os.environ['EDGE_APP_VERSION'] = '4.0.7'
