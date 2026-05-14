#!/bin/bash
# mutmut test runner — adds both the original source and mutmut's temp dir to PYTHONPATH
# PYTHONPATH order: original source first (for test imports), mutmut temp dir prepends automatically
export PYTHONPATH="03-development/src:${PYTHONPATH}"
python3 -m pytest tests/ -x --tb=no -q "$@"
