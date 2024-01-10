from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
XSLT_PATH = (PROJECT_ROOT / "xslt").resolve()
XSLT_FILES = {
    "extract-sch": Path(XSLT_PATH, "extract_sch.xsl").resolve(),
    "schxslt": Path(
        XSLT_PATH,
        "schxslt/core/src/main/resources/xslt/2.0/pipeline-for-svrl.xsl",
    ).resolve(),
}
