from unittest import TestCase
from click.testing import CliRunner

from tests.utils import CWLClickTestCase


class TestStructure(CWLClickTestCase, TestCase):

    def setUp(self):
        super().setUp()

    def test_missing_required_option_fails(self):
        cli = self.generate_cli("tests/data/input-types.cwl")

        runner = CliRunner()
        result = runner.invoke(cli, ["argument"])

        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Missing option", result.output)