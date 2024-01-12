from saxonche import PySaxonProcessor


def test_create_schematron_stylesheet(schematron_stylesheet: str):
    """Test if the schematron stylesheet is a valid xsl stylesheet."""
    with PySaxonProcessor(license=False) as proc:
        xsltproc = proc.new_xslt30_processor()
        xsl = xsltproc.compile_stylesheet(stylesheet_text=schematron_stylesheet)  # type: ignore
        assert xsl is not None
