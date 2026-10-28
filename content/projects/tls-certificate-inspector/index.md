+++
title = 'tls-certificate-inspector'
date = '2026-10-29T00:00:00+09:00'
lastmod = '2026-10-29T00:00:00+09:00'
draft = false
math = false
tags = ['C++', 'TLS', 'wolfSSL', 'CLI']
categories = ['Security']
description = 'wolfSSLを使い、TLSサーバーの証明書を検証・表示するC++製CLIツール。'
summary = 'TLSライブラリへの理解を深めるために開発した、証明書の検証・情報表示ツール。'
+++

## 概要

TLSサーバーへ接続し、検証に成功したサーバー証明書の情報を表示するCLIツール。C++17とwolfSSLを使用している。

証明書のSubject・Issuer・有効期間・SAN・公開鍵の情報や、SHA-256フィンガープリントを確認できる。出力形式は、人が読みやすいテキストとJSONに対応している。

---

## 開発経緯

TLSライブラリへの理解を深めるために開発した。wolfSSLを使って接続・証明書検証・情報取得を実装し、TLSライブラリの使い方と、証明書を検証する流れをコードを通して学ぶことを目的とした。

---

## 使用技術

| 技術 | 用途 |
| --- | --- |
| C++17 | CLIツールの実装、RAIIによるリソース管理 |
| wolfSSL | TLS接続、証明書検証、証明書情報の取得 |
| CMake / CTest | ビルドとテストの実行 |
| Python / cryptography | テスト用証明書の生成と結合テスト |
| GitHub Actions | ビルド・テストの自動実行 |

---

## 主な機能

- TLS 1.3での接続と、明示的なTLS 1.2の選択。
- 証明書の検証、ホスト名検証、SNIへの対応。
- 証明書情報のテキスト・JSON出力。
- DNS解決・TCP接続・TLSハンドシェイクで共通のタイムアウトを使用。
- ローカルのテスト用CA・証明書・TLSサーバーを使ったテスト。

---

## GitHubリポジトリ

[icchi5160/tls-certificate-inspector](https://github.com/icchi5160/tls-certificate-inspector)

ビルド方法・使用例・対応範囲の詳細は、[リポジトリのREADME](https://github.com/icchi5160/tls-certificate-inspector/blob/master/README.md)に記載している。
