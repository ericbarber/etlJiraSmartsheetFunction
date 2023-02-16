"""Module providing logging"""
import logging
import json

from job_builder.model.job import Job


def create_job_object(job: dict) -> Job:
    """Build a job object
    input: json
    output: Job
    """
    job_object = Job(
        job["id"],
        job["name"],
        job["jira_url"],
        job["jira_api"],
        job["jira_query"],
        job["jira_fields"],
        job["max_results"],
        job["target_sheet_id"],
        job["smartsheet_url"]
    )
    return job_object


def build_job_processing_dict(jobs: dict) -> dict:
    """Build a dictionary of all jobs listed in jobs.json
    input: json
    output: dict
    """
    return {job["id"]: create_job_object(job) for job in jobs}


def read_json_jobs(filepath: str) -> None:
    """Read jobs data from json file
    input: filepath str
    output: json
    """
    try:
        with open(filepath, "r", encoding="ascii") as json_file:
            data = json.load(json_file)
        return data["jobs"]

    except json.decoder.JSONDecodeError as err:
        logging.error("An error occurred while parsing the JSON file: %s", err)
        raise err

    except FileNotFoundError as err:
        logging.error("The file could not be found: %s", err)
        raise err

    except KeyError as err:
        logging.error("The jobs key is missing in the json file: %s", err)
        raise err


def validate_job_id(job: Job):
    """Check for Job element: id"""
    if not job.id:
        message = f"Jod ID: {job} does not contain an id.  Add id field type string to job in jobs.json file. (example: 'id': 'newIDString')"
        raise KeyError(message)


def job_validator(func):
    """Process Job object and validate correct structure"""
    def _processor(job):
        validate_job_id(job)
        return func(job)


@job_validator
def build_job(job: Job) -> None:
    """Validate the job"""
