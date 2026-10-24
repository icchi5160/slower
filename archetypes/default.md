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

TODO: ここに本文を記入します。
