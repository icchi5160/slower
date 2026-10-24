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

## 背景

扱う課題やきっかけを記入します。

---

## 試したこと

---

## 分かったこと

---

## 参考資料
