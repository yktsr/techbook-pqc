# Groverのアルゴリズムを、振幅(各候補の「重み」)の計算として古典計算で追うスクリプト
# 量子計算機は N 個の振幅をまとめて扱えるが、測定すると候補が1つだけ得られ、
# 候補 i が得られる確率は振幅の2乗 amp[i]**2 になる。
from math import pi, sqrt


def grover_step(amp, target):
    amp[target] = -amp[target]               # 1. 答えの振幅だけ符号を反転する(実機では「確かめる計算」で行う)
    mean = sum(amp) / len(amp)
    return [2 * mean - a for a in amp]       # 2. 平均値を軸に折り返す(拡散)


def best_iterations(N, target=0):
    # 答えが得られる確率が最大になる繰り返し回数を探す
    amp = [1 / sqrt(N)] * N
    k, prob = 0, amp[target] ** 2
    while True:
        nxt = grover_step(amp, target)
        if nxt[target] ** 2 < prob:
            return k, prob
        amp, k, prob = nxt, k + 1, nxt[target] ** 2


if __name__ == '__main__':
    N, target = 16, 11
    amp = [1 / sqrt(N)] * N                  # 最初はすべての候補が同じ重み
    print(f'N = {N}, answer = {target}')
    print('  k  amp[answer]  amp[other]  P(answer)')
    for k in range(7):
        other = amp[(target + 1) % N]
        print(f'  {k}  {amp[target]:+.3f}       {other:+.3f}      {amp[target] ** 2:.3f}')
        amp = grover_step(amp, target)
    print('iterations needed (classical search needs about N/2 tries on average)')
    print('      N  best k  P(answer)   (pi/4)*sqrt(N)')
    for bits in (4, 8, 12, 16):
        N = 2 ** bits
        k, prob = best_iterations(N)
        print(f'  2^{bits:<2}  {k:6d}  {prob:9.4f}  {pi / 4 * sqrt(N):8.1f}')
