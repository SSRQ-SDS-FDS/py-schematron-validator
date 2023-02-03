from dataclasses import dataclass
from typing import Optional

from saxonche import PySaxonProcessor


@dataclass
class SchematronResult:
    file: str
    report: str

    def is_valid(self) -> bool:
        """Return True if the validation was successful."""
        if "failed-assert" in self.report or "successful-report" in self.report:
            return False
        return True


class SchematronValidationFailedError(Exception):
    """Raised when the schematron validation just returned results of type None."""

    def __init__(self):
        super().__init__("The schematron validation returned no results.")


def extract_schematron_from_relaxng(relaxng: str, xsl_path: str) -> str:
    with PySaxonProcessor(license=False) as proc:
        xsltproc = proc.new_xslt30_processor()
        relaxng = proc.parse_xml(xml_text=relaxng)
        xsl = xsltproc.compile_stylesheet(stylesheet_file=xsl_path)
        isosch = xsl.transform_to_string(xdm_node=relaxng)

    return isosch


def create_schematron_stylesheet(isosch: str, xsl_path: str) -> str:
    with PySaxonProcessor(license=False) as proc:
        xsltproc = proc.new_xslt30_processor()
        xsl = xsltproc.compile_stylesheet(
            stylesheet_file=xsl_path,
        )
        isosch = xsl.transform_to_string(xdm_node=proc.parse_xml(xml_text=isosch))

    return isosch


def isoschematron_validate(files: list[str], relaxng: str) -> list[SchematronResult]:

    from pathlib import Path

    if len(files) == 0:
        raise ValueError("No files to validate")

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

    isosch = create_schematron_stylesheet(
        extract_schematron_from_relaxng(
            relaxng=relaxng, xsl_path=xslt_files["extract-sch"]
        ),
        xsl_path=xslt_files["schxslt"],
    )

    results: list[SchematronResult] = []

    with PySaxonProcessor(license=False) as proc:
        xsltproc = proc.new_xslt30_processor()
        xsl = xsltproc.compile_stylesheet(stylesheet_text=isosch)

        for file in files:
            xml = proc.parse_xml(xml_file_name=file)
            report = xsl.transform_to_string(xdm_node=xml)
            if report is not None:
                results.append(SchematronResult(file=file, report=report))

    if len(results) == 0:
        raise SchematronValidationFailedError()

    return results
