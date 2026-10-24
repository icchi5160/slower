# Slower

学習・研究・個人開発の記録を蓄積する、日本語の個人技術ブログです。
GitHub Pagesで公開しています。公開サイト: https://icchi5160.github.io/slower/

## 必要なツール

- Git（確認環境: 2.43.0）
- Hugo **Extended v0.168.0**（公式の最新安定版を2026-10-24に確認）
- Go / Node.js / npmは現在の構成では不要です。

この環境では公式Linux amd64アーカイブのSHA-256を公式チェックサムと照合し、
`~/.local/bin/hugo`へ導入しました。`hugo version`に`+extended`が含まれることを確認してください。
コマンドが見つからない場合は`export PATH="$HOME/.local/bin:$PATH"`を実行してください。

別の環境では[公式インストール手順](https://gohugo.io/installation/)に従い、
[公式リリースv0.168.0](https://github.com/gohugoio/hugo/releases/tag/v0.168.0)からOS/CPUに合ったExtended版を導入してください。
アーカイブを公式チェックサムで検証してから、PATHの通ったディレクトリに配置します。
Git未導入の場合も[公式手順](https://git-scm.com/downloads)を参照してください。

## 初回取得

submoduleを含めてcloneします。

```bash
git clone --recurse-submodules https://github.com/icchi5160/slower.git
cd slower
```

通常のclone済み環境では、次のコマンドでテーマを取得できます。

```bash
git submodule update --init --recursive
```

PaperModは`themes/PaperMod`のGit submoduleでコミットを固定しています。
初期導入コミット: `969bebdc5600a1639158b5ef4eff9cf6cbb511ac`（必要Hugoバージョン: 0.158.0以上）。
テーマ本体は直接編集せず、将来の調整はプロジェクト側の`layouts/`や`assets/`で行います。
更新時は別途互換性を確認し、submoduleの更新を親リポジトリにも記録してください。

## ローカル起動

```bash
cd /home/icchi/slower
hugo server -D
```

ブラウザで <http://localhost:1313/> を開きます。停止は`Ctrl+C`です。
ヘッダーの「Slower」、PaperModのレイアウト、ライト／ダーク切替ボタンを確認できます。
Homeには仮の自己紹介、GitHubリンク、最新記事の一覧を表示します。Notes・Research・Projectsにはサンプル記事があります。Blogはまだ記事がありません。
`-D`は下書きも表示する指定で、通常のビルドには下書きは含まれません。
サーバーは標準でローカルホストにのみ公開されます。別PCから開発環境を使う場合は、
エディタ等で1313番ポートを転送してください。

## ビルド

```bash
hugo --panicOnWarning
```

`public/`に生成されます。生成物・キャッシュ・ビルドロックはGit管理から除外しています。
`baseURL`は公開URLの`https://icchi5160.github.io/slower/`です。`hugo server`ではローカル用URLになります。
mainへpushするとGitHub ActionsがビルドしてGitHub Pagesへ自動公開します。
リモートは`https://github.com/icchi5160/slower.git`です。

## 主なファイル

- `hugo.toml`: サイト名、日本語、タイムゾーン、テーマの基本設定
- `themes/PaperMod/`: テーマのsubmodule
- `archetypes/`: 共通・セクション別の記事テンプレート
- `IMPLEMENTATION_PLAN.md`: Phaseごとの進捗と承認状況

日本語設定は[現在のHugo設定仕様](https://gohugo.io/configuration/all/#locale)に合わせて
`locale`を使用し、非推奨の`languageCode`は使用していません。
テーマ導入方法は[PaperMod公式手順](https://github.com/adityatelange/hugo-PaperMod/wiki/Installation)を参照しています。

各Phase完了後はユーザー確認を待ち、明示的な承認後に次の1 Phaseだけ進めます。

## 基本ページとプロフィールの変更（Phase 2）

| ページ | URL | 編集するファイル |
| --- | --- | --- |
| Home | `/` | `hugo.toml`の`params.homeInfoParams`（自己紹介） |
| Notes | `/notes/` | `content/notes/_index.md` |
| Blog | `/blog/` | `content/blog/_index.md` |
| Research | `/research/` | `content/research/_index.md` |
| Projects | `/projects/` | `content/projects/_index.md` |
| About | `/about/` | `content/about.md` |
| タグ | `/tags/` | `content/tags/_index.md` |
| カテゴリ | `/categories/` | `content/categories/_index.md` |

ナビゲーションの名称と順番は`hugo.toml`の`menus.main`で変更します。
狭い画面ではPaperMod標準の横スクロールでメニューの末尾まで移動できます。

GitHubユーザー名はユーザー確認済みの`icchi5160`です。
リンクは`hugo.toml`の`params.socialIcons`にまとめ、HomeとAboutで共用しています。
Aboutのリンクは`layouts/_shortcodes/github-link.html`から参照します。
`params.author`は現在GitHubユーザー名を使用しています。必要なら希望の表示名に変更してください。

Homeの自己紹介とAboutのプロフィール・興味分野・使用技術は仮の内容と明記しています。
公開前に実際の内容へ更新してください。Aboutは記事の一覧には含めていません。
記事一覧はPaperMod標準レイアウトを使用し、Homeの一覧対象は
`params.mainSections`（notes / blog / research / projects）に設定しています。

タグとカテゴリはHugoのtaxonomy機能を使用します。Notesのリンクから一覧へ、
記事末尾のタグから同じタグの記事一覧へ移動できます。
Weeknotesは未作成です。後から他のセクションと同様に追加できます。

基本ページは[Hugoのセクション構成](https://gohugo.io/content-management/sections/)と
[PaperModのHome Infoモード](https://github.com/adityatelange/hugo-PaperMod/wiki/Features#home-info-mode)に沿って実装しています。

全ページの背景色は`assets/css/extended/background.css`で統一しています。
ライトモードは薄いグレー、ダークモードはテーマ標準の背景色です。

## Markdown記事の作成（Phase 3）

記事は`index.md`と画像を同じディレクトリにまとめるLeaf Bundleを基本とします。
英小文字とハイフンで記事ディレクトリ名を付けます。`index.md`は記事、`_index.md`は一覧ページです。

```text
content/
├── notes/
│   ├── _index.md
│   ├── deep-learning/transformer-basics/
│   │   ├── index.md
│   │   └── attention-overview.svg
│   ├── computer-vision/
│   ├── programming/
│   ├── mathematics/
│   ├── security/
│   └── infrastructure/
├── blog/
├── research/image-classification-experiment/index.md
└── projects/cli-tool-development/index.md
```

Notesの分野ディレクトリには`_index.md`を置いていないため、Notes一覧に配下の記事が並びます。
分野別の絞り込みにはカテゴリを使用します。空ディレクトリの`.gitkeep`はGit管理用で、記事にはなりません。

### 新規記事の作成

プロジェクトルートで実行します。各セクションのテンプレートは自動選択されます。

```bash
hugo new content notes/programming/my-first-note/index.md
hugo new content blog/my-first-post/index.md
hugo new content research/my-first-experiment/index.md
hugo new content projects/my-first-project/index.md
```

作成されたファイルをエディタで開き、タイトル・概要・本文・タグを記入します。
`archetypes/notes.md`などに、学習の目的・実験設定・プロジェクト概要といった見出しを用意しています。
これら以外の種類では`archetypes/default.md`を使用します。

### メタデータ

先頭の`+++`で囲まれた部分はTOML形式です。

```toml
title = '記事のタイトル'
date = '2026-10-24T09:00:00+09:00'
lastmod = '2026-10-24T09:00:00+09:00'
draft = true
tags = ['Python', '学習記録']
categories = ['Programming']
description = '記事の説明文です。'
summary = '記事一覧に表示する要約です。'
```

- `date`: 公開日。初期値は作成日時なので、公開時に必要に応じて変更します。
- `lastmod`: 最終更新日。本文を更新したときに手動で変更します。未指定なら`date`を使用します。
- `draft`: 初期値は`true`。`hugo server -D`で確認し、公開可能になったら`false`にします。
- `tags`: 複数付与できる技術用語やテーマ。空配列も使用できます。
- `categories`: 大分類。NotesはAI / Deep Learning、Computer Vision、Programming、Mathematics、Security、Infrastructureを基本とします。
- `description`: 詳細ページのタイトル下などに表示する説明。
- `summary`: 一覧に表示する要約。未指定時はHugoが本文から生成します。

公開日は記事上部に表示します。`lastmod`が`date`より新しい場合は本文末尾に更新日を表示します。
Gitのコミット日時やファイルの更新時刻には依存しません。
内容を更新しても記事ディレクトリ名と`date`は維持し、`lastmod`を変更する運用を基本とします。

### 画像の追加

記事の`index.md`と同じディレクトリに画像を置き、相対パスで参照します。

```markdown
![画像の内容を説明する代替テキスト](example.png)
```

サブディレクトリに置く場合は`images/example.png`のように指定します。
記事を移動するときは画像も含めてディレクトリごと移動してください。
Transformerのサンプルには、このリポジトリで作成したSVGの概念図を同梱しています。

### サンプル記事の確認・削除

- Notes: `/notes/deep-learning/transformer-basics/`
- Research: `/research/image-classification-experiment/`
- Projects: `/projects/cli-tool-development/`

サンプルはタイトル・要約・本文でサンプルと明記し、表示確認のため`draft = false`にしています。
Researchの実験は未実施、Projectsは未実装の構想例です。架空の測定値や公開実績はありません。
サンプルを公開対象から外すには`draft = true`に変更するか、該当する記事ディレクトリを削除してください。
`hugo server -D`では下書きも表示されるため、公開対象のみの確認には`hugo server`を使用します。

作成と構成は[Hugo公式Archetypes](https://gohugo.io/content-management/archetypes/)と
[Page bundles](https://gohugo.io/content-management/page-bundles/)に準拠しています。
更新日の優先順位は[公式front matter設定](https://gohugo.io/configuration/front-matter/)に従い明示しています。

### 文字サイズの調整

`assets/css/extended/typography.css`でPaperModの文字サイズを上書きしています。
標準のブラウザ設定では、PC（画面幅769px以上）は本文約20.8px、記事・ページタイトル約36.4px、本文の第2見出し約28.6pxです。
画面幅768px以下では本文16px、タイトル24px、第2見出し20pxです。
PCのみルートの文字サイズを130%にし、カードの要約や日付なども同じ倍率で表示します。
サイズにはremを使用し、ブラウザの既定フォントサイズの変更に追従します。

ブロック間の余白は`assets/css/extended/spacing.css`で調整しています。
Homeの自己紹介欄はテーマ標準の最小高さを解除し、内容に応じた高さにしています。
ヘッダーと本文の間、自己紹介とカードの間、カード同士、記事内の見出し・段落の余白を抑えています。
PC（画面幅769px以上）のコンテンツ最大幅は`--main-width: 1024px`です。
`spacing.css`で調整できます。スマートフォンの幅はテーマ標準を維持しています。

### 参考サイトに合わせた一覧レイアウト

Homeは自己紹介・GitHubリンク、Notes / Research / Projectsへの案内カード、記事一覧の順に表示します。
案内カードは`layouts/_partials/home_info.html`で既存ページのタイトル・説明文を参照します。
記事一覧は1100px以上で3列、769〜1099pxで2列、768px以下で1列です。
`assets/css/extended/spacing.css`で配置・カード間隔を調整しています。
ヘッダーと本文の最大幅を揃え、記事カードは行ごとに高さを揃えて日付を下端に配置します。
記事にカバー画像が指定された場合は16:9で表示します。現在のサンプルは画像なしのカードです。
参考サイトのコンテンツ・画像・CSSの流用はしていません。
PCヘッダーは高さ64pxで上下に余裕を持たせ、ナビゲーションを右寄せにしています。
メニュー項目の間隔は28pxです。スマートフォンでは高さ44pxのコンパクトな配置を維持しています。

ブロック間の余白は、コンパクト化した値から1.2倍に調整しています。記事グリッドの間隔は19.2px、案内カード間は14.4pxです。

### ブロック間の区切り線

内容の大きな区切りには、前後に空行を入れて`---`を記述します。

```markdown
前のブロックの本文。

---

## 次の見出し

次のブロックの本文。
```

記事・Aboutでは主な節の間、各セクショントップでは見出しと紹介本文の間に使用しています。
新規記事テンプレートにも区切り線を用意しています。段落ごとに追加する必要はありません。
Homeの自己紹介・案内・記事一覧間の区切りは`home_info.html`で出力します。
見た目は`spacing.css`で統一しています。タグ・カテゴリ一覧の本文は`layouts/taxonomy.html`で表示します。
プレビューの表示が更新されない場合は、サーバーを停止して`hugo server -D --disableFastRender`で起動し直してください。

## GitHub PagesとActions

### 公開先

- GitHubアカウント：`icchi5160`（ユーザー確認済み）
- リポジトリ：`icchi5160/slower`（Public）
- 公開URL：https://icchi5160.github.io/slower/
- デプロイ対象ブランチ：`main`

現在はリポジトリ名`slower`のプロジェクトサイトとして公開しています。
リポジトリ名`icchi5160.github.io`のユーザーサイトなら標準URLは`https://icchi5160.github.io/`になります。
その場合は`hugo.toml`の`baseURL`とワークフローのPR用`SITE_BASE_URL`の既定値を揃えて変更します。
mainのデプロイ時は`configure-pages`が返す実際のPages URLを優先します。

### ワークフロー

`.github/workflows/hugo.yaml`は次の処理を行います。

1. ソースとPaperMod submoduleを取得。
2. mainの公開時のみ、既に有効になっているPagesのURLを取得。
3. Hugo Extended v0.168.0をダウンロードし、固定したSHA-256で照合。
4. 本番用ビルドを実行。警告も失敗として扱います。
5. mainでは生成物をアップロードし、GitHub Pagesへデプロイ。

`main`へのpushと手動実行に対応し、main向けPRではビルド確認だけ行います。
下書き・将来日付の記事は通常のHugoの公開条件に従って除外します。
`public/`はGitにコミットしません。テーマのバージョンは親リポジトリのsubmoduleで固定します。

Actionsは公式のcheckout / configure-pages / upload-pages-artifact / deploy-pagesを使用し、コミットSHAで固定しています。
権限はビルドに`contents: read`と`pages: read`、デプロイに`pages: write`と`id-token: write`を付与しています。
個別のPATやAPIキーをワークフローへ登録する必要はありません。
Pagesの自動有効化は無効にしており、公開前にSettings側で有効化します。

### 認証と初回公開の手順

初回コミットとoriginの登録、mainへのpush、PagesのActions方式での有効化は実施済みです。
この環境は、ユーザー自身のログイン後にCLIの認証先が`icchi5160`であることを確認済みです。
別環境でのログイン時は、ブラウザで`icchi5160`を選んでください。
認証コードやトークンをチャットやリポジトリに貼り付ける必要はありません。

```bash
gh auth login --hostname github.com
gh api user --jq .login
```

複数アカウントを登録済みなら`gh auth switch --hostname github.com --user icchi5160`で選択できます。
最後のコマンドが`icchi5160`を返すことと、対象リポジトリへのアクセス権を確認します。
Gitのコミット作者名・メールはGitHubログインとは別の設定なので、初回コミット前に確認してください。

以下のリポジトリ作成・push・Pages有効化は、ユーザーの外部操作承認後に行います。

1. 既存リポジトリの有無を確認し、存在する場合は内容を確認します。404は未作成のほか、アクセス権がない場合もあります。
2. 未作成なら`icchi5160/slower`をPublicで作成します。既存リポジトリの公開設定は勝手に変更しません。
3. ローカルの公開対象を確認し、ソースとテーマsubmoduleを初回コミットに含め、対象リポジトリへpushします。
4. GitHubのリポジトリで **Settings → Pages → Build and deployment → Source → GitHub Actions** を選択します。
5. **Actions → Build and deploy Hugo → Run workflow** からmainを選択して実行します。
6. buildとdeployが成功し、デプロイ先URLでHome・各ページ・記事・画像を確認します。
7. 記事更新をmainへpushし、再度デプロイされて変更が反映されることを確認します。

初回pushがPages有効化より先だった場合、`Configure Pages`が失敗することがあります。
SourceをGitHub Actionsに設定した後、手動実行またはRe-run jobsで再実行してください。
無料運用はPublicリポジトリを前提とします。現在のサンプル3記事は`draft = false`なので、公開時にも含まれます。

### 本番ビルドのローカル確認

```bash
hugo --gc --minify --panicOnWarning --environment production
hugo server --disableFastRender
```

生成物を一時ディレクトリへ分ける場合は`--destination /tmp/slower-production-preview`を指定できます。
`hugo server -D`は下書きも表示するため、公開対象だけ確認するときは`-D`を外します。

### デプロイエラーの確認

GitHubの **Actions → Build and deploy Hugo → 対象の実行 → 失敗したjob / step** でログを開きます。

- Checkout：submodule取得が成功したか、`.gitmodules`とテーマのコミットがpushに含まれているか確認。
- Configure Pages：Settings → PagesのSourceがGitHub Actionsか、公開先リポジトリと権限が正しいか確認。
- Install Hugo Extended：ダウンロードエラーかチェックサム不一致かを確認。バージョン更新時は公式チェックサムと固定値も同時に更新。
- Build production site：ログのファイル名・行番号からMarkdown、TOML、テンプレートを修正し、同じ本番ビルドコマンドで確認。
- Deploy：github-pages environmentの承認待ち・対象ブランチの制限・Pages/OIDC権限を確認。
- 公開ページの表示：ActionsのデプロイURL、`baseURL`、ブラウザのキャッシュを確認。

workflowは[Hugo公式のPages手順](https://gohugo.io/host-and-deploy/deploy-to-github-pages/)と
[GitHub公式のPages作成手順](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)を参考に、
現在使用しないGo・Node.js・Dart Sassの導入を省いて構成しています。

独自ドメインには後から変更できます。取得したドメインのDNSとGitHub PagesのCustom domainを設定し、
`hugo.toml`の`baseURL`とworkflowのPRビルド用URLを変更して再デプロイします。
記事のMarkdownやLeaf Bundleの構成はそのまま利用できます。

### 記事更新の公開

Markdownと必要に応じて`lastmod`を更新し、ローカル表示を確認してからpushします。

```bash
hugo --gc --minify --panicOnWarning
git add content/
git commit -m "Update technical notes"
git push origin main
```

[Actionsの実行一覧](https://github.com/icchi5160/slower/actions)でbuild・deployの成功を確認し、
[公開サイト](https://icchi5160.github.io/slower/)で変更を確認します。
