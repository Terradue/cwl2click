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

cwlVersion: v1.2

$graph:
- class: CommandLineTool
  id: clt_id
  requirements: {}
  baseCommand: 
  - basecommand
  arguments: 
  - argument
  inputs:
    directory-input:
      type: Directory?
      inputBinding:
        prefix: --directory-input
    file-input:
      type: File? 
      inputBinding:
        prefix: --file-input
    int-input:
      type: int?
      inputBinding:
        prefix: --int-input
    float-input:
      type: float?
      inputBinding:
        prefix: --float-input
    string-input:
      type: string?
      inputBinding:
        prefix: --string-input
  outputs:
    result:
      outputBinding:
        glob: .
      type: Directory