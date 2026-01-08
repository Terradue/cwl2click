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
      type: Directory
      inputBinding:
        prefix: --directory-input
    file-input:
      type: File
      inputBinding:
        prefix: --file-input
  outputs:
    result:
      outputBinding:
        glob: .
      type: Directory