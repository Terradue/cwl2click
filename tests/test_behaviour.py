# Copyright 2025 Terradue
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from unittest import TestCase
from click.testing import CliRunner
from pathlib import Path
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
        self.assertIn("Usage: basecommand argument [OPTIONS]", result.output)
        self.assertIn("--input TEXT", result.output)
        self.assertIn("this is doc", result.output)
        self.assertIn("--help", result.output)

    def test_no_argument(self):
        cli = self.generate_cli("tests/data/no-argument.cwl")

        runner = CliRunner()
        result = runner.invoke(cli, [])

        self.assertEqual(result.exit_code, 2)
        self.assertIn("Usage: basecommand [OPTIONS]", result.output)
        self.assertIn("Try 'basecommand --help' for help.", result.output)
        self.assertIn("Error: Missing option '--directory-input'.", result.output)

    def test_multiple_basecommands(self):
        cli = self.generate_cli(Path("tests/data/multiple-basecommands.cwl"))

        self.assertIsNotNone(cli)
