======
CZigZag
======

CZigZag is a fork of `ZigZag <https://github.com/jbn/ZigZag>`_ which provides functions
for identifying the peaks and valleys of a time series.

CZigzag is rewritten in Cython making it much faster:

- peak_valley_pivots is 40x faster
- pivots_to_modes is 250x faster
- max_drawdown is 4x faster
