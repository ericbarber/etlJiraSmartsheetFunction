"""Module providing data frame operations"""
import pandas as pd

# import jr.jira_percent_complete


def process_issue(issue, url):
    """Process data from json object"""
    issue_dict = dict()

    issue_dict["self"] = issue["self"].strip()
    issue_dict["issue"] = url+"browse/"+issue["key"].strip()

    issue_dict["id"] = issue["id"].strip()
    issue_dict["key"] = issue["key"].strip()

    if (issue["fields"]["assignee"]):
        issue_dict["assignee"] = issue["fields"]["assignee"]["emailAddress"].strip()
    else:
        issue_dict["assignee"] = None

    issue_dict["summary"] = issue["fields"]["summary"].strip()

    # issue_dict["project_key"]   = issue["fields"]["project"]["key"].strip()
    # issue_dict["project_id"]    = issue["fields"]["project"]["id"].strip()
    # issue_dict["project_name"]  = issue["fields"]["project"]["name"].strip()

    issue_dict["status_id"] = issue["fields"]["status"]["id"].strip()
    issue_dict["status_name"] = issue["fields"]["status"]["name"].strip()

    # issue_dict["percent_complete"]   = jr.jira_percent_complete.status_lookup(issue["fields"]["status"]["name"], status_to_percent)

    issue_dataframe = pd.DataFrame([issue_dict])

    return issue_dataframe


if __name__ == "__main__":
    print("Neat")
