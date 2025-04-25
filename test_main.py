import pytest
import os
from collections import defaultdict
from io import StringIO
from unittest.mock import patch

from main import parse_log_file, extract_handler_from_message, parse_logs, generate_handlers_report

def test_extract_handler_from_message():
    assert extract_handler_from_message("/api/v1/auth/login/") == "/api/v1/auth/login/"
    assert extract_handler_from_message("/api/v1/products/") == "/api/v1/products/"

    assert extract_handler_from_message("Error: Internal Server Error") is None
    assert extract_handler_from_message("django.request: /admin/login/") is None

def test_parse_log_file_correct():
    log_content = """
2025-03-26 12:14:43,000 INFO django.request: /api/v1/auth/login/ [192.168.1.95]
2025-03-26 12:15:43,000 ERROR django.request: Internal Server Error: /admin/login/ [192.168.1.95]
2025-03-26 12:16:43,000 INFO django.request: /api/v1/products/ [192.168.1.95]
    """
    
    with patch("builtins.open", return_value=StringIO(log_content)):
        total_requests, handler_data = parse_log_file("test_log.log")

    assert total_requests == 2  
    assert handler_data["/api/v1/auth/login/"]["INFO"] == 1
    assert handler_data["/api/v1/products/"]["INFO"] == 1

def test_parse_log_file_no_requests():
    log_content = """
2025-03-26 12:14:43,000 INFO django.request: /admin/dashboard/ [192.168.1.95]
2025-03-26 12:15:43,000 ERROR django.request: Internal Server Error: /admin/login/ [192.168.1.95]
    """
    
    with patch("builtins.open", return_value=StringIO(log_content)):
        total_requests, handler_data = parse_log_file("test_log.log")

    assert total_requests == 0
    assert len(handler_data) == 0

def test_parse_logs_multiple_files():
    log_content_1 = """
2025-03-26 12:14:43,000 INFO django.request: /api/v1/auth/login/ [192.168.1.95]
"""
    log_content_2 = """
2025-03-26 12:15:43,000 INFO django.request: /api/v1/products/ [192.168.1.95]
    """
    
    with patch("builtins.open", side_effect=[StringIO(log_content_1), StringIO(log_content_2)]):
        total_requests, handler_data = parse_logs(["log1.log", "log2.log"])

    assert total_requests == 2
    assert handler_data["/api/v1/auth/login/"]["INFO"] == 1
    assert handler_data["/api/v1/products/"]["INFO"] == 1

@patch("sys.stdout", new_callable=StringIO)
def test_generate_handlers_report(mock_stdout):
    handler_data = {
        "/api/v1/auth/login/": {"INFO": 2, "DEBUG": 1},
        "/api/v1/products/": {"INFO": 1},
    }
    total_requests = 3
    generate_handlers_report(total_requests, handler_data)

    output = mock_stdout.getvalue()
    assert "Total requests: 3" in output
    assert "/api/v1/auth/login/" in output
    assert "INFO" in output
    assert "DEBUG" in output
    assert "/api/v1/products/" in output


def test_generate_report_headers():
    handler_data = {
        "/api/v1/auth/login/": {"INFO": 1},
    }
    total_requests = 1
    with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
        generate_handlers_report(total_requests, handler_data)
        output = mock_stdout.getvalue()

    assert "HANDLER" in output
    assert "DEBUG" in output
    assert "INFO" in output
    assert "WARNING" in output
    assert "ERROR" in output
    assert "CRITICAL" in output

if __name__ == "__main__":
    pytest.main()
