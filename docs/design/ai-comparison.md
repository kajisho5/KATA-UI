# 10画面の比較ページ 詳細設計書（案）

作成：2026-11-07　対象：kajisho5/KATA-UI　状態：**確認待ち**

## 1. 何を作るか（要件）

ROADMAP Phase 2 の項目「Publish a ten-screen comparison: a direct AI draft and the same screen assembled from fetched KATA sources. Publish the prompts and method.」を作ります。

- よくある画面を10種類えらびます。
- 1つの画面ごとに、AI に2通りで作らせます。
  - **A：そのまま**：指示文だけを渡して、AI に1枚の HTML を書かせる。
  - **B：KATA を使う**：同じ指示文に「KATA の registry から部品を取ってきて組み立てる」を足す。
- 2つを同じ物差しで測って、数字と画面の写真を並べたページを公開します。
- 指示文・手順・AI が出した HTML（手直しなし）も、すべて公開します。

### 1-1. 10画面（既存のブロック・テンプレートと重なるものを選ぶ）

| # | 画面 | B で主に使う KATA の部品 |
|---|---|---|
| 1 | ログイン | Login ブロック、Field、Input、Button |
| 2 | 新規登録フォーム | Field、Input、Select、Checkbox、Button |
| 3 | 設定画面 | Settings ブロック、Switch、Select、Toast |
| 4 | 料金表 | Pricing ブロック、Badge、Button |
| 5 | ダッシュボード | Stat Cards、Line Chart、Table |
| 6 | データ表（並べ替え・絞り込み） | Data Table、Filter Toolbar、Pagination |
| 7 | 購入手続き | Checkout テンプレート、Field、Radio |
| 8 | 受信箱 | Inbox テンプレート、List、Badge |
| 9 | 空の状態＋はじめの案内 | Empty State、Button |
| 10 | 確認ダイアログ付きの削除 | Alert Dialog、Button、Toast |

### 1-2. 測るもの（数字で比べる）

既存のツールを使い、A と B に同じ測り方を当てます。

| 項目 | 測り方 |
|---|---|
| フォーカスが見えない場所の数 | `tools/verify_focus_ring` と同じ判定（Tab で止まる場所ごと） |
| 名前のない入力欄・ボタンの数 | ブラウザのアクセシビリティ情報で、名前が空のもの |
| type のない button の数 | HTML を読んで数える |
| 文字の色の濃さが 4.5:1 未満の数 | `tools/capture_text_contrast` と同じ計算 |
| 使っている色の種類・余白の種類の数 | CSS の値を数える（少ないほど揃っている） |
| ダーク表示・右から左（RTL）で崩れるか | Torture Test と同じ「はみ出し」判定 |
| コンソールのエラー数 | ブラウザで開いて数える |
| ファイルの大きさ | バイト数 |

「どちらが良いか」は書きません。数字と写真だけを出します（AGENTS.md の書き方の決まりに合わせます）。

### 1-3. ずるをしない決まり（手順として公開する）

- A も B も **1回目に出たものをそのまま使います**。やり直し・選び直し・手直しはしません。
- 両方とも同じ AI・同じ日に作ります。
  - AI の名前は「Claude（Anthropic）、Claude Code で実行」と書きます。
  - 細かい型番はリポに書かない決まりがあるので、書きません。
- 指示文は、画面ごとに1つだけ用意します。B は、その文の最後に決まった一文を足すだけにします。
- 測るスクリプトもリポに入れて、だれでも同じ数字を出せるようにします。

### 1-4. やらないこと

- KATA 以外のライブラリ（shadcn/ui など）との比較はしません（すでに vs-shadcn ページがあります）。
- 人による見た目の評価や点数づけはしません。

## 2. 技術選定

既存リポの技術をそのまま使います。あなたのルール「既存リポの技術は変えない」に従うためで、比較表は作っていません。

- ページの生成：build.py（Python）
- 計測と写真：Python と Playwright（Chromium）。どちらもこの環境に入っている版を使い、追加・更新はしません。

## 3. 画面構成

ページは `/compare/` の1枚です（画像 `ai-comparison.svg` を参照）。

1. **見出し**：「Ten screens, two ways」と、1行の説明
2. **手順の箱**
   - A と B の違い
   - 1回目をそのまま使うこと
   - AI の名前と作った日
   - 指示文と HTML へのリンク
3. **まとめの表**：10行 × 主な項目。A と B の数字を並べる。差がある数字だけを太字にする（色で良し悪しは付けない）
4. **画面ごとの節（10個）**
   - A と B の写真を左右に並べる（ライト）。スマホ幅では上下に並べる
   - その画面の数字の表
   - 指示文（開け閉めできる箱）
   - 「A の HTML」「B の HTML」へのリンク
5. **ページの下**：測り方の説明、確かめていないこと

部品はすべて KATA のものを使います（Table、Badge、Accordion、Tabs、Card）。

## 4. 部品の分け方

| ファイル | 役割 |
|---|---|
| `comparison/<画面>/prompt.md` | 指示文（A と B の文） |
| `comparison/<画面>/direct.html` | A の出力（手直しなし） |
| `comparison/<画面>/kata.html` | B の出力（手直しなし） |
| `tools/measure_comparison.py` | 1-2 の項目を測り、写真を撮り、`results.json` を書く |
| `comparison/results.json` | 測った結果 |
| `build.py` | `/compare/` ページを results.json から作る |
| `tests/test_comparison.py` | 10画面すべてに prompt・2つの HTML・結果があるか。ページの数字が results.json と同じか |

## 5. 状態管理

- ページの動きは、開け閉めの箱（Accordion）と、写真の切り替え（Tabs：ライト／ダーク）だけです。
- どちらも KATA の部品の機能をそのまま使います。新しいスクリプトは書きません。

## 6. データ構造（results.json）

```json
{
  "generated": "2026-11-07",
  "agent": "Claude (Anthropic) via Claude Code",
  "screens": [
    {"slug": "login", "title": "Sign in",
     "direct": {"focusInvisible": 0, "unnamed": 0, "buttonNoType": 0, "lowContrast": 0,
                "colors": 0, "spacings": 0, "overflowDarkRtl": 0, "consoleErrors": 0, "bytes": 0},
     "kata":   {"...": "same keys"}}
  ]
}
```

## 7. フォルダ構成（増えるもの）

```
comparison/<10画面>/prompt.md, direct.html, kata.html
comparison/results.json
comparison/shots/<画面>-{direct,kata}-{light,dark}.png
tools/measure_comparison.py
tests/test_comparison.py
docs/design/ai-comparison.md, .svg
```

## 8. PR の分け方

1. この設計案（確認待ち）
2. 指示文10個と、A・B の出力20個（手直しなし）、計測スクリプト、results.json
3. `/compare/` ページ、テスト、ROADMAP・HANDOFF の更新

## 9. 確かめられないこと

- 別の AI や別の日に作ると、数字は変わります。1回分の記録として公開します。
- スクリーンリーダー、Safari、Firefox、実機での確認
- 見た目の好み（数字にしないので、比べていません）
