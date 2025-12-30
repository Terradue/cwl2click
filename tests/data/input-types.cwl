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
    int-input:
      type: int
      inputBinding:
        prefix: --int-input
    float-input:
      type: float
      inputBinding:
        prefix: --float-input
    string-input:
      type: string
      inputBinding:
        prefix: --string-input
  outputs:
    result:
      outputBinding:
        glob: .
      type: Directory