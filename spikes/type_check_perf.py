"""
Comparing performance of type checking methods.

For compatibility and performance (results below), we'll use:
  (type(val) is float or type(val) is int)
  which is a also pretty readable.

For now, with Vec classes we don't care too much about supporting classes
derived from float and int.  Therefore we don't need to use isinstance.
This may change since isinstance performance isn't that much slower.

Note: with python3, methods using IntType and FloatType aren't available.
"""

from __future__ import print_function

import sys
from timeit import timeit

# Results
# Results from the same test vary by as much as 0.2.
# The results below are close to the averages.
#
# Python 2.7.3:
# 0.1831138134 testing (a=float) isinstance(a, (float, int))
# 0.135299921036 testing (a=float) type(a) is float or type(a) is int
# 0.346937894821 testing (a=int) isinstance(a, (float, int))
# 0.254553079605 testing (a=int) type(a) is float or type(a) is int
#
# Python 2.7.3: Using IntType and FloatType, only available in Python 2
# 0.0941069126129 testing (a=float) type(a) is FloatType or type(a) is IntType
# 0.137171030045 testing (a=float) isinstance(a, (FloatType, IntType))
# 0.192821025848 testing (a=int) type(a) is FloatType or type(a) is IntType
# 0.269534826279 testing (a=int) isinstance(a, (FloatType, IntType))
#
# Python 3.3:
# 0.1748974630027078 testing (a=float) isinstance(a, (float, int))
# 0.11830268800258636 testing (a=float) type(a) is float or type(a) is int
# 0.3485602809814736 testing (a=int) isinstance(a, (float, int))
# 0.23826141195604578 testing (a=int) type(a) is float or type(a) is int
#


def main():
    print(timeit("isinstance(a, (float, int))", setup="a=5.0"),
          "testing (a=float) isinstance(a, (float, int))")
    print(timeit("type(a) is float or type(a) is int", setup="a=5.0"),
          "testing (a=float) type(a) is float or type(a) is int")
    print(timeit("isinstance(a, (float, int))", setup="a=5"),
          "testing (a=int) isinstance(a, (float, int))")
    print(timeit("type(a) is float or type(a) is int", setup="a=5"),
          "testing (a=int) type(a) is float or type(a) is int")
    print(timeit("type(a) in NUMERIC_TYPES",
                 setup="a=5;NUMERIC_TYPES=set([float, int])"),
          "testing (a=int) type(a) in predefined set([float, int])")
    print(timeit("type(a) in NUMERIC_TYPES",
                 setup="a=5.0;NUMERIC_TYPES=set([float, int])"),
          "testing (a=float) type(a) in predefined set([float, int])")

    # Tests below only work with python2
    if sys.version_info[0] > 2:
        return

    print()

    print(timeit("type(a) is FloatType or type(a) is IntType",
                 setup="from types import FloatType, IntType; a=5.0"),
          "testing (a=float) type(a) is FloatType or type(a) is IntType")
    print(timeit("isinstance(a, (FloatType, IntType))",
                 setup="from types import IntType, FloatType; a=5.0"),
          "testing (a=float) isinstance(a, (FloatType, IntType))")
    print(timeit("type(a) is FloatType or type(a) is IntType",
                 setup="from types import FloatType, IntType; a=5"),
          "testing (a=int) type(a) is FloatType or type(a) is IntType")
    print(timeit("isinstance(a, (FloatType, IntType))",
                 setup="from types import IntType, FloatType; a=5"),
          "testing (a=int) isinstance(a, (FloatType, IntType))")


if __name__ == "__main__":
    main()
