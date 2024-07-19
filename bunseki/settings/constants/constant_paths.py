# Standard
import os
from glob import glob

from enum import Enum

# Pip
# None

# Custom
from ....home_dir import MAIN_PATH

# from home_dir import MAIN_PATH


class GeneralPaths(Enum):

    # DIR

    MAIN_DIR = MAIN_PATH

    # IMAGES
    IMAGES = os.path.join(MAIN_DIR, "resources/img/")

    # LOG
    LOG_FILE = os.path.join(MAIN_DIR, "log/bunseki.log")


if __name__ == "__main__":
    print(GeneralPaths.IMAGES.value)
