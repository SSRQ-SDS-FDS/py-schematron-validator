import pyschval.schematron.model.svrl as svrl_model


class SchematronResult:
    file: str
    report: svrl_model.Output

    def __init__(self, file_or_input: str, report: str):
        self.file = file_or_input
        self.report = svrl_model.Output(report=report)

    """ def is_valid(self) -> bool:
        if "failed-assert" in self.report or "successful-report" in self.report:
            return False
        return True """
