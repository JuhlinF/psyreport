"""Module for parsing Pearson Q-Interactive-style result files"""

import datetime
import os
from zipfile import ZipFile


class Battery:
    """
    Class containing information about the test battery results.
    """

    def __init__(self) -> None:
        self.indices = []
        self.subtests = []


class IndexScale:
    """
    Class containing information about an index scale.
    """

    def __init__(self) -> None:
        self.name = ""
        self.description = ""
        self.score = None
        self.percentile = None
        self.confidence_intervals = {}

        self.subtests = []


class Subtest:
    """
    Class containing information about a subtest.
    """

    def __init__(self) -> None:
        self.name = ""
        self.description = ""
        self.score = None
        self.raw_score = None


def parse_pearson_zipfile(path: str):
    zf = ZipFile(path)

    tmp = zf.namelist()[0]
    dir, file_name = os.path.split(tmp)
    file_name = os.path.splitext(file_name)[0]

    test_id, date_str = dir.split("_", 1)

    battery_name = file_name.split(dir)[1].split("_")[0]
    m, d, y = date_str.split("_")
    m, d, y = int(m), int(d), int(y)
    date = datetime.date(y, m, d)

    print(f"Test ID: {test_id}\nBattery name: {battery_name}\nDate: {date}")


if __name__ == "__main__":
    parse_pearson_zipfile("tests/EW202304_4_19_2023.zip")
