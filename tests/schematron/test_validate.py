from pyschval.types import result


def test_apply_schematron_validation(schematron_result: list[result.SchematronResult]):
    """Test if the schematron validation is applyable and returns a list of results."""
    assert schematron_result is not None
    assert isinstance(schematron_result, list) is True
    assert (
        all(isinstance(r, result.SchematronResult) for r in schematron_result) is True
    )
