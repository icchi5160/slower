+++
aliases = ['/blog/first-tech-note/']
title = "初めての技術記事"
date = '2026-10-24T16:09:35+09:00'
lastmod = '2026-10-24T16:09:35+09:00'
draft = true
# 数式を使う記事ではtrueに変更する。
math = false
# カードにつくタグ
tags = ['sample'] 
# ナビゲーションカテゴリ
categories = ['Notes'] 
# 各コンテンツページのタイトルの下に表示される
description = '別に技術記事じゃなくてブログのコンテンツ作成のテスト'
# カードに表示される説明
summary = 'いろいろ記入してみて表示を確認する用のノート'
+++

## 背景

これは初めて自分で書く記事。新しい記事を投稿する際の手順を書いておく。

---

## 新しい記事の投稿手順

### ローカルで記事下書き作成，編集，チェック
```python
python3 scripts/blog.py new articles python-pathlib --topic programming --title "pathlibの使い方" --summary "ファイルパス操作で学んだこと。" --tag Python

(draftのパスが表示されるのでctrl+clickで開いて，内容を書く)
(draftタグをfalseにする)

python3 scripts/blog.py check

hugo -D server # localで表示を確認
```

### git pushで投稿
```bash
# 対象ファイルを確認してから、明示的に指定してステージする例
git add content/articles/python-pathlib/
git diff --cached # 変更の確認
# コードや設定変更がある場合は、それらも確認して追加する
git commit -m "Add pathlib learning note"
git push origin main

# GitHub Actionでビルド・デプロイが成功したか確認
gh run list --repo icchi5160/slower --limit 5
```

---

## 参考資料

なし