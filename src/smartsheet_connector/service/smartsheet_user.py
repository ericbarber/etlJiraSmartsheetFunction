"""Modules providing system operations"""
import os
from dotenv import load_dotenv

from smartsheet_connector.model.smartsheet_user import SmartsheetUser


def build_smartsheet_user() -> SmartsheetUser:
    """Load user details from .env file located in app root"""
    load_dotenv()
    smartsheet_username = os.environ.get("USERNAMESMARTSHEET")
    smartsheet_access_token = os.environ.get("USERKEYSMARTSHEET")
    smartsheet_url = os.environ.get("USERURLSMARTSHEET")

    return SmartsheetUser(smartsheet_username, smartsheet_access_token, smartsheet_url)
