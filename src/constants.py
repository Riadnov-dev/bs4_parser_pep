import re
from pathlib import Path

MAIN_DOC_URL = "https://docs.python.org/3/"
BASE_DIR = Path(__file__).parent
DATETIME_FORMAT = "%Y-%m-%d_%H-%M-%S"
PEP_URL = "https://peps.python.org/"

EXPECTED_STATUS = {
    "A": ("Active", "Accepted"),
    "D": ("Deferred",),
    "F": ("Final",),
    "P": ("Provisional",),
    "R": ("Rejected",),
    "S": ("Superseded",),
    "W": ("Withdrawn",),
    "": ("Draft", "Active"),
}

OUTPUT_PRETTY = "pretty"
OUTPUT_FILE = "file"

PYTHON_VERSION_PATTERN = re.compile(
    r"Python (?P<version>\d\.\d+) \((?P<status>.*)\)")
PDF_A4_ZIP_PATTERN = re.compile(r".+pdf-a4\.zip$")
