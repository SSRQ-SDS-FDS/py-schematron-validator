from pathlib import Path

import pytest
from testfixtures import TempDirectory

from pyschval.main import (
    SchematronResult,
    extract_schematron_from_relaxng,
    isoschematron_validate,
)

xslt_path = Path(Path(__file__).parent.parent / "xslt").resolve()
xslt_files = {
    "extract-sch": str(Path(xslt_path, "extract_sch.xsl").resolve()),
    "schxslt": str(
        Path(
            xslt_path,
            "schxslt/core/src/main/resources/xslt/2.0/pipeline-for-svrl.xsl",
        ).resolve()
    ),
}


@pytest.fixture
def schema_data():
    base_path = Path(Path(__file__).parent.parent / "xslt").resolve()
    relaxng = """ <grammar xmlns="http://relaxng.org/ns/structure/1.0"
         datatypeLibrary="http://www.w3.org/2001/XMLSchema-datatypes">
            <sch:pattern xmlns:sch="http://purl.oclc.org/dsdl/schematron" xmlns:rng="http://relaxng.org/ns/structure/1.0">
                <sch:rule context="test">
                    <sch:assert test="matches(., 'hello world')" xml:lang="en">The text matches 'hello world'</sch:assert>
                </sch:rule>
            </sch:pattern>
        </grammar>"""
    return (
        {
            "extract-sch": str(Path(base_path, "extract_sch.xsl").resolve()),
            "schxslt": str(
                Path(
                    base_path,
                    "schxslt/core/src/main/resources/xslt/2.0/pipeline-for-svrl.xsl",
                ).resolve()
            ),
        },
        relaxng,
    )


@pytest.fixture
def dir():
    with TempDirectory() as dir:
        dir.write("test1.xml", bytes("<test>hello world</test>", encoding="utf-8"))
        yield dir


@pytest.fixture
def xml(dir: TempDirectory):
    return str(dir.as_path("test1.xml"))


def test_extract_schematron_from_relaxng(schema_data):
    import xml.etree.ElementTree as ET

    result = ET.fromstring(
        extract_schematron_from_relaxng(schema_data[1], schema_data[0]["extract-sch"])
    )

    assert result is not None
    assert len(result[0:]) == 2


def test_isoschematron_validate_valid_input(schema_data, xml):
    files = [xml]
    results = isoschematron_validate(files, schema_data[1])
    assert isinstance(results, list)
    assert all(isinstance(result, SchematronResult) for result in results)
    assert all(result.is_valid() for result in results)


def test_isoschematron_validate_empty_files_list():
    files = []
    relaxng = "<element name='test'></element>"
    with pytest.raises(ValueError):
        isoschematron_validate(files, relaxng)


def test_schematron_result_is_valid():
    schematron_result = SchematronResult("test.xml", "successful-report")
    assert not schematron_result.is_valid()
    schematron_result = SchematronResult("test.xml", "failed-assert")
    assert not schematron_result.is_valid()
    schematron_result = SchematronResult("test.xml", "valid")
    assert schematron_result.is_valid()
