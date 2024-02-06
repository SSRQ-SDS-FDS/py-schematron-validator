from parsel import Selector

from pyschval.schematron.model.svrl import __NAMESPACE__, SchematronError


def test_schematron_error_without_role():
    error = SchematronError(
        Selector(
            f"<failed-assert xmlns='{__NAMESPACE__}' test='matches(., \"^[A-Z]\")'><text>The text should start with a upper-case value</text></failed-assert>",
            type="xml",
        )
    )
    assert error.test == 'matches(., "^[A-Z]")'
    assert error.text == "The text should start with a upper-case value"
    assert error.role is None
