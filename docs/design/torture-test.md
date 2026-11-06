# Torture Test ページ 詳細設計書（案）

作成：2026-11-06　対象：kajisho5/KATA-UI　状態：**確認待ち（まだ作っていません）**

## 1. 何を作るか（要件）

ROADMAP Phase 1 の残り項目「Build one Torture Test page: three instances per component, RTL, dark mode, 200% zoom and keyboard-only operation」を作ります。

- 1枚のページに、Phase 1 の40部品を **3つずつ** 並べる（合計120個）。
- そのページを、次の **8通りの条件** で自動テストする。
  - 文字の向き：左から右（LTR）／右から左（RTL）
  - 色：ライト／ダーク
  - 拡大：100%（幅1280px）／200%（幅640px）
- それぞれの条件で、**キーボードだけ** で最初から最後まで移動する。
- 結果を表にして残し、CI（GitHub の自動チェック）で「前より悪くなっていないか」を毎回確かめる。

### 1-1. 対象の40部品（HANDOFF の順）

button, input, field, textarea, select, checkbox, radio, switch, modal, dropdown, popover, tooltip, toast, card, tabs, accordion, badge, alert, table, pagination, breadcrumbs, alert-dialog, drawer, combobox, date-picker, slider, toggle, segmented, avatar, progress, skeleton, spinner, empty-state, separator, sidebar, command, context-menu, hover-card, data-table, file-upload

### 1-2. 自動テストで調べること（各条件ごと）

| # | 項目 | 合格の条件 |
|---|---|---|
| A | エラー | ページのエラー・コンソールのエラーが0件 |
| B | 横はみ出し | ページ全体が横にスクロールしない（画面幅以内） |
| C | 部品のはみ出し | 各部品の枠から中身がはみ出さない |
| D | キーボード移動 | Tab キーでページの最後まで進める（途中で閉じ込められない） |
| E | フォーカスの見え方 | 止まった場所すべてで、フォーカスの枠が見える（既存の verify_focus_ring と同じ判定） |
| F | 3つの一致 | 同じ部品の1つ目・2つ目・3つ目で、Tab で止まる回数が同じ |

### 1-3. やらないこと（この PR の範囲外）

- 見つかった不具合の修正（部品ごとに別の PR で直します）
- ホームページの「Stable / Beta の数」表示（HANDOFF の次の項目。別 PR）
- スクリーンリーダー・Safari・Firefox・実機での確認（ここでは確かめられません）
- 公開サイト（kata-ui.dev）への掲載（必要なら別 PR で提案します）

## 2. 技術選定

既存リポの技術（Python の生成スクリプト＋素の HTML/CSS/JS、テストは Python＋Playwright）をそのまま使います。あなたのルール「既存リポの技術は変えない」に従うためで、比較表は作っていません。

| 使うもの | 版 | 根拠 |
|---|---|---|
| Python | 3.13.18（この環境で確認） | 既存の check.py・build.py と同じ |
| Playwright（Python） | 環境に入っている版をそのまま使う（追加・更新しない） | 既存の tests/test_*_browser.py と同じ |
| Chromium | 環境に入っている版 | 同上 |

新しいライブラリは足しません。依存の版も上げません。

## 3. 画面構成

1枚のページ `tests/torture.html` だけです（画像 `torture-test.svg` 参照）。

- **上部のツールバー**（画面上に固定）
  - タイトル「Torture Test」と「40 parts × 3」
  - 文字の向き：LTR / RTL の切り替え（KATA の Segmented 部品を使う）
  - 色：Light / Dark の切り替え（同じく Segmented）
  - 部品へ移動：40部品の選択メニュー（KATA の Select 部品）
  - 拡大の案内：「200% はブラウザの拡大（Ctrl/⌘ と +）で確かめる」
- **本文**：40部品を順番に1つずつ
  - 見出し行：番号（01〜40）、部品名、状態バッジ（Beta など、meta.json から）、部品ページへのリンク
  - その下に、点々模様の台（サイトのプレビューと同じ見た目）を3つ縦に並べる。台の左上に「1」「2」「3」の小さな札
- **スマホ幅（640px 以下）**：ツールバーが2段に折り返す。本文は同じ縦並び

縦に並べる理由：Sidebar（620px）や Data Table（560px）など横に広い部品があるため、3つを横に並べると狭い画面で崩れ、テストしたい「はみ出し」と区別できなくなるからです。

## 4. 部品の分け方

