"""Unit tests for the Bandit source."""

from datetime import datetime
import unittest
from unittest.mock import Mock, patch

from src.collector import MetricCollector


class BanditTest(unittest.TestCase):
    """Unit tests for the security warning metric."""

    def setUp(self):
        self.mock_response = Mock()
        self.mock_response.json = Mock(
            return_value=dict(
                generated_at="2019-07-12T07:38:47Z",
                results=[
                    dict(
                        filename="src/collectors/cxsast.py",
                        issue_confidence="MEDIUM",
                        issue_severity="LOW",
                        issue_text="Possible hardcoded password: '014DF517-39D1-4453-B7B3-9930C563627C'",
                        line_number=37,
                        more_info="https://bandit/b106_hardcoded_password_funcarg.html",
                        test_id="B106",
                        test_name="hardcoded_password_funcarg")]))
        self.sources = dict(source_id=dict(type="bandit", parameters=dict(url="bandit.json")))

    def test_warnings(self):
        """Test the number of security warnings."""
        metric = dict(type="security_warnings", sources=self.sources, addition="sum")
        with patch("requests.get", return_value=self.mock_response):
            response = MetricCollector(metric).get()
        self.assertEqual("1", response["sources"][0]["value"])
        self.assertEqual(
            [dict(
                location="src/collectors/cxsast.py:37", key="B106:src/collectors/cxsast.py:37",
                issue_text="Possible hardcoded password: '014DF517-39D1-4453-B7B3-9930C563627C'",
                issue_severity="Low", issue_confidence="Medium",
                more_info="https://bandit/b106_hardcoded_password_funcarg.html")],
            response["sources"][0]["entities"])

    def test_warnings_with_high_severity(self):
        """Test the number of high severity security warnings."""
        self.sources["source_id"]["parameters"]["severities"] = ["high"]
        metric = dict(type="security_warnings", sources=self.sources, addition="sum")
        with patch("requests.get", return_value=self.mock_response):
            response = MetricCollector(metric).get()
        self.assertEqual("0", response["sources"][0]["value"])
        self.assertEqual([], response["sources"][0]["entities"])

    def test_warnings_with_high_confidence(self):
        """Test the number of high confidence security warnings."""
        self.sources["source_id"]["parameters"]["confidence_levels"] = ["high"]
        metric = dict(type="security_warnings", sources=self.sources, addition="sum")
        with patch("requests.get", return_value=self.mock_response):
            response = MetricCollector(metric).get()
        self.assertEqual("0", response["sources"][0]["value"])
        self.assertEqual([], response["sources"][0]["entities"])

    def test_source_up_to_dateness(self):
        """Test that the source age in days is returned."""
        metric = dict(type="source_up_to_dateness", sources=self.sources, addition="max")
        with patch("requests.get", return_value=self.mock_response):
            response = MetricCollector(metric).get()
        expected_age = (datetime.now() - datetime(2019, 7, 12, 7, 38, 47)).days
        self.assertEqual(str(expected_age), response["sources"][0]["value"])