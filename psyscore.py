"""Module for parsing Pearson Q-Interactive-style result files"""

from zipfile import ZipFile


class Battery:
    """
    Class containing information about the test battery results.
    """

    def __init__(self) -> None:
        self.indices = []
        self.subtests = []

    def __str__(self) -> str:
        return f"Battery ({', '.join([str(index) for index in self.indices])})"


class IndexScale:
    """
    Class containing information about an index scale.
    """

    def __init__(self) -> None:
        self.name = ""
        self.description = ""
        self.score = int()
        self.percentile = int()
        self.confidence_intervals = {}
        self.subtests = []

    def __str__(self) -> str:
        return f"{self.name} ({self.score})"


class Subtest:
    """
    Class containing information about a subtest.
    """

    def __init__(self) -> None:
        self.name = ""
        self.description = ""
        self.score = int()
        self.raw_score = int()

    def __str__(self) -> str:
        return f"Subtest {self.name} ({self.score})"


def parse_pearson_zipfile(path: str):
    """
    Parse a file exported from Pearson Q-Interactive.
    """
    zipfile = ZipFile(path)

    filename = str()
    for filename in zipfile.namelist():
        if filename.endswith(".csv"):
            break

    with zipfile.open(filename) as csv_file:
        lines = csv_file.read().decode("utf-16").splitlines()

    battery = Battery()

    subtest_rows = _get_section(lines, "Skalpoäng")
    for row in subtest_rows:
        battery.subtests.append(_subtest_from_row(row))

    index_rows = _get_section(lines, "Indexpoäng")
    for row in index_rows:
        index = _index_from_row(row)
        battery.indices.append(index)

    return battery


def _get_section(lines: list, section: str) -> list[str]:
    start = lines.index(section) + 3
    stop = lines.index("", start)
    return lines[start:stop]


def _subtest_from_row(line: str) -> Subtest:
    subtest = Subtest()
    name, _, score = line.split(",")
    subtest.name = _fix_name(name)
    subtest.score = int(score)
    return subtest


def _index_from_row(row: str) -> IndexScale:
    index = IndexScale()
    (
        name,
        score,
        percentile,
        conf_90_low,
        conf_90_high,
        conf_95_low,
        conf_95_high,
    ) = row.split(",")
    index.name = _fix_name(name)
    index.score = int(score)
    index.percentile = int(percentile)
    index.confidence_intervals["90"] = (int(conf_90_low), int(conf_90_high))
    index.confidence_intervals["95"] = (int(conf_95_low), int(conf_95_high))
    return index


def _fix_name(name: str) -> str:
    start = name.index(" ") + 1
    name = name[start:]
    return name


if __name__ == "__main__":
    result = parse_pearson_zipfile("tests/EW202304_4_19_2023.zip")
    print(result)
