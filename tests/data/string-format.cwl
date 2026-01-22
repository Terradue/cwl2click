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
  requirements:
    - class: SchemaDefRequirement
      types:
      - $import: https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml
  baseCommand: 
  - basecommand
  arguments: 
  - argument
  inputs:
    uri-input:
      type: https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URI
      label: "Product URI"
      doc: "Product URI in string format"
      inputBinding:
        prefix: --uri-input
    uuid-input:
      type: https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#UUID
      label: "Product UUID"
      doc: "Product UUID in string format"
      inputBinding:
        prefix: --uuid-input
  outputs:
    result:
      outputBinding:
        glob: .
      type: Directory