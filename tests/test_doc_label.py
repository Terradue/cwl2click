from unittest import TestCase

from tests.utils import CWLClickTestCase


class TestDocLabel(CWLClickTestCase, TestCase):

    def setUp(self):
        super().setUp()

    def test_label(self):
        cli = self.generate_cli("tests/data/doc-label.cwl")

        self.assertIn("argument", cli.commands)

        cmd = cli.commands["argument"]

        self.assertEqual(cmd.help, "this is doc")
        self.assertEqual(cmd.short_help, "this is label")

        params = {p.name: p for p in cmd.params}
        self.assertIn("input", params)
        
        opt = params["input"]
        self.assertEqual(opt.help, "this is input label")
        