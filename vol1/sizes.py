# 従来の公開鍵暗号と耐量子計算機暗号の、公開鍵・暗号文・署名のサイズを比べるスクリプト
# どの方式も OpenSSL で実際に鍵・暗号文・署名を生成して測る。
import subprocess
import tempfile


def sh(cmd, cwd):
    return subprocess.run(cmd, shell=True, cwd=cwd, check=True,
                          capture_output=True).stdout


def openssl_sizes(cwd, genpkey_args, op):
    sh(f'openssl genpkey {genpkey_args} -out k.pem', cwd)
    sh('openssl pkey -in k.pem -pubout -out pub.pem', cwd)
    spki = len(sh('openssl pkey -pubin -in pub.pem -outform DER', cwd))
    if op == 'kem':
        out = len(sh('openssl pkeyutl -encap -pubin -inkey pub.pem -out c.bin -secret s.bin'
                     ' && cat c.bin', cwd))
    elif op == 'rsa-oaep':
        out = len(sh('printf 0123456789abcdef0123456789abcdef | openssl pkeyutl -encrypt '
                     '-pubin -inkey pub.pem -pkeyopt rsa_padding_mode:oaep', cwd))
    elif op == 'ecdh':
        out = spki - 12  # 相手に送るのは一時公開鍵そのもの (SPKIヘッダ12バイトを除く)
    elif op == 'sign-digest':
        sig = sh('printf hello | openssl pkeyutl -sign -rawin -digest sha256 -inkey k.pem', cwd)
        out = len(ecdsa_der_to_raw(sig)) if genpkey_args.startswith('-algorithm EC') else len(sig)
    else:  # sign
        out = len(sh('printf hello > m.txt && openssl pkeyutl -sign -rawin -in m.txt -inkey k.pem', cwd))
    return spki, out


# ECDSA の署名は DER で (r, s) を包んでいて、長さが 70〜72 バイトで揺れる。
# 比較しやすいように、固定長の r || s (各32バイト) に直して測る。
def ecdsa_der_to_raw(der):
    pos = 2
    parts = []
    for _ in range(2):
        length = der[pos + 1]
        parts.append(int.from_bytes(der[pos + 2:pos + 2 + length], 'big').to_bytes(32, 'big'))
        pos += 2 + length
    return b''.join(parts)


if __name__ == '__main__':
    with tempfile.TemporaryDirectory() as d:
        print('--- key establishment ---')
        print(f'{"algorithm":<22}{"public key(SPKI)":>18}{"ciphertext":>12}')
        for name, args, op in [
            ('RSA-3072 (OAEP)', '-algorithm RSA -pkeyopt rsa_keygen_bits:3072', 'rsa-oaep'),
            ('X25519', '-algorithm X25519', 'ecdh'),
            ('ML-KEM-512', '-algorithm ML-KEM-512', 'kem'),
            ('ML-KEM-768', '-algorithm ML-KEM-768', 'kem'),
            ('ML-KEM-1024', '-algorithm ML-KEM-1024', 'kem'),
        ]:
            pk, ct = openssl_sizes(d, args, op)
            print(f'{name:<22}{pk:>18}{ct:>12}')

        print('--- signatures ---')
        print(f'{"algorithm":<22}{"public key(SPKI)":>18}{"signature":>12}')
        for name, args, op in [
            ('RSA-3072 (PKCS#1)', '-algorithm RSA -pkeyopt rsa_keygen_bits:3072', 'sign-digest'),
            ('ECDSA P-256 (r||s)', '-algorithm EC -pkeyopt ec_paramgen_curve:P-256', 'sign-digest'),
            ('Ed25519', '-algorithm ED25519', 'sign'),
            ('ML-DSA-44', '-algorithm ML-DSA-44', 'sign'),
            ('ML-DSA-65', '-algorithm ML-DSA-65', 'sign'),
            ('ML-DSA-87', '-algorithm ML-DSA-87', 'sign'),
            ('SLH-DSA-SHA2-128s', '-algorithm SLH-DSA-SHA2-128s', 'sign'),
            ('SLH-DSA-SHA2-128f', '-algorithm SLH-DSA-SHA2-128f', 'sign'),
        ]:
            pk, sig = openssl_sizes(d, args, op)
            print(f'{name:<22}{pk:>18}{sig:>12}')
