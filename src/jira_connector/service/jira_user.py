"""Modules providing system operations"""
import os
from dotenv import load_dotenv
import requests
from requests.auth import HTTPBasicAuth

from jira_connector.model.jira_user import JiraUser


def build_jira_user() -> JiraUser:
    """Load user details from .env file located in app root"""
    load_dotenv()
    jira_username = os.environ.get("USERNAMEJIRA")
    jira_access_token = os.environ.get("USERKEYJIRA")
    jira_url = os.environ.get("USERURLJIRA")

    return JiraUser(jira_username, jira_access_token, jira_url)


def valid_user(user: JiraUser) -> bool:
    """Validate user access by querying user details"""
    url = user.jira_url + "myself"

    auth = HTTPBasicAuth(user.jira_username, user.jira_access_token)

    headers = {
        "Accept": "application/json"
    }

    response = requests.request(
        "GET",
        url,
        headers=headers,
        auth=auth,
        timeout=10
    )

    if response.status_code == 200:
        return True
    return False


if __name__ == "__main__":
    valid_user(build_jira_user())
