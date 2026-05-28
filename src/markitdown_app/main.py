"""Entry point for MarkItDown App."""

import sys


def main() -> None:
    from markitdown_app.app import MarkItDownApp

    app = MarkItDownApp()
    app.run()


if __name__ == "__main__":
    main()
