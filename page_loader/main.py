import webbrowser

from page_loader.cli import parse_args
from page_loader import download


def main():
    args = parse_args()
    res = download(args.url, args.output)
    if args.x:
        webbrowser.open(res)
    return res


if __name__ == "__main__":
    main()
