from typing import Optional

from _pytest.config import Config
from _pytest.config.argparsing import Parser
from _pytest.reports import TestReport

# from _pytest.main import Session
# from _pytest.nodes import Item

PASSED_SYMBOL = "\u2714"
FAILED_SYMBOL = "\u2718"


def pytest_adoption(parser: Parser) -> None:
    export = parser.getgroup("export")
    export.addoption(
        "--export",
        action="store",
        default="csv",
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


# TODO: implement saving report to multiple formats
# def pytest_report_modifyitems(
#     session: Session, config: Config, items: list[Item]
# ) -> None:
#     pass
