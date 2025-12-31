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