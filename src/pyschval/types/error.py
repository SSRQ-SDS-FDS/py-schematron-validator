class SchematronValidationFailed(Exception):
    """Error when the schematron validation returns as None."""

    def __init__(self, file: str):
        super().__init__(f"The schematron validation for {file} returned no results.")
