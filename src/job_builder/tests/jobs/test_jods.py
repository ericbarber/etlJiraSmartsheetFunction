# https://github.com/karthi2103/pytest_test_data_handler/blob/main/tests/email/test_email.py
import json
import os
import pytest
from pathlib import Path

from jira_connector.service.job import read_json_jobs
from jira_connector.tests.util.data_resolver import inject_test_data


def test_jobs_json_file_exists():
    path = Path('./jobs.json')
    assert path.is_file(), f'File path for jobs.json is incorrect, or file is missing.'


class TestData:
    test_data = inject_test_data(file="jobs/jobsTestSet.json")

    # test function
    @pytest.mark.parametrize("input", test_data.happyPath)
    def test_read_json_jobs(self, input):
        """Check for all fields and types"""
        pass
