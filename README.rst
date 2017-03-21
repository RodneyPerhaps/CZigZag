======
cZigZag
======

cZigZag is a fork of `ZigZag <https://github.com/jbn/ZigZag>`_ which provides functions
for identifying the peaks and valleys of a time series.

cZigzag is rewritten in Cython making it much faster:
- peak_valley_pivots: 40x faster
- pivots_to_modes: 250x faster
- max_drawdown: 4x faster
