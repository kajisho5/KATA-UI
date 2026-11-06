# トップページの文章を半分にする 詳細設計書（案）

作成：2026-11-06　対象：kajisho5/KATA-UI　状態：**確認待ち**

## 1. 何を作るか（要件）

ROADMAP Phase 2 の項目「Reduce home-page prose to half the Phase 2 baseline recorded below」を行います。

### 1-1. 数え方の変更（オーナー決定 2026-11-06）

- これまでの基準：ページ全体の単語数 815語。メニュー・左の部品一覧・テーマ編集パネルも数えていた。
- いまの実測：全体 851語。内訳は次のとおり。
  - 本文（`<main>` 相当：ヒーロー〜最後の節）：**369語**
  - 左の部品一覧：358語
  - テーマ編集パネル（Foundry）：71語
  - 上のメニュー：23語
  - フッター：20語
  - スマホ用メニュー：10語
- 共通部分だけで約480語あるので、本文を全部消しても407語以下になりません。
- そこで **本文だけを数え、369語 → 185語以下** を目標にします。オーナーがこの案を選びました。
- 数え方は今までと同じです。script と style の外にある文字を、空白で区切って数えます。
- ROADMAP の基準の欄に、数え方を変えた理由と新しい基準（本文369語）を英語で書き足します。

### 1-2. やらないこと

- 左の部品一覧、テーマ編集パネル、メニュー、フッターは変えません。
- 見た目の部品（色・余白・文字の大きさ）は変えません。今ある site.css の書き方を使います。
- 主張する数字（部品数・Mold Verified）は今までどおり、生成時に数えた値を出します。

## 2. 技術選定

既存の build.py（Python で HTML を作る）の文章を書き換えるだけです。新しい技術・ライブラリは使いません。あなたのルール「既存リポの技術は変えない」に従うため、比較表は作っていません。

## 3. 画面構成（変更後、上から順）

画像 `home-prose.svg` を参照してください。左が今、右が変更後です。

| # | 節 | 今の語数 | 変更後の文 | 変更後の語数 |
|---|---|---:|---|---:|
| 1 | ヒーロー | 69 | 部品数の行（今と同じ）／見出し（今と同じ）／「Copy the files into your project. No framework, no build step.」／ボタン2つ／「MIT · Mold Verified 164 / 164 · Results」 | 47 |
| 2 | One mold | 27 | 見出し「One mold: shared tokens」／「Load tokens.css, then a component. Change a token; every part follows.」 | 16 |
| 3 | 最初の5部品 | 約130 | 見出し「Five to start」／カード5枚は「部品名＋状態バッジ」だけにする。説明文とタグは消す。カードは今までどおり各部品ページへのリンク | 13 |
| 4 | インストール | 23 | 見出し「Install」／コマンド2行（今と同じ）／「Or copy from any component page.」 | 14 |
| 5 | テンプレート | 25 | 見出し「Templates」／「Try a dashboard, inbox or settings page.」 | 8 |
| 6 | AI と使える環境 | 約50 | 見出し「AI tools」／「The registry, MCP server and AI skill serve the files you copy here.」／「Works with any HTML stack; React needs a few markup changes.」 | 26 |
| 7 | Pro | 22 | 見出し「Components are free. Pro adds layouts.」／「21 blocks, 7 templates, $129 once. Not on sale yet.」／リンク「Pricing」 | 17 |
| 8 | Lab とショーケース | 26 | 2つの節を1行にまとめる：「More: Lab · Showcase · Report a problem」 | 8 |
| | **合計** | **369** | | **約149** |

- 消す文の中身は、ほかのページにも書いてあります。
  - 部品の説明は各部品ページにあります。
  - 対応する環境の一覧はドキュメントの Installation にあります。
  - 「Check results and Beta labels…」の内容は、ヒーローの数字とリンクで代わりにします。
- 「12, 26 などの数」は、実装後に実際に数え直して PR に書きます。上の数は案の段階の数え方です。

## 4. 部品の分け方

- 直すのは `build.py` の、トップページの本文を作る部分だけです。
- カードは、今の説明文とタグの行を出さないようにします。カードの枠・リンク・バッジは今のものを使います。
- 8番の1行は、今ある `lpsec` の節の形を使います。

## 5. 状態管理

文章だけの変更なので、新しい状態はありません。

## 6. データ構造

- 部品数・バッジ・Mold Verified の数字は、今と同じく meta.json と check.py の結果から作ります。
- 単語数の測り方を、`tools/` の小さなスクリプトかテストにします。CI で「本文が185語以下」を毎回確かめ、増えたら落ちるようにします。

## 7. フォルダ構成（増えるもの・変わるもの）

```
build.py                         ← トップページ本文の文章
tests/test_home_prose.py         ← 本文の語数が185語以下かを確かめる（新規）
docs/ROADMAP.md                  ← 数え方の変更と結果、チェック
docs/HANDOFF.md                  ← 状態の更新
docs/design/home-prose.md        ← この設計書
docs/design/home-prose.svg       ← 画面のデザイン
```

## 8. 確かめること（実装後）

- 本文の語数（前 369 → 後 ○○）
- ライト・ダークの前後スクリーンショット（幅1280px と 390px）
- 既存のテストがすべて通ること（ホームの Stable/Beta 表示のテストを含む）

## 9. 確かめられないこと

- 文を減らしたことで、初めて来た人に伝わりやすくなったかどうか（利用者の調査はしていません）
- スクリーンリーダー、Safari、Firefox、実機での見え方
