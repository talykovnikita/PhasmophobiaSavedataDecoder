import argparse

import app_logger
from PhasmoSaveDataDecoder import PhasmoSaveDataDecoder

logger = app_logger.get_logger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Set money value for you profile in Phasmophobia."
    )
    parser.add_argument(
        "-amount", type=int, default=999999, help="Amount of money that will be set."
    )
    config = parser.parse_args()
    logger.debug(f"Parameters: {config}")

    PhasmoSaveDataDecoder().decrypt().set_money(amount=config.amount).encrypt()


if __name__ == "__main__":
    main()