| ファイル | 役割 |
|---|---|
| `tools/build_torture.py` | 40部品の preview.html を読み、3つずつ並べた `tests/torture.html` を作る |
| `tests/torture.html` | 作られたページ（リポに入れる。手では書き換えない） |
| `tools/verify_torture.py` | 8条件 × 6項目を自動で調べ、結果を書き出す |
| `docs/review/torture/results.json` | 最新の結果（機械が読む用） |
| `docs/review/torture/README.md` | 結果の表（人が読む用） |
| `tests/test_torture_sync.py` | ページが生成スクリプトの出力と一致しているか（ブラウザ不要、毎回） |
| `tests/test_torture_browser.py` | CI で8条件を回し、results.json より悪くなっていないか確かめる |

### 4-1. 3つ並べるときの細工

- ラジオボタンの組の名前（kpay・cycle・density・range の4つ）に「-1」「-2」「-3」を付ける。付けないと3つが1つの組として動いてしまう。
- 各部品のスクリプトは1回だけ読み込む（全部品が「1回の読み込みで全部を初期化する」作りになっていることは T4 で確認済み）。
- CSS は部品ごとに1回だけ読み込む（41ファイル）。
- 3つの台にはそれぞれ名前を付ける（例：「Button 1」）。

## 5. 状態管理

- ツールバーの状態（向き・色）は **URL のうしろ** に書く（例：`?dir=rtl&theme=dark`）。
  - こうすると、テストはこの URL を開くだけで各条件を再現できる。
  - 読み込み時に `<html>` の `dir` と `data-theme` に反映する。
- ブラウザへの保存（localStorage）は使わない。
- ページの小さなスクリプトは、ほかの部品と同じ決まり（関数の中に閉じる、2回読んでも安全）で書く。

## 6. データ構造

### 6-1. 部品の一覧（`tools/build_torture.py` の中）

```python
PARTS = ["button", "input", ..., "file-upload"]   # 40個、HANDOFF の順
```

### 6-2. 結果（`results.json`）

```json
{
  "generated": "2026-11-06",
  "parts": 40,
  "conditions": ["ltr-light-100", "ltr-light-200", "...8個"],
  "summary": {"ltr-light-100": {"errors": 0, "page_overflow": 0, "tab_stops": 273, "fail": ["tabs:C"]}},
  "failures": [{"condition": "ltr-light-100", "part": "tabs", "check": "C", "detail": "content 10px wider than its stage"}]
}
```

CI は「今回の失敗」が「results.json に記録済みの失敗」の中に収まっていれば合格にします。新しい失敗が出たら不合格です。直した失敗は results.json から消すので、数は減る一方になります（今ある「ラチェット」と同じ考え方）。

## 7. フォルダ構成（増えるものだけ）

```
tools/build_torture.py
tools/verify_torture.py
tests/torture.html
tests/test_torture_sync.py
tests/test_torture_browser.py
docs/review/torture/README.md
docs/review/torture/results.json
docs/design/torture-test.md      ← この設計書
docs/design/torture-test.svg     ← 画面のデザイン
```

あわせて更新するもの：`.github/workflows/mold.yml`（ブラウザテストの行に1つ追加）、`docs/HANDOFF.md`、`docs/ROADMAP.md`。

## 8. 試作でわかったこと（事実）

捨てる前提の試作ページ（コミットしていません）を作り、2条件だけ試しました。

- 41個の CSS と18個のスクリプトを1枚にまとめても、エラーは出ませんでした（1件の「ファイルが見つからない」は調査中。アイコン画像の可能性が高いが未確認）。
- Tab で止まる場所は273か所で、どの部品も1つ目・2つ目・3つ目で数が同じでした。
- **Tabs がはみ出していました**（画面幅1280px でページが10px 横に広がる）。原因の候補は `.tabpane` の `width:100%` と内側の余白です（Input の #71 と同じ型。推測で、まだ確かめていません）。

本番の8条件では、ほかにも見つかる可能性があります。見つかったものは結果の表に載せ、修正は部品ごとの別 PR にします。

## 9. PR の分け方

1. **この PR**：ページ・生成スクリプト・自動テスト・結果の表（不具合は直さず記録だけ）
2. その後：見つかった不具合を部品ごとに1つずつ直す（直すたびに results.json の失敗が減る）
3. その後：ホームページに Stable / Beta の数を出す

## 10. 確かめられないこと

- スクリーンリーダー（VoiceOver、NVDA）
- Safari、Firefox
- 実機のスマホ・タッチ操作
- 本物のブラウザ拡大（テストでは「幅640px」で代わりにしています。WCAG の「200% 拡大で崩れない」の確かめ方として一般的な方法です）
- 実際の日本語入力
