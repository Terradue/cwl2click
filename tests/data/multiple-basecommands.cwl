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

- class: CommandLineTool
  id: clt_id_2
  label: "this is label"
  doc: "this is doc"
  requirements: {}
  baseCommand: 
  - basecommand-2
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

- class: CommandLineTool
  id: clt_id_3
  requirements: {}
  baseCommand: 
  - basecommand-3
  arguments: []
  inputs:
    directory-input:
      type: Directory
      inputBinding:
        prefix: --directory-input
  outputs:
    result:
      outputBinding:
        glob: .
      type: Directory

- class: CommandLineTool
  id: clt_id_4
  requirements: {}
  baseCommand: 
  - basecommand-4
  arguments: []
  inputs:
    directory-input:
      type: Directory
      inputBinding:
        prefix: --directory-input
  outputs:
    result:
      outputBinding:
        glob: .
      type: Directory
