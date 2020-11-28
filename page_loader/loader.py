from os.path import splitext
from pathlib import Path
import re
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


def download(url, destination=Path.cwd()) -> str:
    file_name = get_filename_by_url(url)
    dir_path = Path(destination) / (file_name + "_files")
    dir_path.mkdir(exist_ok=True)

    contents = requests.get(url).text
    contents = load_resources(
        contents, dir_path,
        # match=urlparse(url).hostname
    )

    page_path = Path(destination).resolve() / (file_name + '.html')
    page_path.write_text(contents, 'utf-8')
    return page_path


def get_filename_by_url(url) -> str:
    parsed = urlparse(url)
    file_name = (parsed.hostname + parsed.path.rstrip('/'))\
        .replace('/', '-')\
        .replace('.', '-')
    return file_name


tag_map = {
    'img': 'data-src',
    'script': 'src',
    'link': 'href',
}


def load_resources(contents, destination, match='') -> str:
    soup = BeautifulSoup(contents, features='html.parser')
    for tag, attr in tag_map.items():
        for elem in soup.find_all(tag, recursive=True):
            src = elem.get(attr)
            if not src or not re.search(match, src):
                continue
            base, ext = splitext(src)
            file_path = Path(destination) / (get_filename_by_url(base) + ext)
            response = requests.get(src)
            file_path.write_bytes(response.content)
            elem[attr] = (Path(destination.name) / file_path.name).as_posix()
    return str(soup)
