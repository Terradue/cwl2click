from unittest import TestCase

from tests.utils import CWLClickTestCase


class TestStringFormat(CWLClickTestCase, TestCase):

    def setUp(self):
        super().setUp()
        self.cli = self.generate_cli("tests/data/string-format.cwl")

    def test_uri_inputs(self):

        self.assertIn("argument", self.cli.commands)

        cmd = self.cli.commands["argument"]
        params = {p.name: p for p in cmd.params}
        self.assertIn("uri_input", params)

        opt = params["uri_input"]
        
        self.assertEqual(opt.type.name, "text")

    def test_uuid_inputs(self):

        self.assertIn("argument", self.cli.commands)

        cmd = self.cli.commands["argument"]
        params = {p.name: p for p in cmd.params}
        self.assertIn("uuid_input", params)

        opt = params["uuid_input"]
        
        self.assertEqual(opt.type.name, "uuid") 
