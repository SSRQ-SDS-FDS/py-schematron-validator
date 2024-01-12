import pyschval.schematron.model.svrl as svrl_model
from pyschval.types import result


def test_result_file_property(
    schematron_result: list[result.SchematronResult], xml: str
):
    assert schematron_result[0].file == xml


def test_result_report_property(
    schematron_result: list[result.SchematronResult], xml: str
):
    report = schematron_result[0].report

    assert isinstance(report, svrl_model.Output)
    assert report.title == "Extracted Schematron Rules"

    assert report.fired_rules is not None
    assert len(report.fired_rules) == 1
    assert report.fired_rules[0].context == "test"

    assert report.failed_asserts is not None
    assert len(report.failed_asserts) == 1
    assert report.failed_asserts[0].test == "matches(., '^[A-Z]')"
    assert (
        report.failed_asserts[0].text == "The text should start with a upper-case value"
    )
    assert report.failed_asserts[0].role == svrl_model.Role.WARN

    assert report.is_valid() is False
    assert report.is_valid(all_error_types=False) is True
