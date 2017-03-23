from __future__ import print_function
import numpy as np
import czigzag as czz
import zigzag as pzz
import time

def mytimeit(mod, a):
    t0 = time.time()
    pivots = mod.peak_valley_pivots(a, 0.03, -0.03)
    t1 = time.time()    
    modes = mod.pivots_to_modes(pivots)
    t2 = time.time()
    returns = mod.compute_segment_returns(a, pivots)
    t3 = time.time()
    drawdown = mod.max_drawdown(a)
    t4 = time.time()
    t = []
    t.append((t1-t0)*1000)
    t.append((t2-t1)*1000)
    t.append((t3-t2)*1000)
    t.append((t4-t3)*1000)
    return t, pivots, modes, returns, drawdown


def diff(name, a1, a2):
    print("{}: the two modules produce the same thing  = {}".format(name, np.array_equal(a1, a2)))


def run():
    size = 1000000
    a  = np.cumprod(1. + np.random.randn(size) * 0.01)
    t_pzz, pivots_pzz, modes_pzz, returns_pzz, drawdown_pzz = mytimeit(pzz, a)
    t_czz, pivots_czz, modes_czz, returns_czz, drawdown_czz = mytimeit(czz, a)

    print("CZigZag: execution time of peak_valley_pivots, pivots_to_modes, returns, max_drawdown = %7.1f, %7.1f, %7.1f, %7.1f ms" % (t_czz[0], t_czz[1], t_czz[2], t_czz[3]))
    print("ZigZag:  execution time of peak_valley_pivots, pivots_to_modes, returns, max_drawdown = %7.1f, %7.1f, %7.1f, %7.1f ms" % (t_pzz[0], t_pzz[1], t_pzz[2], t_pzz[3]))
    print("Speedup:                   peak_valley_pivots, pivots_to_modes, returns, max_drawdown = %7.1f, %7.1f, %7.1f, %7.1f" % (t_pzz[0]/t_czz[0], t_pzz[1]/t_czz[1], t_pzz[2]/t_czz[2], t_pzz[3]/t_czz[3]))

    diff('pivots', pivots_czz, pivots_pzz)
    diff('modes', modes_czz, modes_pzz)
    diff('returns', returns_czz, returns_pzz)
    diff('drawdown', drawdown_czz, drawdown_pzz)


def main():
    print("First run")
    run()
    print("Second run")
    run()


if __name__ == "__main__":
    main()

