import xml.etree.ElementTree as ET


def test_extract_schematron_from_relaxng(extracted_schematron_rules: str):
    """Test the extraction of schematron-rules from a relaxng-source.

    It should return a parsable xml-string, containing the schematron-rules.
    """
    result = ET.fromstring(extracted_schematron_rules)

    assert result is not None
    assert result.tag.endswith("schema")
    assert len(result[0:]) == 2
    assert result[0].tag.endswith("title")
    assert result[1].tag.endswith("pattern")

    assert_rule = result.find(".//{http://purl.oclc.org/dsdl/schematron}assert")
    assert assert_rule is not None
    assert assert_rule.attrib["test"] == "matches(., 'hello world')"
