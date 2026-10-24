{{- $name := .File.ContentBaseName -}}
{{- if eq $name "index" -}}
  {{- $name = path.Base .File.Dir -}}
{{- end -}}
+++
title = '{{ replace $name "-" " " | title }}'
date = '{{ .Date }}'
lastmod = '{{ .Date }}'
draft = true
# 数式を使う記事ではtrueに変更する。
math = false
tags = []
categories = []
# 公開前にdescriptionを記入する。summaryは空なら本文から自動生成。
description = ''
summary = ''
+++

## 目的

TODO: 検証したい仮説を記入します。

---

## 実験設定

TODO: データセット、分割、前処理、モデル、環境、乱数シードを記録します。

---

## 結果

TODO: 未実施の場合は「未実施」と明記し、実測値と予想を区別します。

---

## 考察・限界

---

## 再現手順・参考資料
