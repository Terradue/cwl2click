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
        