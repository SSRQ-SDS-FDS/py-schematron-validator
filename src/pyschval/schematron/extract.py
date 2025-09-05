from pathlib import Path

from saxonche import PySaxonProcessor

from pyschval import config, utils


def extract_schematron_from_relaxng(
    relaxng_source: str | Path, xsl_path: str = str(config.XSLT_FILES["extract-sch"])
) -> str:
    """Extract the schematron-rules from a relaxng-source.

    Args:
        relaxng_source (str | Path): The relaxng-source.
        xsl_path (str, optional): The path to the xsl-file. Defaults to str(config.XSLT_FILES["extract-sch"]).

    Returns:
        str: The schematron-rules.
    """
    with PySaxonProcessor(license=False) as proc:
        xsltproc = proc.new_xslt30_processor()
        relaxng = (
            proc.parse_xml(xml_file_name=str(relaxng_source))
            if utils.is_file_and_exists(relaxng_source)
            else proc.parse_xml(xml_text=relaxng_source)  # type: ignore
        )
        xsl = xsltproc.compile_stylesheet(stylesheet_file=xsl_path)  # type: ignore
        isosch = xsl.transform_to_string(xdm_node=relaxng)

    return isosch
