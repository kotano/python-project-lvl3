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
def download(url, destination=Path.cwd(), localonly=True) -> list:
    logging.info("Starting download")
    file_name = get_filename_by_url(url)
    resources_path = Path(destination) / (file_name + "_files")
    resources_path.mkdir(exist_ok=True)

    page_contents = load_resources(url, resources_path, localonly=localonly)

    page_path = Path(destination).resolve() / (file_name + '.html')
    page_path.write_text(page_contents, 'utf-8')
    return page_path, resources_path


@log_func
def get_filename_by_url(url) -> str:
    parsed = urlparse(url)
    hostname = parsed.hostname if parsed.hostname else ''
    file_name = "{}/{}".format(hostname.strip('/'), parsed.path.strip('/'))\
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
def load_resources(url, local_dir, localonly=True) -> str:
    soup = BeautifulSoup(requests.get(url).text, features='html.parser')
    for tag, attr in tag_map.items():
        for elem in soup.find_all(tag):
            src = elem.get(attr)
            if not src:
                continue
            elif localonly and not urlparse(url).hostname in src:
                logger.info("Skipping side resource {}".format(src))
                continue
            src = normalize_link(src, url)
            elem[attr] = save_resource(src, local_dir)
    return str(soup)


def normalize_link(src, original_link) -> str:
    res = src
    parsed_link = urlparse(res)
    # If address is relative then add hostname to link
    if not parsed_link.netloc:
        absolute_path = dirname(original_link)
        logger.info("Changing local address {}".format(src))
        res = "{}/{}".format(absolute_path, parsed_link.path.strip('/'))
    return res


def save_resource(src, destination) -> str:
    base, ext = splitext(src)
    file_path = Path(destination) / (get_filename_by_url(base) + ext)
    try:
        response = requests.get(src)
    except Exception:
        logger.exception("Error occured while loading resource.")
        return src
    file_path.write_bytes(response.content)
    logger.info("Resource {} was saved to {}".format(src, file_path))
    res = (Path(destination.name) / file_path.name).as_posix()
    logger.info("Chaned link to local address {}".format(res))
    return res
