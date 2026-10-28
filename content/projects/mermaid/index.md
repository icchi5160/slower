+++
title = 'mermaid'
date = '2026-10-29T00:00:00+09:00'
lastmod = '2026-10-29T00:00:00+09:00'
draft = false
math = false
tags = ['Mermaid', 'JavaScript', 'Vite', '可視化']
categories = ['Programming']
description = 'Mermaid記法のクラス図をブラウザで編集・描画し、SVG・PNGで保存するローカルツール。'
summary = 'Mermaid記法で書いたファイルの内容を図として描画するために開発した、Mermaid Class Studioの紹介。'
+++

## 概要

Mermaid Class Studioは、Mermaid記法のクラス図をブラウザで編集・描画するローカルツール。ソースを編集して図を確認し、レイアウトや描画方向を切り替えながら見やすい配置を選べる。

図の移動・拡大縮小に対応し、描画した図はSVGやPNGとして保存できる。描画処理はローカルのブラウザ内で行う。

---

## 開発経緯

Mermaid記法で書いたファイルの内容を、図として描画したかったために開発した。ソースを編集しながら描画結果を確認し、図として保存できるツールにした。

---

## 使用技術

| 技術 | 用途 |
| --- | --- |
| JavaScript / HTML / CSS | 編集画面と操作機能の実装 |
| Mermaid | クラス図の描画 |
| ELK / Dagre | 図のレイアウト |
| Vite / Node.js | 開発サーバーとビルド |
| Playwright | ブラウザテスト |

---

## 主な機能

- Mermaidソースの編集と描画。
- ELK・Dagreの切り替えと、4方向の配置の比較。
- ドラッグによる移動、拡大縮小、全体表示。
- SVG・PNG形式での画像保存。

---

## GitHubリポジトリ

[icchi5160/mermaid](https://github.com/icchi5160/mermaid)

起動方法・操作方法の詳細は、[リポジトリのREADME](https://github.com/icchi5160/mermaid/blob/main/README.md)に記載している。
