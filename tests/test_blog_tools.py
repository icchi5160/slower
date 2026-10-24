"""記事作成と、公開前に検出したい入力ミスの回帰テスト。標準ライブラリのみ。"""
import importlib.util
from pathlib import Path
import shutil
from types import SimpleNamespace
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('blog', ROOT / 'scripts/blog.py')
blog = importlib.util.module_from_spec(spec)
spec.loader.exec_module(blog)


class MarkdownTests(unittest.TestCase):
    def test_code_examples_are_not_template_or_image_errors(self):
        self.assertEqual(blog.body_errors('説明。\n\n````python\nTODO: example\n![](example.png)\n```\n````\n', True), [])

    def test_common_markdown_mistakes(self):
        for body, message in [('```python\nx = 1\n', 'フェンス'), ('##\n本文', '空の見出し'),
                              ('TODO: 記入\n', 'TODO'), ('![](image.png)', '代替テキスト'),
                              ('## 見出し\n\n---\n', '本文が空')]:
            with self.subTest(body=body):
                self.assertTrue(any(message in error for _, error in blog.body_errors(body, True)))
        self.assertEqual(blog.body_errors('TODO: 記入\n', False), [])
        self.assertEqual(blog.body_errors('本文と `![](example.png)`。', True), [])

    def test_frontmatter_and_publication_requirements(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            article = root / 'content/blog/test/index.md'
            article.parent.mkdir(parents=True)
            valid = '+++\ntitle = "記事"\ndate = "2026-10-24T09:00:00+09:00"\ndescription = "概要"\ndraft = false\n+++\n本文。\n'
            article.write_text(valid, encoding='utf-8')
            self.assertEqual(blog.markdown_errors(root, {}), [])
            cases = [(valid.replace('description = "概要"', 'description = ""'), 'description'),
                     (valid.replace('draft = false', 'draft = "false"'), 'true/false'),
                     (valid.replace('+++\n本文', 'tags = "Python"\n+++\n本文'), '配列'),
                     (valid.replace('+++\n本文', 'lastmod = "2020-01-01"\n+++\n本文'), 'lastmod'),
                     (valid.replace('date = "2026-10-24T09:00:00+09:00"', 'date = "bad"'), '日付形式'),
                     ('本文だけ', 'front matter'), ('+++\ntitle = [\n+++\n本文', 'content/blog/test/index.md')]
            for text, message in cases:
                with self.subTest(message=message):
                    article.write_text(text, encoding='utf-8')
                    self.assertTrue(any(message in error for error in blog.markdown_errors(root, {})))
            article.write_text(valid, encoding='utf-8')
            article.with_name('_index.md').write_text('+++\ntitle = "Section"\n+++\n', encoding='utf-8')
            self.assertTrue(any('同じフォルダ' in error for error in blog.markdown_errors(root, {})))


class LinkTests(unittest.TestCase):
    def test_relative_encoded_and_root_links(self):
        for prefix in ('/', '/slower/'):
            with self.subTest(prefix=prefix), tempfile.TemporaryDirectory() as directory:
                site = Path(directory)
                (site / 'post').mkdir()
                (site / 'image.webp').write_bytes(b'fixture')
                (site / 'index.html').write_text(f'<a href="{prefix}post/?q=1#%E8%A6%8B%E5%87%BA%E3%81%97">記事</a><img srcset="image.webp 1x, image.webp 2x"><a href="https://other.test/missing">外部</a>', encoding='utf-8')
                (site / 'post/index.html').write_text('<h2 id="見出し">見出し</h2><a href="../">Home</a><a href="#見出し:~:text=example">本文</a>', encoding='utf-8')
                errors, count = blog.link_errors(site, 'https://example.test' + prefix)
                self.assertEqual(errors, [])
                self.assertEqual(count, 5)

    def test_missing_files_anchors_and_project_prefix(self):
        with tempfile.TemporaryDirectory() as directory:
            site = Path(directory)
            (site / 'index.html').write_text('<a href="missing/">欠落</a><img src="bad.png"><a href="#absent">見出し</a><a href="/blog/">パス外</a>', encoding='utf-8')
            errors, _ = blog.link_errors(site, 'https://example.test/slower/')
            self.assertEqual(len(errors), 4)
            self.assertTrue(any('見出し・id' in error for error in errors))
            self.assertTrue(any('baseURL' in error for error in errors))


@unittest.skipUnless(shutil.which('hugo'), 'Hugoが必要です')
class NewPostTests(unittest.TestCase):
    def test_real_hugo_archetypes_and_overwrite_protection(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'hugo.toml').write_text('baseURL = "https://example.test/"\ntitle = "Test"\n', encoding='utf-8')
            shutil.copytree(ROOT / 'archetypes', root / 'archetypes')
            (root / 'content').mkdir()
            for section in blog.SECTIONS:
                args = SimpleNamespace(section=section, slug='first-post', topic='programming' if section == 'notes' else None,
                                       title='日本語の「記事」', summary='概要と "引用"', tag=['Python', '学習'])
                path = blog.new_post(root, args)
                meta, body, _ = blog.read_post(path)
                self.assertEqual(meta['title'], args.title)
                self.assertEqual(meta['description'], args.summary)
                self.assertEqual(meta['tags'], args.tag)
                self.assertTrue(meta['draft'])
                self.assertFalse(meta['math'])
                self.assertIn('TODO:', body)
                if section == 'notes':
                    self.assertEqual(meta['categories'], ['Programming'])
                original = path.read_bytes()
                with self.assertRaises(ValueError):
                    blog.new_post(root, args)
                self.assertEqual(path.read_bytes(), original)
            self.assertEqual(blog.markdown_errors(root, {}), [])
            # 下書きのままなら許容される未記入項目を、公開時には検出する。
            path.write_text(path.read_text().replace('draft = true', 'draft = false'), encoding='utf-8')
            self.assertTrue(any('TODO' in error for error in blog.markdown_errors(root, {})))

    def test_unsafe_names_and_invalid_topic_combination(self):
        for section, slug, topic in [('blog', '../escape', None), ('blog', 'UpperCase', None),
                                      ('notes', 'valid', None), ('blog', 'valid', 'programming')]:
            with self.subTest(slug=slug, section=section):
                with self.assertRaises(ValueError):
                    blog.new_post(ROOT, SimpleNamespace(section=section, slug=slug, topic=topic))


if __name__ == '__main__':
    unittest.main()
