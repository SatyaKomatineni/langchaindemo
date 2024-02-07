import baselog as log
import fileutils as fileutils

def getHFAPIKey():
    API_Env_key = "HUGGINGFACE_API_KEY"
    API_Key = fileutils.getEnvVariable(API_Env_key, None)
    if API_Key == None:
        raise Exception(f"No api key found in environment:{API_Env_key}")
    return API_Key

def get_FB_HFAPIKey():
    API_Env_key = "FB_HUGGINGFACE_API_KEY"
    API_Key = fileutils.getEnvVariable(API_Env_key, None)
    if API_Key == None:
        raise Exception(f"No api key found in environment:{API_Env_key}")
    return API_Key

def getSampleHFEndPoint():
    return "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"

def getFB_HF_LLM_Endpoint():
    return "https://z8dvl7fzhxxcybd8.eu-west-1.aws.endpoints.huggingface.cloud/"
