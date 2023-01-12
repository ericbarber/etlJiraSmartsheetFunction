"""Module providing data types"""
from dataclasses import dataclass


@dataclass
class Job:
    """Job dataclass"""
    job_id: str
    name: str
    jira_url: str
    jira_api: str
    jira_query: str
    jira_fields: list
    max_results: int
    target_sheet_id: str
    smartsheet_url: str
