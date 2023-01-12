"""Module providing data types"""
from dataclasses import dataclass


@dataclass
class SmartsheetUser:
    """Jira user class"""
    smartsheet_username: str
    smartsheet_access_token: str
    smartsheet_url: str
