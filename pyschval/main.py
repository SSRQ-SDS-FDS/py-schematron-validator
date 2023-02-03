from dataclasses import dataclass


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


def isoschematron_validate(files: list[str], relaxng: str) -> list[SchematronResult]:
    from pathlib import Path

    from saxonche import PySaxonProcessor

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

    results: list[SchematronResult] = []

    with PySaxonProcessor(license=False) as proc:
        xsltproc = proc.new_xslt30_processor()
        """ Step 1: Extract the schematron from the RelaxNG"""
        relaxng = proc.parse_xml(xml_text=relaxng)
        xsl = xsltproc.compile_stylesheet(stylesheet_file=xslt_files["extract-sch"])
        isosch = xsl.transform_to_string(xdm_node=relaxng)
        """ Step 2: Create the schematron stylesheet"""
        xsl = xsltproc.compile_stylesheet(
            stylesheet_file=xslt_files["schxslt"],
        )
        isosch = xsl.transform_to_string(xdm_node=proc.parse_xml(xml_text=isosch))
        xsl = xsltproc.compile_stylesheet(stylesheet_text=isosch)
        """ Step 3: Validate the files"""
        for file in files:
            xml = proc.parse_xml(xml_file_name=file)
            report = xsl.transform_to_string(xdm_node=xml)
            if report is not None:
                results.append(SchematronResult(file=file, report=report))

    results = list(filter(None, results))

    if len(results) == 0:
        raise SchematronValidationFailedError()

    return results
