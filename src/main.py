"""Module providing logging"""
import logging
import logger
from job_builder.service.job import read_json_jobs, build_job_processing_dict

from jira_connector.service.jira_api_v3 import jira_issue_search
from jira_connector.service.jira_user import build_jira_user, valid_user

from smartsheet_connector.service.smartsheet_build import smartsheets_data_load


def main() -> None:

    # load data from jobs.json file
    FILEPATH = "./jobs.json"
    jobs = read_json_jobs('jobs.json')

    if jobs:
        # jobs data processing
        logging.info('Jobs details loaded from %s', FILEPATH)

        # validate jobs
        job_processing_dict = build_job_processing_dict(jobs)
        logging.info('Number of jobs to be processed: %s',
                     len(job_processing_dict))

        logging.info('Jobs ready for jira api')

    else:
        # handle the error
        logging.info('Jobs details did not load')

    try:
        jira_user = build_jira_user()

        if not valid_user(jira_user):
            raise EnvironmentError(
                f'Jira Access Issue: Jira User {jira_user.jira_username}: Not able to access system, may not even exits.')

    except Exception as err:
        raise err

    if job_processing_dict:

        for index, job in job_processing_dict.items():

            try:
                job_jira_datafram = jira_issue_search(
                    jira_user, job.jira_query, job.jira_fields, job.jira_url)

                smartsheets_data_load(
                    job_jira_datafram, job.target_sheet_id)

            except Exception as err:
                raise err


if __name__ == "__main__":
    main()
