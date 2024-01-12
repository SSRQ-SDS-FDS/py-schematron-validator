import pytest

from pyschval.main import (
    isoschematron_validate,
    isoschematron_validate_async,
)
from pyschval.types import result


def test_isoschematron_validate_valid_input(schema: str, xml: str):
    validation_results = isoschematron_validate([xml], schema)
    assert isinstance(validation_results, list)
    assert all(isinstance(r, result.SchematronResult) for r in validation_results)
    assert all(r.report.is_valid(all_error_types=False) for r in validation_results)


def test_isoschematron_validate_async_valid_input(schema: str, xml: str):
    from asyncio import run

    validation_results = run(isoschematron_validate_async([xml], schema))
    assert isinstance(validation_results, list)
    assert all(isinstance(r, result.SchematronResult) for r in validation_results)
    assert all(r.report.is_valid(all_error_types=False) for r in validation_results)


def test_isoschematron_validate_empty_files_list():
    files = []
    relaxng = "<element name='test'></element>"
    with pytest.raises(ValueError):
        isoschematron_validate(files, relaxng)
