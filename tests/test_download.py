from tempfile import TemporaryDirectory

import pytest
import requests_mock

from page_loader import download
from page_loader.logging import PathAccessError, ConnectionError

# TODO: Check links were changed
# TODO:


def test_download():
    expected_text = "Test data"
    expected_name = "ru-hexlet-io-professions.html"
    with requests_mock.Mocker() as rmock:
        rmock.get("https://ru.hexlet.io/professions", text=expected_text)
        with TemporaryDirectory() as tempdir:
            local_page, _ = download(
                "https://ru.hexlet.io/professions", tempdir)
            received_text = local_page.read_text(encoding='utf-8')
            assert received_text == expected_text
    assert local_page.name == expected_name


def test_resources_download(page, image, style, script):
    address = "https://local.com"
    with requests_mock.Mocker() as rmock:
        rmock.get(address, text=page.read_text(encoding='utf-8'))
        rmock.get(f"{address}/assets/style.css", text=style.read_text())
        rmock.get(f"{address}/assets/script.js", text=script.read_text())
        rmock.get(f"{address}/assets/python.png", content=image.read_bytes())
        with TemporaryDirectory() as tempdir:
            page_path, resources_path = download(address, tempdir, False)
            assert page_path.read_text(
                encoding='utf-8') != page.read_text(encoding='utf-8')
            # Check resources exist in *_files directory.
            resources_list = [x.name for x in resources_path.iterdir()]
            assert len(resources_list) == 3
            for f in ['style.css', 'script.js', 'python.png']:
                assert f"local-com-assets-{f}" in resources_list


@pytest.mark.parametrize("url", [
    "https://local.com/wrong", "wrong//local.com/page", "https://"])
def test_exceptions(url):
    # Test with wrong url
    with TemporaryDirectory() as tempdir:
        with pytest.raises(ConnectionError):
            download(url, tempdir)
    # Test with wrong output path
    with requests_mock.Mocker() as rmock:
        rmock.get(url, text="Test")
        with pytest.raises(PathAccessError):
            download(url, 'wrong')
