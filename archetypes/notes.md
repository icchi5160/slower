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

## 学習の目的

TODO: 何を理解したいかを記入します。

---

## 要点

TODO: 学んだ内容を整理します。

---

## 確認したこと・未解決の疑問

---

## 参考資料
