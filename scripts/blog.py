#!/usr/bin/env python3
"""Slowerの記事作成と、Markdown・生成サイトの検証。追加ライブラリ不要。"""
from __future__ import annotations

import argparse
from datetime import date, datetime, time
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from urllib.parse import unquote, urljoin, urlsplit
from zoneinfo import ZoneInfo

try:
    import tomllib
except ModuleNotFoundError:
    raise SystemExit("Python 3.11以上が必要です。")

ROOT = Path(__file__).resolve().parents[1]
SECTIONS = ("articles", "research", "projects")
TOPICS = {
    "deep-learning": "AI / Deep Learning",
    "computer-vision": "Computer Vision",
    "programming": "Programming",
    "mathematics": "Mathematics",
    "security": "Security",
    "infrastructure": "Infrastructure",
}
SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")


def read_post(path: Path) -> tuple[dict, str, int]:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    if not lines or lines[0].strip() != "+++":
        raise ValueError("先頭にTOML front matter（+++）が必要です")
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "+++"), None)
    if end is None:
        raise ValueError("front matterを閉じる+++がありません")
    return tomllib.loads("".join(lines[1:end])), "".join(lines[end + 1:]), end + 2


def as_datetime(value: object, tz: ZoneInfo) -> datetime:
    if isinstance(value, datetime):
        result = value
    elif isinstance(value, date):
        result = datetime.combine(value, time.min)
    elif isinstance(value, str):
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    else:
        raise ValueError("ISO形式の日付・日時で指定してください")
    return result.replace(tzinfo=tz) if result.tzinfo is None else result


def body_errors(body: str, published: bool) -> list[tuple[int, str]]:
    errors = []
    # コメントを除いて検証しつつ、元の行番号を保つ。
    visible = re.sub(r"<!--.*?-->", lambda m: "\n" * m[0].count("\n"), body, flags=re.S)
    # フェンスとTODOは原文で調べる。コード内のTODOや画像記法は検証対象外。
    fence = None
    meaningful = False
    for number, line in enumerate(body.splitlines(), 1):
        match = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if fence:
            if match and match[1][0] == fence[0] and len(match[1]) >= fence[1] and not match[2].strip():
                fence = None
            elif line.strip():
                meaningful = True
            continue
        if match:
            fence = (match[1][0], len(match[1]), number)
            continue
        if re.match(r"^ {0,3}#{1,6}\s*$", line):
            errors.append((number, "空の見出しがあります"))
        if published and re.search(r"<!--\s*TODO:|^ {0,3}TODO:", line):
            errors.append((number, "公開記事にテンプレートのTODOが残っています"))
        without_code = re.sub(r"`+[^`]*`+", "", line)
        if re.search(r"!\[\s*\](?:\(|\[)", without_code):
            errors.append((number, "記事画像には空でない代替テキストを付けてください"))
    if fence:
        errors.append((fence[2], "コードブロックのフェンスが閉じていません"))
    for line in visible.splitlines():
        if not re.match(r"^\s*(?:#{1,6}\s|[-*_]{3,}\s*$|`{3,}|~{3,})", line) and re.search(r"[^\s#>*_~`|=-]", line):
            meaningful = True
    if published and not meaningful:
        errors.append((1, "公開記事の本文が空です"))
    return errors


