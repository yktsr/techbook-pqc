# Shorのアルゴリズムの流れを古典計算で追うスクリプト
# 量子計算機が担当するのは「a^x mod N の周期 r を見つける」部分だけで、
# 残りは古典計算(最大公約数)で済む。ここでは周期を総当たりで求めて代用する。
from math import gcd


# 量子計算機が高速に解く部分: a^r = 1 (mod N) となる最小の r (位数) を求める
def find_period(a, N):
    x, r = a % N, 1
    while x != 1:
        x = x * a % N
        r += 1
    return r


def shor(N, a):
    g = gcd(a, N)
    if g != 1:
        return g, N // g  # たまたま約数を引き当てた
    r = find_period(a, N)
    seq = [pow(a, x, N) for x in range(min(2 * r + 1, 10))]
    print(f'  a={a}: a^x mod {N} =', ' '.join(map(str, seq)), f'... -> period r={r}')
    if r % 2 == 1:
        print('    r が奇数なので失敗 (別の a でやり直す)')
        return None
    h = pow(a, r // 2, N)
    if h == N - 1:
        print(f'    a^(r/2) = -1 (mod {N}) なので失敗 (別の a でやり直す)')
        return None
    # a^r - 1 = (a^(r/2) - 1)(a^(r/2) + 1) = 0 (mod N) なので、どちらかが N と約数を共有する
    return gcd(h - 1, N), gcd(h + 1, N)


def success_rate(N):
    # N と互いに素な a (2 <= a <= N-1) のうち、周期から約数が求まるものを数える
    ok = total = 0
    for a in range(2, N):
        if gcd(a, N) != 1:
            continue
        total += 1
        r = find_period(a, N)
        if r % 2 == 0 and pow(a, r // 2, N) != N - 1:
            ok += 1
    return ok, total


if __name__ == '__main__':
    # 3233 = 61 x 53 は「実装しながら学ぶRSA暗号」で使った法
    # N = 21 では、失敗する 2 つの場合(r が奇数、a^(r/2) = -1)を先に試す
    for N, candidates in [(15, [7, 14]), (21, [4, 5, 2]), (3233, [3])]:
        print(f'N = {N}')
        for a in candidates:
            result = shor(N, a)
            if result:
                print(f'    factors: {N} = {result[0]} x {result[1]}')
                break
    print('success rate over a coprime to N')
    for N in (15, 21, 3233):
        ok, total = success_rate(N)
        print(f'  N = {N}: {ok} / {total} = {100 * ok / total:.0f}%')
