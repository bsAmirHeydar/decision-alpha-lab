fix(lcm): verify LF and CRLF baseline materializations symmetrically

- accept only raw, all-LF, or all-CRLF byte-equivalent text materializations
- preserve strict binary and semantic-content integrity
- report LF and CRLF equivalence counts separately
- add reverse-direction and mixed-EOL regression coverage
- make the PowerShell apply pipeline fail immediately on native command failure
