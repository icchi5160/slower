# Slower

学習・研究・個人開発を日本語Markdownで記録する個人技術ブログです。
Hugo Extended + PaperModで生成し、GitHub ActionsからGitHub Pagesへ公開します。

- 公開先: https://icchi5160.github.io/slower/
- リポジトリ: https://github.com/icchi5160/slower
- 進捗・承認記録はローカルの`IMPLEMENTATION_PLAN.md`で管理し、Gitの対象外とします。
- Phase 1〜7の実装・公開が完了しています。数式・図・検索・デザイン調整・品質チェックを導入済みです。

## 普段の記事投稿手順

初回準備が済んでいる場合は、次の流れで投稿できます。コマンドはリポジトリのルートで実行します。

1. 下書きを作成する。

   ```bash
   python3 scripts/blog.py new blog my-new-post --title "記事のタイトル"
   ```

2. `content/blog/my-new-post/index.md`をVS Codeなどで開き、タイトル・description・本文を編集する。テンプレートの`TODO:`は書き換えるか削除する。
3. ローカルサーバーを起動し、http://localhost:1313/blog/my-new-post/ を確認する。

   ```bash
   hugo server -D --disableFastRender
   ```

4. 公開準備ができたら`draft = false`にし、dateを公開日時に合わせる。未来の日時は通常の公開ビルドには含まれない。必要に応じてlastmodも更新する。
5. 別のターミナルで公開前チェックを実行する。

   ```bash
   python3 scripts/blog.py check
   ```

6. 変更内容を確認し、記事フォルダをコミット・pushする。

   ```bash
   git status --short
   git diff
   git add content/blog/my-new-post/
   git diff --cached
   git commit -m "Add new blog post"
   git push origin main
   ```

