import sys
import os
import tempfile
import logging
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
logging.disable(logging.CRITICAL)


def create_temporary_file(extension=None, contents=None):
    if extension:
        (fd, path) = tempfile.mkstemp(suffix=extension)
    else:
        (fd, path) = tempfile.mkstemp(suffix='.tmp')

    if contents:
        os.write(fd, contents.encode())

    os.close(fd)
    return path




