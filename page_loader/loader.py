import logging
from os.path import splitext
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from page_loader import logging as lo


logger = logging.getLogger(__name__)


# @log_func
def download(url, destination=Path.cwd(), localonly=True) -> list:
    logger.info("Starting download")
    file_name = get_filename_by_url(url)
    resources_path = (Path(destination) / (file_name + "_files")).resolve()
    if not resources_path.parent.exists():
        logger.error("Could not find the path specified: %s" % destination)
        raise lo.PathAccessError("Directory not found.")
    resources_path.mkdir(exist_ok=True)

    page_contents = load_resources(url, resources_path, localonly=localonly)

    page_path = Path(destination).resolve() / (file_name + '.html')
    page_path.write_text(page_contents, 'utf-8')
    return page_path, resources_path


@lo.log_func
def get_filename_by_url(url) -> str:
    parsed = urlparse(url)
    hostname = parsed.hostname if parsed.hostname else ''
    file_name = "{}{}".format(hostname, parsed.path)\
        .strip('/')\
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
@lo.log_func
def load_resources(url, local_dir, localonly=True) -> str:
    soup = get_parsed_html(url)
    parsed_url = urlparse(url)
    for tag, attr in tag_map.items():
        for elem in soup.find_all(tag):
            src = elem.get(attr)
            if not src:
                continue
            elif not urlparse(src).netloc:
                src = urljoin(url, src.strip('/'))
            elif localonly and parsed_url.hostname not in src:
                logger.debug("Skipping side resource {}".format(src))
                continue
            elem[attr] = save_resource(src, local_dir)
    return str(soup)


def save_resource(src, destination) -> str:
    base, ext = splitext(src)
    file_path = Path(destination) / (get_filename_by_url(base) + ext)
    try:
        response = requests.get(src)
        file_path.write_bytes(response.content)
    except OSError as e:
        # Skip unsuccessfull download
        logger.error(
            "Unable to save resource to destination path {}".format(file_path))
        logger.debug(e, exc_info=True)
        return src
    logger.info("Resource {} was saved to {}".format(src, file_path))
    res = (Path(destination.name) / file_path.name).as_posix()
    logger.debug("Chaned link to local address {}".format(res))
    return res


def get_parsed_html(url):
    try:
        soup = BeautifulSoup(requests.get(url).text, features='html.parser')
    except requests.exceptions.RequestException as e:
        logger.error(
            "Failed to establish connection with: {}".format(url))
        logger.debug(e, exc_info=True)
        raise lo.ConnectionError() from e
    return soup
