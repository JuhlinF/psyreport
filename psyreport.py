"""
Create a report based on a Pearson Q-Interactive export file using Jinja2
"""
from jinja2 import Environment, PackageLoader, select_autoescape

from psyscore import parse_pearson_zipfile


def create_report(qi_file: str, template_name: str):
    """
    Create a report for test in <qi_file> using Jinja2 template <template_name>
    """
    battery = parse_pearson_zipfile(qi_file)
    env = Environment(
        loader=PackageLoader("psyreport"),
        trim_blocks=True,
        autoescape=select_autoescape(),
    )
    template = env.get_template(template_name)

    return template.render(battery=battery)


if __name__ == "__main__":
    print(create_report("tests/TT111111_4_10_2023.zip", "plain.txt"))
