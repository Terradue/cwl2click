from unittest import TestCase

from tests.utils import CWLClickTestCase


class TestInputTypes(CWLClickTestCase, TestCase):

    def setUp(self):
        super().setUp()

    def test_input_types(self):
        cli = self.generate_cli("tests/data/input-types.cwl")

        self.assertIn("argument", cli.commands)

        cmd = cli.commands["argument"]
        params = {p.name: p for p in cmd.params}
        print(params)
        self.assertIn("directory_input", params)
        self.assertIn("file_input", params)
        self.assertIn("string_input", params)
        self.assertIn("int_input", params)
        self.assertIn("float_input", params)
        
        opt = params["directory_input"]
        self.assertTrue(opt.required)
        self.assertEqual(opt.type.name, "directory")
        self.assertFalse(opt.multiple)

        opt = params["file_input"]
        self.assertTrue(opt.required)
        self.assertEqual(opt.type.name, "file")
        self.assertFalse(opt.multiple)   

        opt = params["string_input"]
        self.assertTrue(opt.required)
        self.assertEqual(opt.type.name, "text")
        self.assertFalse(opt.multiple)

        opt = params["int_input"]
        self.assertTrue(opt.required)
        self.assertEqual(opt.type.name, "integer")
        self.assertFalse(opt.multiple)

        opt = params["float_input"]
        self.assertTrue(opt.required)
        self.assertEqual(opt.type.name, "float")
        self.assertFalse(opt.multiple)

    def test_array_input_types(self):
        cli = self.generate_cli("tests/data/array-input-types.cwl")

        self.assertIn("argument", cli.commands)

        cmd = cli.commands["argument"]
        params = {p.name: p for p in cmd.params}

        opt = params["file_input"]
        self.assertTrue(opt.required)
        self.assertEqual(opt.type.name, "file")
        self.assertTrue(opt.multiple)

        opt = params["directory_input"]
        self.assertTrue(opt.required)
        self.assertEqual(opt.type.name, "directory")
        self.assertTrue(opt.multiple)

        opt = params["string_input"]
        self.assertTrue(opt.required)
        self.assertEqual(opt.type.name, "text")
        self.assertTrue(opt.multiple)

        opt = params["int_input"]
        self.assertTrue(opt.required)
        self.assertEqual(opt.type.name, "integer")
        self.assertTrue(opt.multiple)

        opt = params["float_input"]
        self.assertTrue(opt.required)
        self.assertEqual(opt.type.name, "float")
        self.assertTrue(opt.multiple)

    def test_optional_input_types(self):
        cli = self.generate_cli("tests/data/optional-input-types.cwl")

        self.assertIn("argument", cli.commands)

        cmd = cli.commands["argument"]
        params = {p.name: p for p in cmd.params}

        opt = params["file_input"]
        self.assertFalse(opt.required)
        self.assertEqual(opt.type.name, "file")
        self.assertFalse(opt.multiple)

        opt = params["directory_input"]
        self.assertFalse(opt.required)
        self.assertEqual(opt.type.name, "directory")
        self.assertFalse(opt.multiple)

        opt = params["string_input"]
        self.assertFalse(opt.required)
        self.assertEqual(opt.type.name, "text")
        self.assertFalse(opt.multiple)

        opt = params["int_input"]
        self.assertFalse(opt.required)
        self.assertEqual(opt.type.name, "integer")
        self.assertFalse(opt.multiple)

        opt = params["float_input"]
        self.assertFalse(opt.required)
        self.assertEqual(opt.type.name, "float")
        self.assertFalse(opt.multiple)