Endianness.py [![Unlicensed work](https://raw.githubusercontent.com/unlicense/unlicense.org/master/static/favicon.png)](https://unlicense.org/)
=============
[![PyPi Status](https://img.shields.io/pypi/v/Endianness.svg)](https://pypi.org/project/Endianness)
[![GitLab Build Status](https://gitlab.com/KOLANICH/Endianness.py/badges/master/pipeline.svg)](https://gitlab.com/KOLANICH/Endianness.py/pipelines/master/latest)
![GitLab Coverage](https://gitlab.com/KOLANICH/Endianness.py/badges/master/coverage.svg)
[![Coveralls Coverage](https://img.shields.io/coveralls/KOLANICH/Endianness.py.svg)](https://coveralls.io/r/KOLANICH/Endianness.py)
[![Libraries.io Status](https://img.shields.io/librariesio/github/KOLANICH/Endianness.py.svg)](https://libraries.io/github/KOLANICH/Endianness.py)


This is a library to compute ranges mapping of endiannesses. The library allows you to map (a) `slice`(s) of bits of a number of a certain length in provided generalized endianness to a `slice`s of bits of a number.

It is not yet ready.

Notation
-------------
An endianness is encoded as
`((?P<type>b|l)(?P<chunk_size_in_bits>\d+))+`

<details>
<summary>Examples</summary>


The examples of number `0x0123456789ABCDEF` encoded in different endianneses:
`b32` or `b16`  or `b8` or  `b4` or `b32_b16_b8_b4_b2` (also known as just "big endian")
`0123456789ABCDEF`

`l32` or `l32_b32` or `l32_b8`
`89ABCDEF 01234567`

`l32_b16_l8`
`AB/89|EF/CD 23/01|67/45`

`l16`
`CDEF 89AB 4567 0123`

`l8` (also known as just "little endian")
`EF CD AB 89 67 45 23 01`

`l4`
`F E D C B A 9 8 7 6 5 4 3 2 1 0`

</details>

Requirements
------------
* [`Python >=3.4`](https://www.python.org/downloads/). [`Python 2` is dead, stop raping its corpse.](https://python3statement.org/) Use `2to3` with manual postprocessing to migrate incompatible code to `3`. It shouldn't take so much time. For unit-testing you need Python 3.6+ or PyPy3 because their `dict` is ordered and deterministic.
* [`rangeslicetools`](https://github.com/KOLANICH/rangeslicetools.py) [![Unlicensed work](https://raw.githubusercontent.com/unlicense/unlicense.org/master/static/favicon.png)](https://unlicense.org/) [![PyPi Status](https://img.shields.io/pypi/v/rangeslicetools.svg)](https://pypi.org/project/rangeslicetools)
[![GitLab Build Status](https://gitlab.com/KOLANICH/rangeslicetools.py/badges/master/pipeline.svg)](https://gitlab.com/KOLANICH/rangeslicetools.py/pipelines/master/latest)
![GitLab Coverage](https://gitlab.com/KOLANICH/rangeslicetools.py/badges/master/coverage.svg)
[![Coveralls Coverage](https://img.shields.io/coveralls/KOLANICH/rangeslicetools.py.svg)](https://coveralls.io/r/KOLANICH/rangeslicetools.py)
[![Libraries.io Status](https://img.shields.io/librariesio/github/KOLANICH/rangeslicetools.py.svg)](https://libraries.io/github/KOLANICH/rangeslicetools.py)
