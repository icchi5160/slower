{{- $name := .File.ContentBaseName -}}
{{- if eq $name "index" -}}
  {{- $name = path.Base .File.Dir -}}
{{- end -}}
+++
title = '{{ replace $name "-" " " | title }}'
date = '{{ .Date }}'
lastmod = '{{ .Date }}'
draft = true
tags = []
categories = []
description = '記事の概要を1〜2文で記入してください。'
summary = '一覧に表示する要約を記入してください。'
+++

## 目的

検証したい仮説を記入します。

---

## 実験設定

データセット、分割、前処理、モデル、環境、乱数シードを記録します。

---

## 結果

未実施の場合は「未実施」と明記し、実測値と予想を区別します。

---

## 考察・限界

---

## 再現手順・参考資料
