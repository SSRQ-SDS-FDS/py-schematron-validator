import pytest

from pyschval.schematron.create import create_schematron_stylesheet
from pyschval.schematron.extract import extract_schematron_from_relaxng
from pyschval.schematron.validate import apply_schematron_validation
from pyschval.types import result


@pytest.fixture(scope="session")
def schema() -> str:
    return """ <grammar xmlns="http://relaxng.org/ns/structure/1.0"
         datatypeLibrary="http://www.w3.org/2001/XMLSchema-datatypes">
            <sch:pattern xmlns:sch="http://purl.oclc.org/dsdl/schematron" xmlns:rng="http://relaxng.org/ns/structure/1.0">
                <sch:rule context="test">
                    <sch:assert test="matches(., 'hello world')" xml:lang="en">The text matches 'hello world'</sch:assert>
                    <sch:assert role="WARN" test="matches(., '^[A-Z]')" xml:lang="en">The text
                    should start with a upper-case value</sch:assert>
                </sch:rule>
            </sch:pattern>
        </grammar>"""


@pytest.fixture(scope="session")
def xml() -> str:
    return "<test>hello world</test>"


@pytest.fixture(scope="session")
def extracted_schematron_rules(schema: str) -> str:
    return extract_schematron_from_relaxng(schema)


@pytest.fixture(scope="session")
def schematron_stylesheet(extracted_schematron_rules: str) -> str:
    return create_schematron_stylesheet(extracted_schematron_rules)


@pytest.fixture(scope="session")
def schematron_result(
    schematron_stylesheet: str, xml: str
) -> list[result.SchematronResult]:
    return apply_schematron_validation([xml], schematron_stylesheet)
