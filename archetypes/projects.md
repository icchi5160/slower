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

## 概要

解決したい課題と対象ユーザーを記入します。

---

## 使用技術

---

## 開発経緯

---

## 現在の状態

構想・開発中・公開済みなど、実際の状態を記入します。

---

## GitHubリポジトリ

公開済みの実際のURLを記入します。
