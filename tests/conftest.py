import os
import sys

# Make omnibot importable from tests/. Priority:
# 1. mutmut temp dir (prepended by mutmut automatically)
# 2. 03-development/src (project source)
_src = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "03-development", "src")
if _src not in sys.path:
    sys.path.insert(1, _src)  # position 1 so mutmut's temp dir at position 0 wins
