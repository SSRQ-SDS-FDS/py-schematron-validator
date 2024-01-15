# PYSCHVAL [piː-waɪ-ɛs-siː-eɪʧ-viː-eɪ-ɛl]

![CI](https://github.com/SSRQ-SDS-FDS/py-schematron-validator/actions/workflows/main.yml/badge.svg)

To validate XML-files against a given schema (RELAXNG) it's a common practice to use schematron-rules for further validation tasks. This rules are often embedded in the schema. This python package is a small wrapper around [SchXSLT](https://github.com/schxslt/schxslt) and enables schematron validation in python using [SaxonC HE](https://pypi.org/project/saxonche/).

## Installation

At the moment the repository is not published on `pypi` – but you can directly include the repo using your package manager of choice.

## Usage

```python
from pyschval import isoschematron_validate, SchematronResult

def validate() -> list[SchematronResult]:
    relaxng = """ <grammar xmlns="http://relaxng.org/ns/structure/1.0"
         datatypeLibrary="http://www.w3.org/2001/XMLSchema-datatypes">
            <sch:pattern xmlns:sch="http://purl.oclc.org/dsdl/schematron" xmlns:rng="http://relaxng.org/ns/structure/1.0">
                <sch:rule context="test">
                    <sch:assert test="matches(., 'hello world')" xml:lang="en">The text matches 'hello world'</sch:assert>
                </sch:rule>
            </sch:pattern>
        </grammar>"""
    files = ["file1.xml", "file2.xml"]
    return isoschematron_validate(files, relaxng)

if __name__ == "__main__":
    validate()
```

`isoschematron_validate` is the main function to perform the validation. As a first arguments it excepts a list of filenames or direct xml-input (as strings) and the relaxng-schema as a string. The package is fully typed for ease of use. The returned `SchematronResult` allows you to check if the validation was successful and to get the error messages. For more details see the [validation module](./pyschval/schematron/validate.py).

## Author

- [Bastian Politycki](https://github.com/Bpolitycki) – Swiss Law Sources
