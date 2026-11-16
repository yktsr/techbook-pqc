# 量子計算の3つのルールを、振幅のリストで追うスクリプト
#   1. n 量子ビットの状態は 2^n 個の振幅のリスト(2乗の合計は1)
#   2. 操作(ゲート)はリスト全体を書き換える(2乗の合計は保たれる)
#   3. 測定すると値が1つ、振幅の2乗の確率で得られ、リストは失われる
import random
from math import sqrt


def hadamard(amp, j):
    # j 番目の量子ビットにアダマール変換をかける: (a, b) -> ((a + b)/sqrt2, (a - b)/sqrt2)
    out = amp[:]
    for i in range(len(amp)):
        if not (i >> j) & 1:                 # j 番目のビットが 0 の値と 1 の値を組にする
            a, b = amp[i], amp[i | 1 << j]
            out[i], out[i | 1 << j] = (a + b) / sqrt(2), (a - b) / sqrt(2)
    return out


def measure(amp, rng):
    # 値を1つ、振幅の2乗の確率で引く。振幅そのものは返さない
    return rng.choices(range(len(amp)), weights=[a * a for a in amp])[0]


def flip_coin(p):
    # 古典のコインを投げ直す: 表裏の確率は混ざって 50% ずつになるだけ
    return [(p[0] + p[1]) / 2, (p[0] + p[1]) / 2]


def show(v):
    return '[' + ', '.join(f'{x:+.3f}' for x in v) + ']'


if __name__ == '__main__':
    rng = random.Random(2026)
    n = 3
    amp = [1.0] + [0.0] * (2 ** n - 1)       # リセット: 000 の振幅だけが 1
    print('reset    :', show(amp))
    for j in range(n):
        amp = hadamard(amp, j)
    print('H x 3    :', show(amp))
    print('sum of squares =', f'{sum(a * a for a in amp):.3f}')
    # 本物の量子計算機では測ると状態が失われるので、8回測るにはリセットからやり直す。
    # measure は amp を書き換えないので、同じ amp から8回引けば同じことになる
    print('measure 8 times:', ' '.join(f'{measure(amp, rng):03b}' for _ in range(8)))
    print('coin vs qubit')
    p, a = [1.0, 0.0], [1.0, 0.0]
    print(f'  start   : coin P = {show(p)}  qubit amp = {show(a)}')
    for k in (1, 2):
        p, a = flip_coin(p), hadamard(a, 0)
        print(f'  {k} flip{"s" if k > 1 else " "} : coin P = {show(p)}  qubit amp = {show(a)}')
    # 測ると区別できない2つの状態も、アダマール変換をかけると結果が分かれる
    for start in ([1 / sqrt(2), 1 / sqrt(2)], [1 / sqrt(2), -1 / sqrt(2)]):
        print(f'  H{show(start)} = {show(hadamard(start, 0))}')
