import webbrowser

from page_loader.cli import parse_args
from page_loader import download
from page_loader import logging

logger = logging.logging.getLogger(__name__)


def main():
    args = parse_args()
    logging.configure_logger(args.loglevel)
    try:
        page, resources = download(args.url, args.output, args.externals)
    except logging.PageLoaderError:
        exit(1)
    if args.x:
        webbrowser.open(page)
    print(page)
    exit(0)


if __name__ == "__main__":
    main()