def markdown_errors(root: Path, config: dict) -> list[str]:
    errors = []
    tz = ZoneInfo(config.get("timeZone", "Asia/Tokyo"))
    for path in sorted((root / "content").rglob("*.md")):
        label = path.relative_to(root).as_posix()
        try:
            meta, body, start = read_post(path)
        except (ValueError, UnicodeError) as exc:
            errors.append(f"{label}:1: {exc}")
            continue
        if not isinstance(meta.get("title"), str) or not meta["title"].strip():
            errors.append(f"{label}:1: titleが空、または文字列ではありません")
        for field in ("draft", "math", "ShowToc", "searchHidden"):
            if field in meta and not isinstance(meta[field], bool):
                errors.append(f"{label}:1: {field}はtrue/falseで指定してください")
        for field in ("description", "summary"):
            if field in meta and not isinstance(meta[field], str):
                errors.append(f"{label}:1: {field}は文字列で指定してください")
        for field in ("tags", "categories"):
            value = meta.get(field, [])
            if not isinstance(value, list) or not all(isinstance(x, str) and x.strip() for x in value):
                errors.append(f"{label}:1: {field}は文字列の配列で指定してください")
        relative = path.relative_to(root / "content")
        article = relative.parts[0] in SECTIONS and path.name != "_index.md"
        published = article and meta.get("draft", False) is not True
        if article:
            parts = list(relative.parts[1:-1])
            if path.name != "index.md":
                parts.append(path.stem)
            if not all(SLUG.fullmatch(part) for part in parts):
                errors.append(f"{label}:1: 記事のパスは英小文字・数字・ハイフンで指定してください")
            if "date" not in meta:
                errors.append(f"{label}:1: 記事の公開日dateが必要です")
            if published and not str(meta.get("description", "")).strip():
                errors.append(f"{label}:1: 公開記事のdescriptionが空です")
            dates = {}
            for field in ("date", "lastmod"):
                if field in meta:
                    try:
                        dates[field] = as_datetime(meta[field], tz)
                    except ValueError:
                        errors.append(f"{label}:1: {field}の日付形式が不正です")
            if published and "date" in dates and "lastmod" in dates and dates["lastmod"] < dates["date"]:
                errors.append(f"{label}:1: lastmodがdateより前になっています")
        if path.name == "index.md" and path.with_name("_index.md").exists():
            errors.append(f"{label}:1: 同じフォルダにindex.mdと_index.mdは置けません")
        for line, message in body_errors(body, published):
            errors.append(f"{label}:{start + line - 1}: {message}")
    return errors


class Document(HTMLParser):
    def __init__(self, text: str):
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.links: list[tuple[str, int]] = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "a" and "name" in attrs:
            self.ids.add(attrs["name"])
        for field in ("href", "src"):
            if field in attrs and (field == "src" or tag in ("a", "link", "image", "use")):
                self.links.append((attrs[field], self.getpos()[0]))
        if "srcset" in attrs and not attrs["srcset"].startswith("data:"):
            for item in attrs["srcset"].split(","):
                if item.strip():
                    self.links.append((item.strip().split()[0], self.getpos()[0]))

    handle_startendtag = handle_starttag


def link_errors(site: Path, base_url: str) -> tuple[list[str], int]:
    errors = []
    count = 0
    site = site.resolve()
    base_url = base_url.rstrip("/") + "/"
    base = urlsplit(base_url)
    if base.scheme not in ("http", "https") or not base.netloc:
        raise ValueError("baseURLはhttp(s)の絶対URLにしてください")
    pages = sorted(site.rglob("*.html"))
    if not (site / "index.html").is_file() or not pages:
        return ["生成先にindex.htmlがありません"], 0
    documents = {p: Document(p.read_text(encoding="utf-8")) for p in pages}
    for page, document in list(documents.items()):
        page_url = urljoin(base_url, page.relative_to(site).as_posix())
        for raw, line in document.links:
            if not raw:
                continue
            original = urlsplit(raw)
            if original.scheme and original.scheme not in ("http", "https"):
                if original.scheme == "javascript":
                    errors.append(f"{page.relative_to(site)}:{line}: javascript:リンクは使用できません")
                continue
            url = urlsplit(urljoin(page_url, raw))
            if url.netloc != base.netloc:
                continue
            url_path = unquote(url.path)
            prefix = unquote(base.path)
            if url_path == prefix.rstrip("/"):
                url_path += "/"
            if not url_path.startswith(prefix):
                if original.netloc:  # 同ホスト上の別サイトへの絶対URLは外部リンク扱い。
                    continue
                errors.append(f"{page.relative_to(site)}:{line}: baseURLのパス外へのリンク: {raw}")
                continue
            count += 1
            target = (site / url_path[len(prefix):]).resolve()
            if not target.is_relative_to(site):
                errors.append(f"{page.relative_to(site)}:{line}: 生成先の外への参照: {raw}")
                continue
            if target.is_dir():
                target /= "index.html"
            if not target.is_file():
                errors.append(f"{page.relative_to(site)}:{line}: リンク・画像の参照先がありません: {raw}")
                continue
            fragment = unquote(url.fragment).split(":~:", 1)[0]
            if fragment and target.suffix in (".html", ".svg"):
                if target not in documents:
                    documents[target] = Document(target.read_text(encoding="utf-8"))
                if fragment not in documents[target].ids:
                    errors.append(f"{page.relative_to(site)}:{line}: 見出し・idがありません: {raw}")
    return errors, count


