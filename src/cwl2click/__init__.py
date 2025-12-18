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

from cwl_loader.utils import (
    assert_process_contained,
    search_process
)
from cwl_utils.parser import Process
from typing import (
    List,
    TextIO
)

def to_click(
    cwl_document: Process | List[Process],
    workflow_id: str,
    output_stream: TextIO
):
    assert_process_contained(
        process=cwl_document,
        process_id=workflow_id
    )

    process: Process | None = search_process(
        process_id=workflow_id,
        process=cwl_document
    ) # can't be None, at that point
