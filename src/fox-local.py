import logging
import sys

from bidirectional import FoxBidirectional

_LOGGER = logging.getLogger(__name__)


def main():
    """Main entry point"""
    _LOGGER.info("Starting Fox Local...")
    fox_service = FoxBidirectional()
    fox_service.run()


def setup_logging():
    """Setup a logging target"""
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    root.addHandler(handler)


if __name__ == "__main__":
    setup_logging()
    main()
