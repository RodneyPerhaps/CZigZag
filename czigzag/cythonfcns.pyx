import numpy as np
cimport numpy as np
cimport cython

cdef int VALLEY = -1
cdef int PEAK = 1

ctypedef np.float64_t FLOAT_t
ctypedef np.int8_t INT_t


@cython.boundscheck(False)
@cython.wraparound(False)
def __identify_initial_pivot(np.ndarray[FLOAT_t, ndim=1] X, double up_thresh, double down_thresh):
    cdef double x_0 = X[0]
    cdef double max_x = x_0
    cdef double max_t = 0
    cdef double min_x = x_0
    cdef double min_t = 0
    up_thresh += 1
    down_thresh += 1

    cdef long t
    cdef double x_t
    for t in range(1, X.size):
        x_t = X[t]

        if x_t / min_x >= up_thresh:
            return VALLEY if min_t == 0 else PEAK

        if x_t / max_x <= down_thresh:
            return PEAK if max_t == 0 else VALLEY

        if x_t > max_x:
            max_x = x_t
            max_t = t

        if x_t < min_x:
            min_x = x_t
            min_t = t

    cdef long t_n = X.size-1
    return VALLEY if x_0 < X[t_n] else PEAK


@cython.boundscheck(False)
@cython.wraparound(False)
def _peak_valley_pivots(np.ndarray[FLOAT_t, ndim=1] X, double up_thresh, double down_thresh):
    cdef int initial_pivot = __identify_initial_pivot(X, up_thresh, down_thresh)

    cdef long t_n = X.size
    cdef np.ndarray[INT_t, ndim=1] pivots = np.zeros(t_n, dtype=np.int8)
    pivots[0] = initial_pivot

    # Adding one to the relative change thresholds saves operations. Instead
    # of computing relative change at each point as x_j / x_i - 1, it is
    # computed as x_j / x_1. Then, this value is compared to the threshold + 1.
    # This saves (t_n - 1) subtractions.
    up_thresh += 1
    down_thresh += 1

    cdef int trend = -initial_pivot
    cdef long last_pivot_t = 0
    cdef double last_pivot_x = X[0]
    cdef long t
    cdef double x
    cdef double r
    for t in range(1, X.size):
        x = X[t]
        r = x / last_pivot_x

        if trend == -1:
            if r >= up_thresh:
                pivots[last_pivot_t] = trend
                trend = 1
                last_pivot_x = x
                last_pivot_t = t
            elif x < last_pivot_x:
                last_pivot_x = x
                last_pivot_t = t
        else:
            if r <= down_thresh:
                pivots[last_pivot_t] = trend
                trend = -1
                last_pivot_x = x
                last_pivot_t = t
            elif x > last_pivot_x:
                last_pivot_x = x
                last_pivot_t = t

    if last_pivot_t == t_n-1:
        pivots[last_pivot_t] = trend
    elif pivots[t_n-1] == 0:
        pivots[t_n-1] = -trend

    return pivots


@cython.boundscheck(False)
@cython.wraparound(False)
def _max_drawdown(np.ndarray[FLOAT_t, ndim=1] X):
    cdef double mdd = 0
    cdef double peak = X[0]
    cdef double dd
    cdef long i
    cdef double x
    for i in range(0, X.size):
        x = X[i]
        if x > peak: 
            peak = x
        dd = (peak - x) / peak
        if dd > mdd:
            mdd = dd
    return mdd


@cython.boundscheck(False)
@cython.wraparound(False)
def _pivots_to_modes(np.ndarray[INT_t, ndim=1] pivots):
    cdef np.ndarray[INT_t, ndim=1] modes = np.zeros(pivots.size, dtype=np.int8)
    modes[0] = pivots[0]
    cdef long mode = -modes[0]
    cdef long t
    cdef long x
    for t in range(1, pivots.size):
        x = pivots[t]
        if x != 0:
            modes[t] = mode
            mode = -x
        else:
            modes[t] = mode
    return modes


@cython.boundscheck(False)
@cython.wraparound(False)
def _peak_valley_pivots_candlestick(np.ndarray[FLOAT_t, ndim=1] close, np.ndarray[FLOAT_t, ndim=1] high, np.ndarray[FLOAT_t, ndim=1] low, double up_thresh, double down_thresh):
    cdef int initial_pivot = __identify_initial_pivot(close, up_thresh, down_thresh)

    cdef long t_n = close.size
    cdef np.ndarray[INT_t, ndim=1] pivots = np.zeros(t_n, dtype=np.int8)
    pivots[0] = initial_pivot

    # Adding one to the relative change thresholds saves operations. Instead
    # of computing relative change at each point as x_j / x_i - 1, it is
    # computed as x_j / x_1. Then, this value is compared to the threshold + 1.
    # This saves (t_n - 1) subtractions.
    up_thresh += 1
    down_thresh += 1

    cdef int trend = -initial_pivot
    cdef long last_pivot_t = 0
    cdef double last_pivot_x = close[0]
    cdef long t
    cdef double x
    cdef double r
    for t in range(1, close.size):

        if trend == -1:
            x = low[t]
            r = x / last_pivot_x
            if r >= up_thresh:
                pivots[last_pivot_t] = trend
                trend = 1
                last_pivot_x = high[t]
                last_pivot_t = t
            elif x < last_pivot_x:
                last_pivot_x = x
                last_pivot_t = t
        else:
            x = high[t]
            r = x / last_pivot_x
            if r <= down_thresh:
                pivots[last_pivot_t] = trend
                trend = -1
                last_pivot_x = low[t]
                last_pivot_t = t
            elif x > last_pivot_x:
                last_pivot_x = x
                last_pivot_t = t


    if last_pivot_t == t_n-1:
        pivots[last_pivot_t] = trend
    elif pivots[t_n-1] == 0:
        pivots[t_n-1] = trend

    return pivots
