from pathlib import Path

from saxonche import PySaxonProcessor

from pyschval import utils
from pyschval.types import error, result


def apply_schematron_validation(
    input: list[str | Path], isosch: str
) -> list[result.SchematronResult]:
    """Apply the schematron validation to the input files.

    Args:
        input (list[str]): The input files.
        isosch (str): The schematron file.

    Returns:
        list[SchematronResult]: The list of results.
    """
    results: list[result.SchematronResult] = []

    with PySaxonProcessor(license=False) as proc:
        xsltproc = proc.new_xslt30_processor()
        xsl = xsltproc.compile_stylesheet(stylesheet_text=isosch)  # type: ignore
        for x in input:
            input_casted = str(x)
            xml = (
                proc.parse_xml(xml_file_name=input_casted)
                if utils.is_file_and_exists(x)
                else proc.parse_xml(xml_text=input_casted)
            )
            report: str | None = xsl.transform_to_string(xdm_node=xml)

            if report is None:
                raise error.SchematronValidationFailed(input_casted)

            results.append(
                result.SchematronResult(
                    file_or_input=input_casted,
                    report=report,
                )
            )

    return results
