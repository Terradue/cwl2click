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

from tests.utils import CWLClickTestCase


class TestImplicitPrefix(CWLClickTestCase, TestCase):

    def setUp(self):
        super().setUp()
        self.cli = self.generate_cli("tests/data/implicit-prefix.cwl")

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
