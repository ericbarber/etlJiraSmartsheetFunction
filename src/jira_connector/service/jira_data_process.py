"""Module providing data frame operations"""
import pandas as pd

# import jr.jira_percent_complete


def process_issue(issue, url) -> pd.DataFrame:
    """Process data from json object"""
    issue_dict = dict()

    issue_dict["self"] = issue.get("self").strip()

    issue_dict["issue"] = url+"browse/"+issue.get("key").strip()

    issue_dict["id"] = issue.get("id").strip()
    issue_dict["key"] = issue.get("key").strip()

    issue_dict["assignee"] = issue.get("fields", {}).get(
        "assignee", {}).get("emailAddress")

    issue_dict["summary"] = issue.get("fields", {}).get("summary", {}).strip()

    # issue_dict["project_key"]   = issue.get("fields", {}).get("project", {}).get("key").strip()
    # issue_dict["project_id"]    = issue.get("fields", {}).get("project", {}).get("id").strip()
    # issue_dict["project_name"]  = issue.get("fields", {}).get("project", {}).get("name").strip()

    issue_dict["status_id"] = issue.get(
        "fields", {}).get("status").get("id").strip()
    issue_dict["status_name"] = issue.get(
        "fields", {}).get("status").get("name").strip()

    # issue_dict["percent_complete"] = jr.jira_percent_complete.status_lookup(
    #     issue["fields"]["status"]["name"], status_to_percent)

    issue_dataframe = pd.DataFrame([issue_dict])

    return issue_dataframe


if __name__ == "__main__":
    pass
