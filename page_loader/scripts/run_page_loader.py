import sys
import webbrowser
import logging

from page_loader.cli import parse_args
from page_loader import download
from page_loader.logging import configure_logger


def main():
    args = parse_args()
    configure_logger(args.loglevel)
    res = download(args.url, args.output)
    if args.x:
        webbrowser.open(res)
    logging.debug("Program finished with exit code 0")
    print(res)
    sys.exit(0)


if __name__ == "__main__":
    main()
