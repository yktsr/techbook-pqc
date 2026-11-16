# 実装しながら学ぶ耐量子計算機暗号

同人誌「実装しながら学ぶ耐量子計算機暗号」(サークル電気羊)のプログラムです。

## vol1/ 量子計算機編

第1巻に載せたプログラムと、その実行結果(`.txt`)です。
量子計算機のプログラムは、量子ビットの状態を数(振幅)のリストとして、古典計算機で追うものです。

| ファイル | 本書での位置 | 内容 |
| --- | --- | --- |
| `qubit_basics.py` | Script 2.1、2.2 | 量子計算の3つのルール(状態・ゲート・測定)を振幅のリストで追う |
| `shor_classical.py` | Script 2.3、2.4 | Shorのアルゴリズムの流れを古典計算で追う |
| `shor_qft.py` | Script 2.5、2.6 | 量子フーリエ変換のあとの測定値の確率を求める |
| `grover_sim.py` | Script 2.7、2.8 | Groverのアルゴリズムの振幅の変化を追う |
| `sizes.py` | 図3.1 | 従来の公開鍵暗号と耐量子計算機暗号の、公開鍵・暗号文・署名のサイズを、OpenSSLで実際に生成して比べる |

### 動かし方

Python 3.9以上の標準ライブラリだけで動きます。

```bash
cd vol1
python3 qubit_basics.py
```

乱数はすべて固定してあるので、実行結果は本書(と同じフォルダの `.txt`)と同じになります。

`sizes.py` だけは、OpenSSL 3.5以上が必要です(ML-KEMとML-DSAに対応した版)。
macOS標準の `/usr/bin/openssl` はLibreSSLで、これらに対応していないので、Homebrewなどで入れたOpenSSLを先にPATHに置いてください。

動作は macOS 27.2、Python 3.9.6、OpenSSL 3.6.4 で確認しました。

## ライセンス

MIT License([LICENSE](LICENSE))
