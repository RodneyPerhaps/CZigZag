from .cythonfcns import __identify_initial_pivot, _peak_valley_pivots, _max_drawdown, _pivots_to_modes, _peak_valley_pivots_candlestick

import numpy as np

VALLEY = -1
PEAK = 1


def _identify_initial_pivot(X, up_thresh, down_thresh):
    """Quickly identify the X[0] as a peak or valley."""
    return __identify_initial_pivot(X.astype(np.float64), float(up_thresh), float(down_thresh))

def peak_valley_pivots(X, up_thresh, down_thresh):
    """
    Finds the peaks and valleys of a series.

    Parameters
    ----------
    X : This is your series.
    up_thresh : The minimum relative change necessary to define a peak.
    down_thesh : The minimum relative change necessary to define a valley.

    Returns
    -------
    an array with 0 indicating no pivot and -1 and 1 indicating valley and peak
    respectively

    The First and Last Elements
    ---------------------------
    The first and last elements are guaranteed to be annotated as peak or
    valley even if the segments formed do not have the necessary relative
    changes. This is a tradeoff between technical correctness and the
    propensity to make mistakes in data analysis. The possible mistake is
    ignoring data outside the fully realized segments, which may bias analysis.
    """
    if down_thresh > 0:
        raise ValueError('The down_thresh must be negative.')

    return _peak_valley_pivots(X.astype(np.float64), float(up_thresh), float(down_thresh))


def compute_segment_returns(X, pivots):
    """Return a numpy array of the pivot-to-pivot returns for each segment."""
    pivot_points = X[pivots != 0]
    return pivot_points[1:] / pivot_points[:-1] - 1.0



def max_drawdown(X):
    """
    Return the absolute value of the maximum drawdown of sequence X.

    Note
    ----
    If the sequence is strictly increasing, 0 is returned.
    """
    return _max_drawdown(X.astype(np.float64))


def pivots_to_modes(pivots):
    """
    Translate pivots into trend modes.

    Parameters
    ----------
    pivots : the result of calling peak_valley_pivots

    Returns
    -------
    A numpy array of trend modes. That is, between (VALLEY, PEAK] it is 1 and
    between (PEAK, VALLEY] it is -1.
    """    
    return _pivots_to_modes(pivots.astype(np.int8))


def peak_valley_pivots_candlestick(close, high, low, up_thresh, down_thresh):
    """
    Finds the peaks and valleys of a series of HLC (open is not necessary).
    TR: This is modified peak_valley_pivots function in order to find peaks and valleys for OHLC.

    Parameters
    ----------
    close : This is series with closes prices.
    high : This is series with highs  prices.
    low : This is series with lows prices.
    up_thresh : The minimum relative change necessary to define a peak.
    down_thesh : The minimum relative change necessary to define a valley.

    Returns
    -------
    an array with 0 indicating no pivot and -1 and 1 indicating valley and peak
    respectively

    The First and Last Elements
    ---------------------------
    The first and last elements are guaranteed to be annotated as peak or
    valley even if the segments formed do not have the necessary relative
    changes. This is a tradeoff between technical correctness and the
    propensity to make mistakes in data analysis. The possible mistake is
    ignoring data outside the fully realized segments, which may bias analysis.
    """
    if down_thresh > 0:
        raise ValueError('The down_thresh must be negative.')

    return _peak_valley_pivots_candlestick(close.astype(np.float64),
                                           high.astype(np.float64),
                                           low.astype(np.float64),
                                           float(up_thresh),
                                           float(down_thresh))
