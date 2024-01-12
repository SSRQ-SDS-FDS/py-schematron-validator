from pathlib import Path
from typing import Callable

from pyschval import config, utils
from pyschval.schematron import create, extract, validate
from pyschval.types import result


def isoschematron_validate(
    input: list[str | Path],
    relaxng: str,
    extract_rules: Callable[
        [str | Path, str], str
    ] = extract.extract_schematron_from_relaxng,
    create_schema: Callable[[str, str], str] = create.create_schematron_stylesheet,
) -> list[result.SchematronResult]:
    """Validate the input files with the schematron rules. Sync version – running in the main thread.

    Args:
        input (list[str]): The input files.
        relaxng (str): The relaxng file.
        extract_rules (Callable[[str | Path, str], str], optional): The function to extract the schematron rules from the relaxng file. Defaults to extract_schematron_from_relaxng.
        create_schema (Callable[[str, str], str], optional): The function to create the schematron stylesheet. Defaults to create_schematron_stylesheet.

    Raises:
        ValueError: If the input is empty.
        SchematronValidationFailedError: If the validation fails.

    Returns:
        list[SchematronResult]: The list of results.
    """
    if len(input) == 0:
        raise ValueError("Input is empty")

    isosch = create_schema(
        extract_rules(relaxng, str(config.XSLT_FILES["extract-sch"])),
        str(config.XSLT_FILES["schxslt"]),
    )

    return validate.apply_schematron_validation(input, isosch)


async def isoschematron_validate_async(
    input: list[str | Path],
    relaxng: str,
    extract_rules: Callable[
        [str | Path, str], str
    ] = extract.extract_schematron_from_relaxng,
    create_schema: Callable[[str, str], str] = create.create_schematron_stylesheet,
) -> list[result.SchematronResult]:
    """Validate the input files with the schematron rules. Async version – running in a separate process.

    Args:
        input (list[str]): The input files.
        relaxng (str): The relaxng file.
        extract_rules (Callable[[str | Path, str], str], optional): The function to extract the schematron rules from the relaxng file. Defaults to extract_schematron_from_relaxng.
        create_schema (Callable[[str, str], str], optional): The function to create the schematron stylesheet. Defaults to create_schematron_stylesheet.

    Raises:
        ValueError: If the input is empty.
        SchematronValidationFailedError: If the validation fails.

    Returns:
        list[SchematronResult]: The list of results.
    """
    from asyncio import gather, get_running_loop
    from concurrent.futures import ProcessPoolExecutor
    from functools import partial
    from os import cpu_count

    if len(input) == 0:
        raise ValueError("Input is empty")

    isosch = create_schema(
        extract_rules(relaxng, str(config.XSLT_FILES["extract-sch"])),
        str(config.XSLT_FILES["schxslt"]),
    )

    results: list[result.SchematronResult] = []
    loop = get_running_loop()
    tasks = []
    cpus = cpu_count()
    len_files = len(input)
    with ProcessPoolExecutor() as pool:
        for files in utils.partition(
            input,
            len_files
            if len_files == 1
            else (len_files if cpus is None else int(len_files / cpus)),
        ):
            tasks.append(
                loop.run_in_executor(
                    pool,
                    partial(
                        validate.apply_schematron_validation, input=files, isosch=isosch
                    ),
                )
            )
        intermediate_results: list[list[result.SchematronResult]] = await gather(*tasks)
        results = [result for chunk in intermediate_results for result in chunk]

    return results
