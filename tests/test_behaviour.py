from unittest import TestCase
from click.testing import CliRunner

from tests.utils import CWLClickTestCase


class TestBehaviour(CWLClickTestCase, TestCase):

    def setUp(self):
        super().setUp()

    def test_basecommand_argument(self):
        cli = self.generate_cli("tests/data/basecommand-argument.cwl")

        runner = CliRunner()
        result = runner.invoke(cli, ["argument"])

        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Error: Missing option '--input'.", result.output)


    def test_basecommand_argument_help(self):
        cli = self.generate_cli("tests/data/basecommand-argument.cwl")

        runner = CliRunner()
        result = runner.invoke(cli, ["argument", "--help"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("Usage: cli argument [OPTIONS]", result.output)
        self.assertIn("--input TEXT", result.output)
        self.assertIn("this is doc", result.output)
        self.assertIn("--help", result.output)

    def test_no_argument(self):
        cli = self.generate_cli("tests/data/no-argument.cwl")

        runner = CliRunner()
        result = runner.invoke(cli, [])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("Usage:", result.output)