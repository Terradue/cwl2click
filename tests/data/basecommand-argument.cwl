cwlVersion: v1.2

$graph:
- class: CommandLineTool
  id: clt_id
  label: "this is label"
  doc: "this is doc"
  requirements: {}
  baseCommand: 
  - basecommand
  arguments:
  - argument
  inputs:
    input:
      type: string
      label: "this is input label"
      doc: "this is input label"
      inputBinding:
        prefix: --input
  outputs:
    result:
      outputBinding:
        glob: .
      type: Directory