CZigZag
=======

CZigZag is a fork of `ZigZag <https://github.com/jbn/ZigZag>`_ which provides functions
for identifying the peaks and valleys of a time series.

For maximum speed, CZigzag is written in Cython while ZigZag can optionally use numba just-in-time compilation. If numba can be installed, CZigZag seems to be a little bit faster (10%). If numba can't be installed, CZigZag is much faster than pure Python code:

- peak_valley_pivots is 50x faster
- pivots_to_modes is 900x faster
- max_drawdown is 140x faster

Installation
------------

pip install git+https://github.com/jewicht/ZigZag.git
