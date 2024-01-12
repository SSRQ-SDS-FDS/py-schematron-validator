from saxonche import PySaxonProcessor

from pyschval import config


def create_schematron_stylesheet(
    isosch: str, xsl_path: str = str(config.XSLT_FILES["schxslt"])
) -> str:
    """Create the schematron stylesheet.

    Args:
        isosch (str): The isoschematron file.
        xsl_path (str, optional): The path to the schematron stylesheet. Defaults to str(config.XSLT_FILES["schxslt"]).

    Returns:
        str: The schematron stylesheet.
    """
    with PySaxonProcessor(license=False) as proc:
        xsltproc = proc.new_xslt30_processor()
        xsl = xsltproc.compile_stylesheet(  # type: ignore
            stylesheet_file=xsl_path,
        )
        return xsl.transform_to_string(xdm_node=proc.parse_xml(xml_text=isosch))
