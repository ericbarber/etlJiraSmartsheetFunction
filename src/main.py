"""Module providing logging"""
import logging
import logger
import pandas as pd

from job_builder.service.job import read_json_jobs, build_job_processing_dict

from jira_connector.service.jira_api_v3 import jira_issue_search
from jira_connector.model.jira_user import JiraUser
from jira_connector.service.jira_user import build_jira_user, valid_user
from jira_connector.service.jira_data_process import process_issue

from smartsheet_connector.service.smartsheet_build import smartsheets_data_load


def get_jira_data(
    jira_user: JiraUser,
    job: dict,
    start: int,
    limit: int
) -> None:
    """Query data from Jira"""

    job_jira_data = jira_issue_search(
        jira_user,
        job.jira_query,
        job.jira_fields,
        start,
        limit
    )

    query_total_results = int(job_jira_data["total"])

    dataframe = pd.DataFrame()

    for issue in job_jira_data["issues"]:
        issue_dataframe = process_issue(issue, job.jira_url)

        dataframe = pd.concat(
            [dataframe, issue_dataframe],
            ignore_index=True
        )

    query_result = dataframe

    return query_total_results, query_result


def main() -> None:
    """Main function"""

    # load data from jobs.json file
    file_path = "./jobs.json"
    jobs = read_json_jobs('jobs.json')

    if jobs:
        # jobs data processing
        logging.info('Jobs details loaded from %s', file_path)

        # validate jobs
        job_processing_dict = build_job_processing_dict(jobs)
        logging.info('Number of jobs to be processed: %s',
                     len(job_processing_dict))

    else:
        # handle the error
        logging.info('Jobs details did not load')

    try:
        # build jira user for api query
        jira_user = build_jira_user()

        if not valid_user(jira_user):
            raise EnvironmentError(
                f"""Jira Access Issue: Jira User {jira_user.jira_username}: \
Not able to access system, may not even exits.""")

    except Exception as err:
        raise err

    # process data from query
    if job_processing_dict:

        for _, job in job_processing_dict.items():
            _start = 0
            _limit = job.max_results
            issues_processed = 0

            try:
                query_total_results, query_result = get_jira_data(
                    jira_user=jira_user,
                    job=job,
                    start=_start,
                    limit=_limit
                )

                # send first batch to smartsheet
                smartsheets_data_load(
                    query_result,
                    job.target_sheet_id
                )

                # counter for issues processed by pagination
                issues_processed = issues_processed + issues_processed

                if query_total_results > _limit:
                    logging.debug("PAGINATION REQUIRED")
                    paginate_data = True

                while paginate_data:
                    _start = _limit + _start
                    if _start > query_total_results:
                        logging.debug("PAGINATION COMPLETE")
                        paginate_data = False
                        continue
                    query_total_results, query_result = get_jira_data(
                        jira_user=jira_user,
                        job=job,
                        start=_start,
                        limit=_limit
                    )

                    # send paginatied batch to smartsheet
                    smartsheets_data_load(
                        query_result,
                        job.target_sheet_id
                    )

            except Exception as err:
                raise err


if __name__ == "__main__":
    main()
