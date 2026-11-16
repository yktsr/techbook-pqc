# Shorのアルゴリズムで、量子フーリエ変換のあとに測定すると何が出るかを計算するスクリプト
# N = 21, a = 2, x の候補は Q = 512 通り(9量子ビット)。Q は N^2 = 441 以上の2のべき乗にとる。
# 振幅のリストを古典計算で追い、測定値 y が出る確率 P(y) を求める。
import cmath
import math
from fractions import Fraction

N, a, Q = 21, 2, 512


def qft(amps):
    # 量子フーリエ変換: 長さ Q の振幅のリストを、別の振幅のリストに変える
    # 出力の y 番目 = (1/sqrt(Q)) * sum_x amps[x] * e^(2 pi i x y / Q)
    Q = len(amps)
    return [sum(amps[x] * cmath.exp(2j * cmath.pi * x * y / Q) for x in range(Q) if amps[x])
            / math.sqrt(Q) for y in range(Q)]


def measurement_probabilities():
    # 1. すべての x (0..Q-1) の重ね合わせを作り、a^x mod N を計算する
    f = [pow(a, x, N) for x in range(Q)]
    # 2. 計算結果の側で v が出たら、残るのは f(x) = v の x だけ。v ごとに量子フーリエ変換をかける
    #    振幅は 1/sqrt(個数) ではなく 1/sqrt(Q) のままにする。こうすると確率に
    #    「v が出る確率(個数/Q)」が最初から掛かる
    # 3. 確率は振幅の絶対値の2乗。v ごとの確率をそのまま足せば、y が出る確率になる
    P = [0.0] * Q
    for v in set(f):
        amps = [1 / math.sqrt(Q) if f[x] == v else 0.0 for x in range(Q)]
        out = qft(amps)
        for y in range(Q):
            P[y] += abs(out[y]) ** 2
    return P


if __name__ == '__main__':
    P = measurement_probabilities()
    print(f'N = {N}, a = {a}, Q = {Q} (9 qubits)')
    print(f'sum of P(y) = {sum(P):.3f}')
    peaks = sorted(sorted(range(Q), key=lambda y: -P[y])[:6])
    print('   y   P(y)   y/Q    closest fraction (denominator < N)')
    for y in peaks:
        frac = Fraction(y, Q).limit_denominator(N - 1)
        print(f'{y:4d}  {P[y]:.3f}  {y / Q:.3f}  {frac}')
    near = sum(P[y + d] for y in peaks for d in (-1, 0, 1) if 0 <= y + d < Q)
    print(f'probability of these 6 peaks and their neighbours = {near:.3f}')
    # 分母を集めて最小公倍数をとる(y = 0 の分母1は手がかりにならないので除く)
    dens = {Fraction(y, Q).limit_denominator(N - 1).denominator for y in peaks} - {1}
    dens = sorted(dens, reverse=True)
    r = math.lcm(*dens)
    print(f'denominators {", ".join(map(str, dens))} -> their least common multiple {r} is the period r')
