from enum import Enum

from parsel import selector

from pyschval.utils import clean_text

__NAMESPACE__ = "http://purl.oclc.org/dsdl/svrl"


class Role(Enum):
    FATAL = "FATAL"
    ERROR = "ERROR"
    WARN = "WARN"
    CAUTION = "CAUTION"
    INFO = "INFO"
    HINT = "HINT"
    TRACE = "TRACE"
    DEBUG = "DEBUG"


class SchematronError:
    role: Role | None
    test: str
    text: str

    def __init__(self, failed_assert: selector.Selector):
        self.test = failed_assert.attrib["test"]
        self.__get_role(failed_assert)
        self.__get_text(failed_assert)

    def __get_role(self, failed_assert: selector.Selector):
        role = failed_assert.attrib.get("role")

        if isinstance(role, str):
            self.role = Role._member_map_.get(role.upper(), None)  # type: ignore
        else:
            self.role = None

    def __get_text(self, failed_assert: selector.Selector):
        text = failed_assert.xpath(
            "svrl:text/text()", namespaces={"svrl": __NAMESPACE__}
        ).get()

        if text is not None:
            self.text = clean_text(text)
        else:
            self.text = ""


class FiredRule:
    context: str

    def __init__(self, fired_rule: selector.Selector):
        context = fired_rule.attrib.get("context")

        if isinstance(context, str):
            self.context = context
        else:
            self.context = ""


class Output:
    title: str | None
    fired_rules: list[FiredRule] | None
    failed_asserts: list[SchematronError] | None
    successful_reports: list[SchematronError] | None

    def __init__(self, report: str):
        parsed_report = selector.Selector(text=report, type="xml")
        self.__get_title(parsed_report)
        self.__get_fired_rules(parsed_report)
        self.failed_asserts = self.__get_errors(parsed_report, "//svrl:failed-assert")
        self.successful_reports = self.__get_errors(
            parsed_report, "//svrl:successful-report"
        )

    def __get_title(self, parsed_report: selector.Selector):
        self.title = parsed_report.attrib.get("title")

    def __get_fired_rules(self, parsed_report: selector.Selector):
        fired_rules = parsed_report.xpath(
            "//svrl:fired-rule", namespaces={"svrl": __NAMESPACE__}
        )

        if len(fired_rules) > 0:
            self.fired_rules = [FiredRule(fired_rule) for fired_rule in fired_rules]
        else:
            self.fired_rules = None

    def __get_errors(
        self, parsed_report: selector.Selector, path: str
    ) -> list[SchematronError] | None:
        errors = parsed_report.xpath(path, namespaces={"svrl": __NAMESPACE__})

        if len(errors) > 0:
            return [SchematronError(error) for error in errors]

        return None

    def is_valid(self, all_error_types: bool = True) -> bool:
        """Return True if the validation was successful.

        Args:
            all_error_types (bool, optional): If True, all error types will be checked.
            Defaults to True. Otherwise, only those with no role or 'ERROR' will be
            checked.

        Returns:
            bool: True if the validation was successful.
        """
        return self.__check_error_type(
            self.failed_asserts, all_error_types
        ) and self.__check_error_type(self.successful_reports, all_error_types)

    def __check_error_type(
        self, error: list[SchematronError] | None, all_error_types: bool
    ) -> bool:
        if error is None:
            return True

        if all_error_types:
            return len(error) == 0

        return (
            len(
                [
                    e
                    for e in error
                    if e.role is None or e.role == Role.ERROR or e.role == Role.FATAL
                ]
            )
            == 0
        )
