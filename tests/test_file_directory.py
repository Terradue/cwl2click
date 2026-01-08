from unittest import TestCase

from tests.utils import CWLClickTestCase


class TestFileDirectory(CWLClickTestCase, TestCase):

    def setUp(self):
        super().setUp()
        self.cli = self.generate_cli("tests/data/file-directory.cwl")

    def test_directory_inputs(self):

        self.assertIn("argument", self.cli.commands)

        cmd = self.cli.commands["argument"]
        params = {p.name: p for p in cmd.params}
        self.assertIn("directory_input", params)
        self.assertIn("file_input", params)

        opt = params["directory_input"]
        self.assertTrue(opt.type.dir_okay)
        self.assertFalse(opt.type.file_okay)
        self.assertTrue(opt.type.exists)
        self.assertTrue(opt.type.readable)
        self.assertTrue(opt.type.resolve_path)

    def test_file_inputs(self):
        
        cmd = self.cli.commands["argument"]
        params = {p.name: p for p in cmd.params}
        self.assertIn("file_input", params)

        opt = params["file_input"]

        self.assertTrue(opt.type.file_okay)
        self.assertFalse(opt.type.dir_okay)
        self.assertTrue(opt.type.exists)
        self.assertTrue(opt.type.readable)
        self.assertTrue(opt.type.resolve_path)