import unittest
from io import StringIO
import sys

from pydominion.utils import log

class TestLog(unittest.TestCase):
    def test_log(self):
        output = StringIO()
        log(output, "brief", "comment")
        self.assertEqual(output.getvalue(), "[brief] comment\n")
