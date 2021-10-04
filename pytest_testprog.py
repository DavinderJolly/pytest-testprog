import csv
import json
from typing import Optional

from _pytest.config import Config
from _pytest.config.argparsing import Parser
from _pytest.main import Session
from _pytest.nodes import Item
from _pytest.reports import TestReport

PASSED_SYMBOL = "\u2714"
FAILED_SYMBOL = "\u2718"


def pytest_addoption(parser: Parser) -> None:
    export = parser.getgroup("export")
    export.addoption(
        "--export",
        action="store",
        default=None,
        help="Store test reports in a CSV file",
    )


def pytest_report_teststatus(
    report: TestReport, config: Config
) -> Optional[tuple[str, str, str]]:
    if report.when == "call" and (
        config.option.verbose == -1 or config.option.verbose >= 0
    ):
        symbol = PASSED_SYMBOL if report.passed else FAILED_SYMBOL
        return (
            report.outcome,
            f" {symbol}",
            f"{report.outcome.upper()} {symbol}",
        )


def pytest_collection_modifyitems(
    session: Session, config: Config, items: list[Item]
) -> None:
    export_option = config.getoption("export")
    if export_option is None:
        return
    parsed_items = get_parsed_items(items)
    if export_option.lower() == "csv":
        export_to_csv(parsed_items)
    elif export_option.lower() == "json":
        export_to_json(parsed_items)
    else:
        raise ValueError("export only supports csv or json")


def export_to_json(parsed_items: list[dict[str, Optional[str]]]) -> None:
    with open("test_list.json", "w") as f:
        json.dump({"tests": parsed_items}, f, indent=2)


def export_to_csv(parsed_items: list[dict[str, Optional[str]]]) -> None:
    with open("test_list.csv", "w") as f:
        writer = csv.DictWriter(
            f, ["file_name", "class_name", "test_name", "summary", "description"]
        )
        writer.writeheader()
        for item in parsed_items:
            writer.writerow(item)


def get_parsed_items(items: list[Item]) -> list[dict[str, Optional[str]]]:
    return [parse_item(item) for item in items]


def parse_item(item: Item) -> dict[str, Optional[str]]:
    summary, _, doc = item.obj.__doc__.strip().partition("\n")
    description, *_ = doc.partition("\n\n")
    return {
        "file_name": f"{item.module.__name__}.py",
        "class_name": item.cls.__name__ if item.cls else None,
        "test_name": item.name,
        "summary": summary.strip(),
        "description": description.strip(),
    }
