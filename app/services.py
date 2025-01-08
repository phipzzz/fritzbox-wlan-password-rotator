from app.config import (
    FB_ADDRESS, 
    FB_USER, 
    FB_PASSWORD, 
    WLAN_CONFIGURATION
)
from fritzconnection import FritzConnection

fc = FritzConnection(address = FB_ADDRESS, user = FB_USER, password = FB_PASSWORD)

def set_new_password(psk, passphrase):

    security_keys = {
        "NewWEPKey0": "",
        "NewWEPKey1": "",
        "NewWEPKey2": "",
        "NewWEPKey3": "",
        "NewPreSharedKey": psk,
        "NewKeyPassphrase": passphrase
    }

    try:
        fc.call_action(WLAN_CONFIGURATION, "SetSecurityKeys", **security_keys)
    except Exception as e:
        print(f"Error: {e}")

def get_current_password():

    try:
        data = fc.call_action(WLAN_CONFIGURATION, "GetSecurityKeys")
        return data["NewKeyPassphrase"]
    except Exception as e:
        print(f"Error: {e}")

def get_ssid():

    try:
        data = fc.call_action(WLAN_CONFIGURATION, "GetSSID")
        return data["NewSSID"]
    except Exception as e:
        print(f"Error: {e}")