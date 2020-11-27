import argparse
import pathlib


def get_argparser() -> object:
    parser = argparse.ArgumentParser(
        "page_loader",
        "page-loader --output /var/tmp https://ru.hexlet/courses",
        "Allows you to load page with everything related to it")
    parser.add_argument("url")
    parser.add_argument(
        '-o', "--output",
        help="set destination path", default=pathlib.Path.cwd(), type=str)
    return parser


def parse_args() -> object:
    args = get_argparser().parse_args()
    return args
