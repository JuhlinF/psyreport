"""Module for parsing Pearson Q-Interactive-style result files"""

from zipfile import ZipFile


class Subtest:
    """
    Class containing information about a subtest.
    """

    def __init__(self) -> None:
        self.name = str()
        self.description = str()
        self.score = int()
        self.raw_score = int()

    def __str__(self) -> str:
        return f"Subtest {self.name} ({self.score})"


class IndexScale:
    """
    Class containing information about an index scale.
    """

    def __init__(self) -> None:
        self.short_name = str()
        self.long_name = str()
        self.description = str()
        self.score = int()
        self.percentile = int()
        self.confidence_intervals = {}  # type dict[str, tuple[int, int]]

    @property
    def score_description(self) -> str:
        """
        Returns a textual description of the index score.
        """
        if 1 <= self.score <= 70:
            return "betydligt under genomsnittet"
        if 71 <= self.score <= 85:
            return "klart under genomsnittet"
        if 86 <= self.score <= 92:
            return "i genomsnittets nedre del"
        if 93 <= self.score <= 107:
            return "inom genomsnittet"
        if 108 <= self.score <= 115:
            return "i genomsnittets övre del"
        if 116 <= self.score <= 130:
            return "klart över genomsnittet"
        if self.score >= 131:
            return "betydligt över genomsnittet"

        raise RuntimeError(f"Bad index score: {self}")

    @property
    def ci_95(self) -> str:
        """Return 95 percent confidence interval"""
        return (
            f"{self.confidence_intervals['95'][0]}-{self.confidence_intervals['95'][1]}"
        )

    def __str__(self) -> str:
        return f"{self.short_name} ({self.score})"


class Battery:
    """
    Class containing information about the test battery results.
    """

    def __init__(self) -> None:
        self.indices = []  # type: list[IndexScale]
        self.subtests = []  # type: list[Subtest]

    def get_index(self, index_name: str) -> IndexScale | None:
        """
        Returns IndexScale with name <index_name> if it exists, otherwise returns None.
        """
        return _find_item(index_name, self.indices, "short_name")

    def get_subtest(self, subtest_name: str) -> Subtest | None:
        """
        Returns Subtest with name <subtest_name> if it exists, otherwise returns None.
        """
        return _find_item(subtest_name, self.subtests, "short_name")

    def __getitem__(self, item_name: str):
        return self.get_index(item_name) or self.get_subtest(item_name)

    def __str__(self) -> str:
        return f"Battery ({', '.join([str(index) for index in self.indices])})"


def parse_pearson_zipfile(report_file) -> Battery:
    """
    Parse a file exported from Pearson Q-Interactive.
    """
    zipfile = ZipFile(report_file)

    filename = str()
    for filename in zipfile.namelist():
        if filename.endswith(".csv"):
            break
    else:
        raise RuntimeError("NO CSV file found in ZIP archive")

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


# Helper functions


def _get_section(lines: list, section: str) -> list[str]:
    start = lines.index(section) + 3
    stop = lines.index("", start)
    return lines[start:stop]


def _subtest_from_row(line: str) -> Subtest:
    subtest = Subtest()
    name, _, score = line.split(",")
    subtest.name = _shorten_name(name)
    subtest.score = score  # type: ignore FIXME
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
    index.long_name = name
    index.short_name = _shorten_name(name)
    index.score = int(score)
    index.percentile = percentile  # type: ignore FIXME
    index.confidence_intervals["90"] = (int(conf_90_low), int(conf_90_high))
    index.confidence_intervals["95"] = (int(conf_95_low), int(conf_95_high))
    return index


def _shorten_name(name: str) -> str:
    start = name.index(" ") + 1
    name = name[start:]
    return name


def _find_item(search_string: str, search_list: list, search_attr: str):
    search_string = search_string.casefold().strip()
    for item in search_list:
        tmp_name = getattr(item, search_attr).casefold().strip()
        if tmp_name == search_string or tmp_name.startswith(search_string):
            return item

    return None


if __name__ == "__main__":
    result = parse_pearson_zipfile("tests/TT111111_4_10_2023.zip")
    print(result)
