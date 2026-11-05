# PR #3: non-CLI remainder after PR #26

Compared main `2c057fb48157fe5fa03ae3f58a892087ff044d4d` with PR #3 head
`ac16cad41ebca8bbfc4f104fa45172be11f5c940`. Intent is taken from the PR's own
base `7587527e36a2b326bd80fb1f93ec307ba1437825` → head diff, not from a reverse
diff that would undo later main changes. No UI, token or checker code is changed
in the CLI PR. The following Japanese titles/bodies can be pasted into issues.

## Issue 1

**タイトル案：Pricing と Landing の請求期間スイッチに名前を付ける（PR #3 残件）**

本文：

PR #3 のラベル追加は main に未反映。`data-billing` の checkbox は switch の装飾を囲む label 内にあるが、その label にテキストがなく、Monthly / Yearly は label の外にある。

| main の該当ファイル | #3 の該当コミット | 今の mold ルールで再導入してよいか |
|---|---|---|
| `blocks/pricing/preview.html` | [cd05f4b](https://github.com/kajisho5/KATA-UI/commit/cd05f4b) | はい。`aria-label="Switch billing period"` など、操作の意味が分かる名前を追加する。現行の button type・トークンを維持 |
| `templates/landing/preview.html` | [be1dd6e](https://github.com/kajisho5/KATA-UI/commit/be1dd6e) | はい。同じ請求期間トグルの名前を追加する。ブロックとテンプレート双方を確認 |

- [ ] Accessibility tree の名前と checked 状態を確認
- [ ] Tab / Space で月額・年額が変わることを確認
- [ ] build.py で配布サンプルを再生成。古いプレビュー全体をコピーしない

## Issue 2

**タイトル案：演出テキスト3部品の ARIA を直し、読み上げる原文を残す（PR #3 残件）**

本文：

main には paragraph に対する `aria-label` が残る。PR #3 の削除意図は有効だが、削除だけを移すと、`aria-hidden` にした演出用 span しか残らず原文が読み上げられなくなる。静的な読み上げ用原文と視覚演出を分けて作り直す。

| main の該当ファイル | #3 の該当コミット | 今の mold ルールで再導入してよいか |
|---|---|---|
| `components/bounce-letters/bounce-letters.js` | [992d38d](https://github.com/kajisho5/KATA-UI/commit/992d38d) | 意図のみ可。`aria-label` の単純削除は不可。元の全文を accessible text として残す |
| `components/text-reveal/text-reveal.js` | [4ecf116](https://github.com/kajisho5/KATA-UI/commit/4ecf116) | 同上。単語ごとの演出 span は hidden のままでも、原文を別に保持する |
| `components/scramble/preview.html` と `components/scramble/scramble.js` | [6277ca7](https://github.com/kajisho5/KATA-UI/commit/6277ca7) | 同上。スクランブル文字を読まず、`SEVENTH WELL` の原文を読めるようにする |

- [ ] unsupported aria-label を除き、原文を一度だけ読めるようにする
- [ ] 演出の完了前・完了後・再実行後の accessibility tree を確認
- [ ] 3配置・RTL・JS二重読み込み、reduced-motion、実スクリーンリーダーを確認
- [ ] CSS を加えるなら既存トークンを使用。古い CSS の raw color / duration を戻さない

`bounce-letters/preview.html` の [7982a20](https://github.com/kajisho5/KATA-UI/commit/7982a20) は最終的な base→head 差分では改行だけ。別の不具合として数えない。

## Issue 3

**タイトル案：サイト本文の薄い文字色と accent 文字を役割トークンへ揃える（PR #3 残件）**

本文：

部品トークンの改善は main に入ったが、サイト chrome の `--ink3:#a1a1aa` / `--acc:#33A6B8` と、文字色の `var(--acc)` は残る。面の accent は変えず、描画される文字だけを適切な役割へ分け、現行ページでコントラストを測る。

| main の該当ファイル | #3 の該当コミット | 今の mold ルールで再導入してよいか |
|---|---|---|
| `site.css` の `--ink3` / `--acc` とその文字用途 | [30fb53e](https://github.com/kajisho5/KATA-UI/commit/30fb53e), [d5fcc05](https://github.com/kajisho5/KATA-UI/commit/d5fcc05) | 役割の分離という意図は可。`#6b6b73` / `#206b79` の直接追加は不要。既存の `--k-ink-3` / `--k-accent-ink` 等で再設計。全体の accent 面を暗くしない |
| `build.py` の `.icstat b`, `.ab-grid .no`, `.ja-step .no`, `.ja-card .go`, `.sc-card .k` と template_detail の full-page demo リンク | [cd38cb2](https://github.com/kajisho5/KATA-UI/commit/cd38cb2) | はい、現在表示される文字用途に `var(--k-accent-ink)` を使う意図は現行ルールに合う。現行の本文・構造は維持 |

- [ ] 現行の catalog / icons / docs / 日本語ページ / template detail を light・dark で測る
- [ ] 背景色が固定された面とテーマで反転する面を区別する
- [ ] placeholder を含む本文は4.5:1以上。disabled は数値を残して別扱い
- [ ] Foundry の明暗カスタム accent で文字と面の役割が混ざらないことを確認

旧トップの長い FAQ / Pro / principles / showcase 本文を再導入する必要はない。現在の短いトップでは使われない `.scmeta` 等の旧セクションを、旧コピーごと復活させない。旧 `.showtile .livechip{color:#a1a1aa}` / `.castlive .cl-cap{color:#6b6b73}` の生の色も不要。将来その面を使う場合は、その時点の固定色／役割トークンで測り直す。

## Issue 4

**タイトル案：横スクロールするコード例をキーボードでも読めるようにする（PR #3 残件）**

本文：

| main の該当ファイル | #3 の該当コミット | 今の mold ルールで再導入してよいか |
|---|---|---|
| `build.py` の `.term` を生成する箇所（現在のトップの Install from your terminal を含む） | [6448868](https://github.com/kajisho5/KATA-UI/commit/6448868), [2086e62](https://github.com/kajisho5/KATA-UI/commit/2086e62) | 意図は可。現行の実表示のコード例へ `tabindex="0"` と名前を付け、focus-visible を保証する。旧3カードの本文の復活は不要 |
| `site.css` と `build.py` のコード表示スタイル | 同上 | 追加するフォーカス表示は既存 `--k-ring`。生の outline / shadow 値は戻さない |

- [ ] 360px、200%拡大、Tab・矢印キーで横に隠れたコードを読めること
- [ ] フォーカスリングが切れず、領域名が読まれること
- [ ] 不要な空の tab stop を増やさず、現在出力しているコード例を対象にする

## Issue 5

**タイトル案：サイト全体の Playwright・axe・横はみ出し回帰を既存 CI に追加する（PR #3 残件）**

本文：

main には部品の複数配置の Python Playwright 検証があるが、PR #3 の代表ページ10件／axe／360〜1440pxの横はみ出しの Node スイートはない。部品テストと役割が違うため、サイト単位の検証という意図は残す。

| main の該当ファイル | #3 の該当コミット | 今の mold ルールで再導入してよいか |
|---|---|---|
| `tests/`（`tests/browser/site.spec.mjs` は未存在） | [9221df6](https://github.com/kajisho5/KATA-UI/commit/9221df6), [620dfde](https://github.com/kajisho5/KATA-UI/commit/620dfde), [980be77](https://github.com/kajisho5/KATA-UI/commit/980be77) | はい。現在のルート・操作へ更新し、必須 UI が無くても成功する conditional skip を避ける。違反を除外して緑にしない |
| `.github/workflows/site-build.yml`, `.github/workflows/mold.yml`（旧 `.github/workflows/ci.yml` は未存在） | [64ffdcb](https://github.com/kajisho5/KATA-UI/commit/64ffdcb), [2c55265](https://github.com/kajisho5/KATA-UI/commit/2c55265) | 既存 CI に統合する。旧 CI 一式を並行導入するのは不要。ブラウザ依存を明示的に install する |
| `package.json` / `playwright.config.mjs`（mainには未存在）, `tools/dark-audit.js` | [aa56d77](https://github.com/kajisho5/KATA-UI/commit/aa56d77), [4fe3602](https://github.com/kajisho5/KATA-UI/commit/4fe3602), [8ecbf85](https://github.com/kajisho5/KATA-UI/commit/8ecbf85) | 再現可能な依存管理と localhost のみでの server 起動という意図は可。古い依存版や CLI テストの二重管理は不要 |

- [ ] 現行の representative pages / search / mobile navigation / keyboard / light・dark を検証
- [ ] 360, 390, 430, 768, 1024, 1440px の overflow を検証
- [ ] axe の未解決違反は失敗として報告し、順次 UI PR で直す

## Already replaced, unnecessary, or requiring no issue

| main の該当ファイル | #3 の該当コミット | 判定 |
|---|---|---|
| `blocks/faq/faq.css` | 8d0cce8 | `--k-accent-ink` が main に反映済み。不要 |
| `components/button/button.css` | abb9f80 | main は accent 面と `--k-on-accent` の役割分離を実装済み。旧 accent-ink 背景案は不要 |
| `components/jelly-buttons/jelly-buttons.css` | 309ce20 | 同上。旧 accent-ink 背景を再導入しない |
| `components/gravity-playground/gravity-playground.css` | e037e58, ac16cad | main の hot は `--k-on-accent`。固定 `--k-zinc-950` よりカスタム accent に追従する。不要 |
| `components/sparkles/preview.html` | 04179e0, 73bddbd, 0f3d8fd | 未反映だが不要。main の固定 zinc-950 面で副文7.763:1、本文19.895:1。本文は既に親の白を継承する。白の重複指定や副文を白へ変える必然性なし |
| `system/tokens.json`, `tokens.css` | 15428eb, 8d914f7, 97eba41, 120408e, 202daaa, 6fbcfe1 | 役割トークン改善は #20 以降の値で置換済み。旧 hex 値、JSON/CSS の不一致、mold ヘッダーの無い旧 tokens.css は不要 |
| `build.py` の viewport / audit集計, `README.md` | 6448868, 007eda7, 3ef9861 | zoom制限除去・JSON由来の件数はmainに実装済み。標準出力行を数える旧集計は不要 |
| `CHANGELOG.md` | d3ea00d | 当時の「upcoming」のCLI/CI計画は現在の実装・ROADMAPに置換。古い予定文の再追加は不要 |

The computed Sparkles colors and the ARIA DOM observations are recorded in
[ui-dom-probe.json](ui-dom-probe.json). This is a Chromium/DOM inspection, not a
screen-reader test or a complete fresh axe audit. The site-contrast issue above
requests measurements; it does not claim every candidate selector fails today.
