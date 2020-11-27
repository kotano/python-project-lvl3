from pathlib import Path

import requests_mock

from tempfile import TemporaryDirectory
from page_loader import download


def test_download():
    expected_text = "Test data"
    expected_name = "ru-hexlet-io-professions.html"
    with requests_mock.Mocker() as rmock:
        rmock.get("https://ru.hexlet.io/professions", text=expected_text)
        with TemporaryDirectory() as tempdir:
            received = Path(
                download("https://ru.hexlet.io/professions", tempdir))
            received_text = received.read_text(encoding='utf-8')
            assert received_text == expected_text
    assert received.name == expected_name


# Задачи
# Добавьте в тесты проверку скачивания изображений и изменения HTML.
# Измените HTML так, чтобы все ссылки указывали на скачанные файлы.
# Добавьте в ридми аскинему с примером работы пакета.
