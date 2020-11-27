import requests
from pathlib import Path
from urllib.parse import urlparse


def download(url, path=Path.cwd()) -> str:
    contents = requests.get(url).text
    file_name = get_filename_by_url(url)
    file_path = Path(path).resolve() / file_name
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(contents)
    return file_path


def get_filename_by_url(url):
    parsed = urlparse(url)
    file_name = (parsed.hostname + parsed.path.rstrip('/'))\
        .replace('/', '-')\
        .replace('.', '-') + '.html'
    return file_name