7. GitHub Actionsのbuild・deployが成功したら、[公開サイト](https://icchi5160.github.io/slower/)で記事とSearchへの反映を確認する。

`git add`は次のコミットに入れる変更を選びます。`git diff --cached`は選んだ変更の確認、`git commit`はローカル履歴への保存、`git push`はGitHubへの送信です。表示を終了する場合は`q`を押します。サイトの設定やデザインも変更した場合は、そのファイルも確認してコミットへ含めます。

**ローカルで表示されても、`draft = true`のままでは公開されません。** `-D`はローカルで下書きを表示するためのオプションです。

## 必要なツールと初回準備

- Git（submodule対応）
- Hugo **Extended 0.168.0**（CIと同じバージョンを推奨）
- Python **3.11以上**（執筆・品質チェック用。追加パッケージ不要）
- ブラウザ。数式・Mermaidの表示にはCDNへの接続が必要です。
- GitHub CLI `gh`は公開結果をCLIで見る場合に任意で使用します。

```bash
git clone --recurse-submodules https://github.com/icchi5160/slower.git
cd slower
git submodule update --init --recursive
git --version
hugo version
python3 --version
```

Hugoがない場合は[公式インストール手順](https://gohugo.io/installation/)に従ってExtended版を導入してください。`~/.local/bin`へ導入した場合は、そのディレクトリをPATHへ追加します。PythonはOSのパッケージ管理から3.11以上を導入してください。

PaperModは`themes/PaperMod`のsubmoduleです。固定コミットは`969bebdc5600a1639158b5ef4eff9cf6cbb511ac`。テーマ本体を直接編集せず、`layouts/`と`assets/css/extended/`で調整します。Hugo・テーマの更新は別作業として、ビルドとブラウザ確認後にバージョンを揃えて行います。

## ローカル起動

```bash
hugo server -D --disableFastRender
```

http://localhost:1313/ を開きます。終了は`Ctrl+C`。`-D`は下書きも表示します。通常の`hugo server`は下書きを除外します。下書きはローカル表示用であり、GitHubへpushしたMarkdown自体はPublicリポジトリから閲覧できます。

ローカルURLは`config/development/hugo.toml`、公開URLはルートの`hugo.toml`で管理します。ローカルは`/slower/`を付けずにアクセスしてください。ポートが使用中なら、起動済みサーバーを使うか`hugo server -D --port 1314`で別ポートにします。

## 新しい記事を作る

記事は原則Leaf Bundle（記事ごとのフォルダと`index.md`）で管理します。
slugは英小文字・数字をハイフンで区切ります。公開後のslug変更はURL変更になるため避けます。

```bash
python3 scripts/blog.py new notes python-pathlib --topic programming --title "pathlibの使い方" --summary "ファイルパス操作で学んだこと。" --tag Python
python3 scripts/blog.py new blog my-first-post --title "初めての記事"
python3 scripts/blog.py new research model-comparison --title "モデルの比較記録"
python3 scripts/blog.py new projects my-cli --title "CLIツールの開発記録" --tag Rust
```

`--tag`は繰り返し指定できます。`--summary`はdescriptionとsummaryの両方へ設定します。同じURLの記事がある場合は上書きしません。

Notesでは`--topic`が必須です。次の6分野から選びます。カテゴリも自動設定します。

| topic | 分野 |
| --- | --- |
| deep-learning | AI / Deep Learning |
| computer-vision | Computer Vision |
| programming | Programming |
| mathematics | Mathematics |
| security | Security |
| infrastructure | Infrastructure |

Pythonコマンドは内部でHugo標準の`hugo new content`を呼び出し、タイトル・概要・タグやNotesのカテゴリを設定します。Hugoコマンドを直接使う場合は、作成後にこれらを手動で編集します。生成される記事はどちらも同じMarkdown形式で、両方のコマンドを実行する必要はありません。

```bash
hugo new content notes/programming/python-pathlib/index.md
```

作成された`content/notes/programming/python-pathlib/index.md`を開いて編集します。VS Codeのターミナルでは、表示されたパスをCtrl+クリック（macOSではCmd+クリック）して開けます。

### メタデータと本文

```toml
+++
title = 'pathlibの使い方'
date = '2026-10-24T09:00:00+09:00'
lastmod = '2026-10-24T09:00:00+09:00'
draft = true
math = false
tags = ['Python']
categories = ['Programming']
description = 'ファイルパス操作で学んだこと。'
summary = ''
+++
```

- `title`: 記事タイトル。
- `date`: 公開日時。公開時に実際の日時へ直します。未来の日付は通常ビルドに出ません。
- `lastmod`: 内容を更新した日時を手動で設定します。省略時はdateを使用し、公開日より新しい場合は記事末尾に表示します。
- `draft`: 執筆中はtrue、公開準備ができたらfalse。
- `description`: 公開記事では必須の短い説明。
- `summary`: 一覧の要約。空なら本文から自動生成。
- `tags` / `categories`: 文字列の配列。使わなければ`[]`。
- `math`: 数式を使う記事のみtrue。

テンプレートの`TODO:`を自分の本文に置き換え、不要な見出しは削除します。見出しは記事タイトルと重複するh1を避け、`##`から始めます。大きなブロックの区切りには空行を挟んで`---`を置きます。コード以外のHTMLは原則使わず、標準Markdownで書きます。

## 記事の更新と画像

既存の`index.md`を編集し、実質的な内容変更ではlastmodを更新します。画像は記事フォルダに同梱し、英小文字とハイフンで命名します。

```text
content/notes/programming/python-pathlib/
├── index.md
└── path-example.webp
```

```markdown
![パス操作の入力と出力を示す図](path-example.webp)
```

記事中の画像には内容が分かる代替テキストを付けます。スクリーンショットは不要部分を切り、読める範囲で縮小・圧縮します。外部画像への直リンクより、公開権限を確認した画像の同梱を推奨します。個人情報・研究データ・認証情報の写り込みも確認してください。

別の記事へのリンクはHugoの`relref`を使うと、GitHub Pagesの`/slower/`を含むURLにも対応できます。

```markdown
[Transformerの基礎]({{< relref "/notes/deep-learning/transformer-basics" >}})
```

## コード・数式・図・目次・検索

### コード

コードフェンスに言語名（`python` / `c` / `rust` / `bash`など）を付けます。Chromaが色付けし、PaperModのコピーボタンが表示されます。長いコードは枠内でスクロールします。コード文字サイズはPaperMod標準（本文の0.78倍）で、フォントはVS Code標準に沿った等幅フォントの候補から端末にあるものを使用します。

````markdown
```python
from pathlib import Path
print(Path.cwd())
```
````

### KaTeX

front matterに`math = true`を指定します。インラインは`$...$`または`\(...\)`、独立行は`$$...$$`または`\[...\]`で囲みます。

```markdown
損失を $L$ とします。

$$
L = -\sum_i y_i \log p_i
$$
```

KaTeX 0.19.1をjsDelivrから整合性ハッシュ付きで読み込みます。math指定のないページでは読み込みません。金額の`$`は必要に応じて`\$`と書きます。

### Mermaid

言語名`mermaid`のコードブロックで記述します。図があるページだけMermaid 12.2.0をjsDelivrから読み込みます。ダークモード切替時も再描画します。

````markdown
```mermaid
flowchart LR
  Input[入力画像] --> Model[モデル] --> Output[分類結果]
```
````

### 目次と検索

目次は`##`と`###`から自動生成します。不要なページではfront matterに`ShowToc = false`を指定します。

SearchはPaperMod同梱のFuse.jsを使用し、タイトル・要約・本文を検索します。日本語の部分文字列と英語の技術用語に対応します。日本語の形態素解析は行いません。検索対象から外すページは`searchHidden = true`を指定します。公開ビルドの検索インデックスには下書きを含めません。

全機能の表示例: http://localhost:1313/blog/technical-writing-check/

## 公開前の品質チェック

```bash
python3 scripts/blog.py check
```

追加パッケージなしで次を確認し、失敗時は終了コード1と対象ファイル・行番号を表示します。

- MarkdownのTOML front matter、タイトル、日時、タグ等の型。
- 公開記事の説明と本文、lastmodとdateの順序、未記入の`TODO:`。
- 記事パスの命名、閉じ忘れたコードフェンス、空の見出し、画像の空の代替テキスト。
- 一時フォルダへの本番ビルド（下書き除外、警告・URL衝突で失敗）。
- 生成HTMLの内部リンク、画像・スクリプト等の参照、srcset、見出しアンカー。

生成先は終了時に削除され、起動中のローカル表示や既存の`public/`を置き換えません。リンクチェックは公開URLのサブパスを考慮します。外部リンク・CDNの接続確認、文章の内容の正しさ、完全なMarkdown構文解析、下書きのリンクチェックは対象外です。下書きのリンクは`hugo server -D`で確認してください。

### 補助ツールを修正したときのテスト

普段の執筆では、上の`python3 scripts/blog.py check`だけで十分です。次はチェック機能自体を検証する回帰テストで、リンク切れの検出や記事の上書き防止などを確認します。

```bash
python3 -m unittest discover -s tests -v
```

### 公開用ファイルを手元に残す場合

次の1行目は公開用ファイルを`public/`へ生成し、2行目はその生成物とMarkdownを検証します。CIもテスト後にこの順で実行します。通常のcheckコマンドと違い、終了後も`public/`が残ります。実行するだけでは公開されません。

```bash
hugo --gc --minify --panicOnWarning --printPathWarnings
python3 scripts/blog.py check --site-dir public
```

### 公開前に見ること

1. TODOを置き換え、description・date・lastmod・タグを確認する。
2. ローカルで本文、画像、コードコピー、数式、図、リンクを確認する。
3. PC・スマートフォン幅とライト／ダークモードで確認する。
4. 公開可能な内容か確認し、draftをfalseにする。
5. `python3 scripts/blog.py check`を実行する。
6. `git status --short`と`git diff`で公開対象を確認する。下書き・画像・履歴もPublicリポジトリでは閲覧可能。

## GitHub Pagesへ公開する

公開先は`icchi5160/slower`です。PagesのSourceは**GitHub Actions**を使用し、独自ドメインは未設定です。mainへのpushを契機にビルド・チェック・デプロイします。PRではビルドとチェックのみ実施します。

記事は`draft = false`にしてからチェック・コミット・pushします。以下は記事フォルダを指定して公開する例です。Codexへ外部操作を依頼する場合は、コミットとpushのどちらを行うか明示してください。

```bash
# 対象ファイルを確認してから、明示的に指定してステージする例
git add content/notes/programming/python-pathlib/
git diff --cached
# コードや設定変更がある場合は、それらも確認して追加する
git commit -m "Add pathlib learning note"
git push origin main
```

GitHubのリポジトリ画面で**Actions → Build and deploy Hugo → 最新の実行**を開きます。build・deployが成功したら https://icchi5160.github.io/slower/ の記事とSearchへの反映を確認します。

GitHub CLIがあれば次でも確認できます。

```bash
gh run list --repo icchi5160/slower --limit 5
gh run view <run-id> --repo icchi5160/slower --log-failed
```

ワークフローは`.github/workflows/hugo.yaml`にあります。HugoアーカイブのSHA-256を検証し、ActionsはコミットSHAで固定しています。通常はcontents:read、デプロイジョブだけpages:write / id-token:writeを与えます。

### デプロイエラーの確認

- **Test authoring tools**: テストの失敗内容と対象関数を確認する。
- **Build production site**: TOML・Markdown・テンプレートエラー、警告、テーマ取得を確認する。
- **Check Markdown and internal links**: 指摘された記事や参照先を修正する。`/notes/...`の直書きより`relref`を使う。
- **Configure Pages / Deploy to GitHub Pages**: PagesのSource、Actionsの権限、対象ブランチ、環境設定を確認する。
- **デプロイ成功なのに記事がない**: 記事が`draft = false`か、dateが未来になっていないかを確認する。`git show HEAD:content/blog/my-new-post/index.md`でコミット内の内容も確認する（パスは実際の記事へ置き換える）。
- **ローカルだけ新しい**: `git status --short`で未コミット変更を確認する。記事だけをgit addした場合、設定やCSSの変更は含まれない。最新実行のコミットと、反映したい変更が含まれるコミットを比較する。
- **表示が古い**: 閲覧先がhttps://icchi5160.github.io/slower/ かを確認し、ブラウザを再読み込みする。GitHub Pages側の反映待ちもある。

失敗を修正したらローカルチェックを再実行してpushします。ログへ認証情報を書かず、トークンを設定ファイルへ記入しないでください。

### 将来URLを変える場合

独自ドメインや`icchi5160.github.io`用リポジトリへの変更は可能です。実施時に`hugo.toml`のbaseURL、GitHub Pages設定、必要ならDNS・CNAME、ワークフローのフォールバックURLをまとめて変更します。`python3 scripts/blog.py check --base-url https://example.com/`で移行先URLでのビルドも検証できます。

## ファイルの役割と今後の管理

| パス | 編集内容 |
| --- | --- |
| hugo.toml | 公開URL、サイト名、プロフィール、GitHubリンク、ナビゲーション、検索等 |
| config/development/ | ローカルURLと旧ローカルパスのリダイレクト |
| content/ | Markdown記事、一覧説明、About、Search、記事画像 |
| archetypes/ | セクション別の記事テンプレート |
| layouts/ | PaperModのテンプレート上書きと拡張 |
| assets/css/extended/ | 文字、余白、背景、記事・コード・図の調整 |
| assets/js/ | 記事限定のKaTeX・Mermaid初期化 |
| assets/images/home/ | Home案内カードの生成画像原本と生成プロンプト記録 |
| scripts/blog.py | 記事作成・品質チェック |
| tests/test_blog_tools.py | チェックと記事作成の回帰テスト |
| .github/workflows/hugo.yaml | ビルド・チェック・GitHub Pages公開 |
| themes/PaperMod/ | submodule。直接変更しない |

Homeの自己紹介は`params.homeInfoParams.Content`、GitHubリンクは`params.socialIcons`、About本文は`content/about.md`で変更します。現在のプロフィールは仮の記述です。

3本の初期サンプルと技術機能の検証記事、ユーザーが作成した記事を掲載しています。サンプル記事は表示確認用です。不要なら`draft = true`にするか削除してください。架空の実験結果・実績を実際の成果として記載しない方針です。

Weeknotesは未作成です。追加する場合は`content/weeknotes/_index.md`と記事テンプレートを用意し、ナビゲーション・mainSections・作成チェック用のSECTIONSを必要に応じて更新します。

`public/`、`resources/_gen/`、PythonキャッシュはGit対象外です。チェック時の一時記事や生成物はリポジトリへ残しません。
