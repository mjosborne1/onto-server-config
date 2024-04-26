import json
import unittest
import os
import igparser

class TestIgParser(unittest.TestCase):
    def test_process_ig(self):
        """
        Test that the valuesets associated with an IG are returned
        """
        homedir=os.environ['HOME']
        outdir=os.path.join(homedir,"data","server-config","out")
        igs = igparser.main(outdir)
        self.assertIsInstance(igs,object)
