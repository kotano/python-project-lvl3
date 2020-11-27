from os.path import splitext
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


def download(url, destination=Path.cwd()) -> str:
    file_name = get_filename_by_url(url)
    dir_path = Path(destination) / (file_name + "_files")
    dir_path.mkdir(exist_ok=True)

    contents = requests.get(url).text
    contents = load_images(contents, dir_path)

    page_path = Path(destination).resolve() / (file_name + '.html')
    page_path.write_text(contents, 'utf-8')
    return page_path


def get_filename_by_url(url) -> str:
    parsed = urlparse(url)
    file_name = (parsed.hostname + parsed.path.rstrip('/'))\
        .replace('/', '-')\
        .replace('.', '-')
    return file_name


def load_images(contents, destination) -> str:
    soup = BeautifulSoup(contents, features='html.parser')
    for tag in soup.find_all('img', recursive=True):
        src = tag['data-src']
        base, ext = splitext(src)
        dest = Path(destination) / (get_filename_by_url(base) + ext)
        response = requests.get(src)
        dest.write_bytes(response.content)
        tag['data-src'] = str(dest)
    return str(soup)


def load_local_files():
    pass
