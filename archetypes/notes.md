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

## 学習の目的

何を理解したいかを記入します。

---

## 要点

学んだ内容を整理します。

---

## 確認したこと・未解決の疑問

---

## 参考資料
