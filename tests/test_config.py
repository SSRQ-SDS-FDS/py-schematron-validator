from pyschval import config


def test_xslt_files_are_found():
    for _, xslt in config.XSLT_FILES.items():
        assert xslt.exists() is True
