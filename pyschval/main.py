from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterator

from saxonche import PySaxonProcessor

XSLT_PATH = Path(Path(__file__).parent.parent / "xslt").resolve()
XSLT_FILES = {
    "extract-sch": str(Path(XSLT_PATH, "extract_sch.xsl").resolve()),
    "schxslt": str(
        Path(
            XSLT_PATH,
            "schxslt/core/src/main/resources/xslt/2.0/pipeline-for-svrl.xsl",
        ).resolve()
    ),
}


def partition(data: list[str], size: int) -> Iterator[list[str]]:
    for i in range(0, len(data), size):
        yield data[i : i + size]


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


def validate_chunk(files: list[str], isosch: str):
    chunk_result: list[SchematronResult] = []

    with PySaxonProcessor(license=False) as proc:
        xsltproc = proc.new_xslt30_processor()
        xsl = xsltproc.compile_stylesheet(stylesheet_text=isosch)

        for file in files:
            xml = proc.parse_xml(xml_file_name=file)
            report = xsl.transform_to_string(xdm_node=xml)
            if report is not None:
                chunk_result.append(SchematronResult(file=file, report=report))
    return chunk_result


def isoschematron_validate(
    files: list[str],
    relaxng: str,
    extract_rules: Callable[[str, str], str] = extract_schematron_from_relaxng,
    create_schema: Callable[[str, str], str] = create_schematron_stylesheet,
) -> list[SchematronResult]:
    if len(files) == 0:
        raise ValueError("No files to validate")

    isosch = create_schema(
        extract_rules(relaxng, XSLT_FILES["extract-sch"]),
        XSLT_FILES["schxslt"],
    )

    results: list[SchematronResult] = []

    results = validate_chunk(files, isosch)

    if len(results) == 0:
        raise SchematronValidationFailedError()

    return results


async def isoschematron_validate_async(
    files: list[str],
    relaxng: str,
    extract_rules: Callable[[str, str], str] = extract_schematron_from_relaxng,
    create_schema: Callable[[str, str], str] = create_schematron_stylesheet,
) -> list[SchematronResult]:
    from asyncio import gather, get_running_loop
    from concurrent.futures import ProcessPoolExecutor
    from functools import partial
    from os import cpu_count

    if len(files) == 0:
        raise ValueError("No files to validate")

    isosch = create_schema(
        extract_rules(relaxng, XSLT_FILES["extract-sch"]),
        XSLT_FILES["schxslt"],
    )

    results: list[SchematronResult] = []
    loop = get_running_loop()
    tasks = []
    cpus = cpu_count()
    len_files = len(files)
    with ProcessPoolExecutor() as pool:
        for files in partition(
            files,
            len_files
            if len_files == 1
            else (len_files if cpus is None else int(len_files / cpus)),
        ):
            tasks.append(
                loop.run_in_executor(
                    pool,
                    partial(validate_chunk, files=files, isosch=isosch),
                )
            )
        intermediate_results: list[list[SchematronResult]] = await gather(*tasks)
        results = [result for chunk in intermediate_results for result in chunk]

    if len(results) == 0:
        raise SchematronValidationFailedError()

    return results
