"""Module providing data types"""
from dataclasses import dataclass


@dataclass
class JiraUser:
    """Jira user class"""
    jira_username: str
    jira_access_token: str
    jira_url: str