def new_post(root: Path, args) -> Path:
    if not SLUG.fullmatch(args.slug):
        raise ValueError("slugは英小文字・数字・ハイフンを使ってください（例: my-first-note）")
    if args.section != "articles" and args.topic:
        raise ValueError("--topicはArticlesでのみ使用できます")
    parts = [args.section, args.slug]
    folder = root / "content" / Path(*parts)
    if not folder.resolve().is_relative_to((root / "content").resolve()):
        raise ValueError("記事の作成先がcontentの外です")
    target = folder / "index.md"
    if target.exists() or folder.with_suffix(".md").exists() or (folder / "_index.md").exists():
        raise ValueError("同じURLの記事が既に存在します。上書きはしません")
    subprocess.run(["hugo", "new", "content", str(target.relative_to(root / "content"))], cwd=root, check=True)
    text = target.read_text(encoding="utf-8")
    values = {}
    if args.title:
        values["title"] = args.title
    if args.summary:
        values.update(description=args.summary, summary=args.summary)
    if args.tag:
        values["tags"] = args.tag
    if args.topic:
        values["categories"] = [TOPICS[args.topic]]
    for key, value in values.items():
        replacement = f"{key} = {json.dumps(value, ensure_ascii=False)}"
        text, changed = re.subn(rf"^{key}\s*=.*$", lambda _: replacement, text, count=1, flags=re.M)
        if not changed:
            raise ValueError(f"テンプレートに{key}がありません")
    target.write_text(text, encoding="utf-8")
    return target


def check(root: Path, args) -> int:
    config = tomllib.loads((root / "hugo.toml").read_text(encoding="utf-8"))
    errors = markdown_errors(root, config)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("Markdown・front matter: OK", flush=True)
    base_url = args.base_url or config["baseURL"]
    with tempfile.TemporaryDirectory(prefix="slower-check-") as directory:
        if args.site_dir:
            site = Path(args.site_dir).resolve()
        else:
            site = Path(directory)
            subprocess.run(["hugo", "--gc", "--minify", "--panicOnWarning", "--printPathWarnings",
                            "--environment", "production", "--baseURL", base_url, "--destination", str(site)],
                           cwd=root, check=True)
        errors, count = link_errors(site, base_url)
        if errors:
            print("\n".join(errors), file=sys.stderr)
            return 1
        print(f"内部リンク・画像・アンカー: OK（{count}参照）")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    create = commands.add_parser("new", help="Leaf Bundle形式の下書きを作成")
    create.add_argument("section", choices=SECTIONS)
    create.add_argument("slug")
    create.add_argument("--topic", choices=TOPICS)
    create.add_argument("--title")
    create.add_argument("--summary", help="descriptionとsummaryの初期値")
    create.add_argument("--tag", action="append", default=[])
    verify = commands.add_parser("check", help="Markdown・本番ビルド・内部リンクを確認")
    verify.add_argument("--site-dir", help="既存の生成先を検証する場合に指定（CI用）")
    verify.add_argument("--base-url", help="公開先URLを上書きする場合に指定")
    args = parser.parse_args()
    try:
        if args.command == "new":
            path = new_post(ROOT, args)
            print(f"下書きを作成しました: {path.relative_to(ROOT)}")
            return 0
        return check(ROOT, args)
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"エラー: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
