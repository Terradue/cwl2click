cwlVersion: v1.2

$graph:
- class: CommandLineTool
  id: clt_id
  doc: "this is doc"
  label: "this is label"
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