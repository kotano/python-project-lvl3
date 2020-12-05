import argparse
import pathlib

loglevels = ["DEBUG", "INFO", "WARNING", "ERROR", 'CRITICAL']


def get_argparser() -> object:
    parser = argparse.ArgumentParser(
        "page_loader",
        "page-loader --output /var/tmp https://ru.hexlet/courses",
        "Allows you to load page with everything related to it")
    parser.add_argument("url", help="Website to download")
    parser.add_argument(
        '-o', "--output",
        help="set destination path", default=pathlib.Path.cwd(), type=str)
    parser.add_argument(
        '-x', help="open with webbrowser after download ends",
        action="store_true")
    parser.add_argument(
        '-l', '--loglevel', help="Set logging level",
        default="WARNING", choices=loglevels)
    return parser


def parse_args() -> object:
    args = get_argparser().parse_args()
    return args
