from pathlib import Path

import requests_mock

from tempfile import TemporaryDirectory
from page_loader import download


def test_download():
    expected_text = "Test data"
    expected_name = "ru-hexlet-io-courses.html"
    with requests_mock.Mocker() as rmock:
        rmock.get("https://ru.hexlet.io/courses", text=expected_text)
        with TemporaryDirectory() as tempdir:
            received = Path(download("https://ru.hexlet.io/courses", tempdir))
            received_text = received.read_text(encoding='utf-8')
            assert received_text == expected_text
    assert received.name == expected_name
