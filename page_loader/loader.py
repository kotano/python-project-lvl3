from logging import getLogger
import logging
from os.path import splitext, dirname
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from page_loader.logging import log_func

logger = getLogger(__name__)


@log_func
def download(url, destination=Path.cwd(), localonly=True) -> str:
    logging.info("Starting download")
    file_name = get_filename_by_url(url)
    dir_path = Path(destination) / (file_name + "_files")
    dir_path.mkdir(exist_ok=True)

    contents = load_resources(url, dir_path, localonly=localonly)

    page_path = Path(destination).resolve() / (file_name + '.html')
    page_path.write_text(contents, 'utf-8')
    return page_path


@log_func
def get_filename_by_url(url) -> str:
    parsed = urlparse(url)
    hostname = parsed.hostname if parsed.hostname else ''
    file_name = (hostname + parsed.path.rstrip('/'))\
        .replace('/', '-')\
        .replace('.', '-')
    return file_name


tag_map = {
    'img': 'src',
    'script': 'src',
    'link': 'href',
}


# TODO: img tag has two type of sources `src` and `data-src`
# find way to handle it.
@log_func
def load_resources(url, destination, localonly=True) -> str:
    soup = BeautifulSoup(requests.get(url).text, features='html.parser')
    for tag, attr in tag_map.items():
        for elem in soup.find_all(tag, recursive=True):
            src = elem.get(attr)
            if not src:
                continue
            addr = urlparse(src)
            # If address is relative then add hostname to link
            if not addr.netloc:
                logger.info("Changing local address {}".format(src))
                src = "{}/{}".format(dirname(url), addr.path)
            # Else if `localonly` is set and link is not related to host
            elif localonly and not urlparse(url).hostname in src:
                logger.info("Skipping side resource {}".format(src))
                continue
            base, ext = splitext(src)
            file_path = Path(destination) / (get_filename_by_url(base) + ext)
            try:
                response = requests.get(src)
            except Exception:
                logger.exception("Error occured while loading resource.")
                continue
            file_path.write_bytes(response.content)
            logger.info("Resource {} was saved to {}".format(src, file_path))
            elem[attr] = (Path(destination.name) / file_path.name).as_posix()
            logger.info("Chaned link to local address {}".format(elem[attr]))
    return str(soup)
