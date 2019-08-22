"""Axe accessibility analysis metric source."""

import csv
import hashlib
from io import StringIO
import re
from typing import List

import requests

from utilities.type import Value, Entities
from .source_collector import SourceCollector


class AxeCSVAccessibility(SourceCollector):
    """Collector class to get accessibility violations."""

    def parse_source_responses_value(self, responses: List[requests.Response]) -> Value:
        """Simply count the rows in the csv file."""
        return str(len(list(self.__parse_csv(responses[0]))))

    def parse_source_responses_entities(self, responses: List[requests.Response]) -> Entities:
        """Convert csv rows of the Axe report into entities, in this case accessibility violations."""
        return [
            dict(
                key=hashlib.md5(str(row).encode('utf-8')).hexdigest(),  # nosec
                violation_type=row["Violation Type"], impact=row["Impact"], url=str(row["URL"]),
                element=row["DOM Element"], page=re.sub(r'http[s]?://[^/]+', '', row['URL']),
                description=row["Messages"], help=row["Help"])
            for row in self.__parse_csv(responses[0])]

    @staticmethod
    def __parse_csv(response: requests.Response) -> csv.DictReader:
        """Parse the CSV and return the row iterator."""
        return csv.DictReader(StringIO(response.text, newline=None))
