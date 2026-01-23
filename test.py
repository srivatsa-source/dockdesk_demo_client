import sys
from auditor import run_audit

if len(sys.argv) == 3:
    run_audit(sys.argv[1], sys.argv[2])
else:
    run_audit('auth.py', 'README.md')
