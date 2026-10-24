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

## 概要

TODO: 解決したい課題と対象ユーザーを記入します。

---

## 使用技術

---

## 開発経緯

---

## 現在の状態

TODO: 構想・開発中・公開済みなど、実際の状態を記入します。

---

## GitHubリポジトリ

TODO: 公開済みの実際のURLを記入します。
