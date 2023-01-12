"""Nodules providing system operations"""
import json
import requests
from requests.auth import HTTPBasicAuth

import pandas as pd

from jira_connector.model.jira_user import JiraUser
from jira_connector.service.jira_data_process import process_issue


def jira_issue_search(user: JiraUser, jql: str, fields: list, jira_url: str) -> any:
    """
    Get issues from jql search result with all related fields
    :param user:
    :param jql:
    :param fields: list of fields, for example: ['priority', 'summary', 'customfield_10007']
    :return
    """

    auth = HTTPBasicAuth(user.jira_username, user.jira_access_token)

    url = user.jira_url + "search"

    headers = {
        "Accept": "application/json"
    }

    fields = None
    params = {}
    # if start is not None:
    #     params["startAt"] = int(start)
    # if limit is not None:
    #     params["maxResults"] = int(limit)
    if fields is not None:
        if isinstance(fields, (list, tuple, set)):
            fields = ",".join(fields)
        params["fields"] = fields
    if jql is not None:
        params["jql"] = jql
    # if expand is not None:
    #     params["expand"] = expand
    # if validate_query is not None:
    #     params["validateQuery"] = validate_query

    response = requests.request(
        "GET",
        url,
        headers=headers,
        params=params,
        auth=auth,
        timeout=100
    )

    data = json.loads(response.text)

    dataframe = pd.DataFrame()

    for issue in data["issues"]:
        issue_dataframe = process_issue(issue, jira_url)
        dataframe = pd.concat([dataframe, issue_dataframe], ignore_index=True)

    return dataframe


if __name__ == "__main__":
    pass
