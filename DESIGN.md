# KATA UI — 設計書 v0.2

Flux / shadcn 水準のコンポーネントライブラリサイトを kata-ui.dev に育てるための設計。
ステータス： スタックは **A（Vanilla のみ）に決定（2026-11-01）**。サイト生成器（build.py）＋レジストリは稼働済み、本番 https://kata-ui.dev/ に反映済み。残る主要判断は §9 収益化の価格のみ（型は決めた）。

---

## 1. ポジショニング

- **何の店か**：UI コンポーネントの「コードの店」。プレビューで触って、コードをコピーして自分のプロジェクトに貼る。
- **配布モデルは shadcn 式**：npm のライブラリではなく「コピペして自分のものにする」。利用者のコードベースに部品が残るので、ロックインがなく、検索流入にも強い。
- **差別化**：
- Flux は Laravel / Livewire 専用、shadcn は React + Tailwind 専用。どちらもフレームワーク前提。
- KATA は **フレームワークなし（Vanilla HTML / CSS / JS）で完結**する部品集。「ビルドなしで、そのまま動く」が両者の空白地帯。
- Cue のような「見栄え・目利き」型とも違う。KATA は実務部品の網羅と正確さで取る。
- **言語**：英語ファースト（サイト・ドキュメント・コードコメント）。日本語版は将来の拡張。
- **名前**：KATA UI（kata-ui.dev 取得・接続済み）。「型」＝再利用できる形、の意。
- **日本性の扱い（2026-11-02 決定）**：思想と物語にだけ入れる。型の哲学（型＝マスターした形を完璧に反復する規律）、余白（ma）、引き算をブランドの原則として語る。部品の見た目には持ち込まない（ボタンは世界共通の顔）。表層の和風装飾（日の丸、縦書き、禅クリップアート等）は禁止。当初トップページに "WHY KATA" セクションとして実装したが、説明文の塊はトップに不要と判断し、ヒーローの一文（"cast from a single mold — kata, the Japanese discipline of the form"）に畳んだ。**見た目への和は一点だけ（2026-11-02 追加決定）**：ロゴマークの芯だけを朱色（#EB471F、判子の朱）にした。ヘッダーロゴと favicon が対象。部品・UI アクセント（ティール）には使わない。**見せ方の教訓（2026-11-02）**：初版は漢字の大きな表示＋ローマ字ラベル＋カードで「和風テーマ」になり、本人に「ダサい」と却下された。静かな版（通常の本文テキスト＋罫線なしの3列、漢字表示なし）が正解。思想は文章の内容でのみ語る。

## 2. スタック（決定済み）

- **部品：Vanilla のみ（案 A）**。需要が見えた部品だけ、将来 React 移植（案 C）へ広げる。
- **サイト生成：自作 build.py（静的生成）で開始済み**。レジストリ（§4）を正本に dist/ を生成し、Cloudflare Pages へ Direct Upload でデプロイ。
- Astro への移行は「部品 50 超え」「ブログ本格化」「生成速度や保守が痛くなった」時点ではじめて検討する。今は build.py で十分。
- **ホスティング：Cloudflare Pages**（kata-ui プロジェクト）。将来 Pro のダウンロード配信も Cloudflare（R2 + 署名付きリンク等）で完結させる想定。

## 3. サイト構成（IA）

```
/ ランディング（Now）
/components/ 部品カタログ：検索＋フィルタ（カテゴリ・タグ・JS要否・状態）（Now：一覧のみ → Next：検索/フィルタ）
/components/[slug]/ 部品詳細（§5 の型）（Now）
/docs/ ドキュメント（Next）
/docs/getting-started 導入（トークンの貼り方、ファイルの置き方）
/docs/theming トークンとテーマ上書きの作法
/docs/dark-mode ダークモードの仕組み
/docs/accessibility アクセシビリティ方針
/blocks/ 組み合わせ済みセクション集：料金表・ヒーロー・FAQ 等（Later、Pro の主在庫）
/templates/ 完成ページのテンプレート（Later、Pro）
/pricing 料金：Free / Pro の線引きと比較表（Next で骨格、販売開始時に有効化）
/changelog 更新履歴＋RSS（Next）
/blog/ 使い方記事（「フレームワークなしでモーダルを作る」等、検索流入のエンジン）（Next）
/search 検索結果（⌘K パレットが主導線、ページは受け皿）（Next）
/license /privacy 法務の最小ページ（Now：リンクだけでも置く）
```

機械向けの出口（ページではないが最初から設計に入れる）：

```
/sitemap.xml 生成器が自動出力（実装済み）
/registry.json レジストリ全体の機械可読インデックス（Next： §8 の配布基盤）
/components/[slug]/component.json 部品単位の機械可読定義（Next）
/llms.txt AI ツール向けのサイト要約（Cue が採用。Next）
/feed.xml changelog / blog の RSS（Next）
```

グローバル要素：

- ヘッダー：Logo / Components / Docs / Blocks / Pricing / Changelog ＋ ⌘K 検索 ＋ GitHub。モバイルではナビを畳む（実装済み：詳細ページはチップ列サイドバー）。
- 詳細ページのサイドバーはカテゴリツリー（デスクトップ）／横スクロールチップ（モバイル）（実装済み）。
- ⌘K コマンドパレットは自社製 Command 部品のドッグフーディングとして作る（Phase 2 の看板）。

## 4. コンポーネント・レジストリ（心臓部）

部品は「フォルダ＝正本」。サイト・コード表示・機械向け出口はすべてここから生成する（二重管理をしない）。

**部品制作の型は `KATA.md` を正とする**（フォルダ構成、meta 契約、色はトークンのみ、検品は `check.py`）。新規部品は `template/` フォルダを複写して作る。

```
components/
button/
meta.json 下記フィールド
preview.html 実演マークアップ（依存部品の CSS は /components/[dep]/[dep].css を link）
button.css トークン参照のみ、直値禁止
button.js 必要な場合のみ
```

meta.json の契約（v0.2 で拡張）：

- `title / category / description` — 表示と SEO の元
- `tags` — フィルタと関連部品の算出
- `status` — stable / beta（品質基準 §7 を満たすまで beta）
- `stage` — プレビューの並び（row / col）
- `usage / a11y` — 詳細ページの本文（a11y にはキーボード操作も含める）
- `keywords` — 検索クエリ想定語（例： "vanilla js modal", "css toggle switch"）（Next で追加）
- `since / updated` — changelog 自動生成の元（Next で追加）
- `pro` — true なら Pro 在庫（Phase 3 で使用、初期は全て false）

生成器が部品追加に連動して更新するもの：カタログ、詳細ページ、サイトマップ、registry.json、検索インデックス、changelog 下書き。

派生物（同じ正本から作る）：

- **単一ファイル版**：HTML + CSS + JS を1ファイルに畳んだ `single.html` を部品ごとに生成し、ダウンロード導線を置く（Next）。「1ファイルで動く」は KATA の約束事そのもの。
- **AI プロンプト版**：部品の仕様・コード・利用上の注意を AI ビルダーに貼れるプロンプト文に整形（Later、Cue 式配布）。

## 5. 部品詳細ページの型

1. パンくず＋見出し（部品名＋一行説明＋状態バッジ）
2. プレビュー：バリアントは部品内タブ、ステージには幅切替（Desktop / Mobile）とテーマ切替（Light / Dark）（実装済み）
3. 依存部品の注記（Uses: …）（実装済み）
4. コードタブ：HTML / CSS / JS（正本ファイルそのまま）＋コピー（実装済み）
5. 単一ファイル版のダウンロード（Next）
6. Usage（使いどころ・やってはいけないこと）
7. Accessibility（方針＋キーボード操作表）
8. 関連部品（タグ一致で自動選出）（Next）
9. Prev / Next（実装済み）

## 6. デザインシステム

- **デザインシステムとして正式化（2026-11-02）**：基盤の正本は `system/tokens.json`（色スケール zinc/asagi、タイポ、余白、角丸、高さ、モーション、エレベーション）。公開ページ /design-system/ を生成器が出力し、tokens.json もそのまま配布する。KATA.md §0「KATA の顔」が原則、tokens.json が実数、tokens.css が実行時ファイル。

- 部品は **tokens.css の `--k-*` 変数だけ**を参照する（サイト側 site.css の変数とは分離済み）。
- ダークは `[data-theme="dark"]` でトークンを差し替える方式（実装済み）。部品側に色の直書きを入れない。
- サイトの見た目（Flux 系の zinc + 黒ボタン）は部品の見た目と一致させる。サイト自体が最大のショーケース。

## 7. 品質基準（Stable の条件）

- キーボードで全操作ができる／フォーカスが見える／必要な aria が付いている
- ダークテーマで破綻しない／モバイル幅（360px〜）で横はみ出し・重なりがない
- **モバイル実幅チェックを公開前の必須ゲートにする**（2026-11-01 の iPhone 崩れの教訓：グリッドの min-width 未対策＋モバイル CSS の優先負け。デスクトップ確認だけで出さない）
- JS なしで成立する部品は JS なしで（Switch / Checkbox が手本）
- 例示データは架空のものだけ（実在のクライアント名・金額を公開物に入れない）

## 8. 配布戦略

- **Now**：サイトからのコピペ（コードタブ）が唯一の正規導線。
- **Next**：単一ファイル・ダウンロード＋ registry.json / component.json の機械可読出口＋ llms.txt。AI ツール・検索エンジンの両方から拾える形にする。
- **Later**：人気部品の React 移植を行った時点で、その移植版を **shadcn レジストリ形式**で公開する（beUI の型）。shadcn の CLI は React + Tailwind 前提であり、Vanilla 本体とは対象が噛み合わないため、本体には使わない（2026-11-01 判断）。
- **MCP サーバー**は Later の候補（Cue / beUI とも Pro 特典に採用）。registry.json ができていれば薄く実装できる。

## 9. 収益化（型は決定、価格は未決定）

Cue / beUI に共通する型を採用する：

- **Free**：単品部品は全て公開・MIT（コピペ自由、商用可）。スポンサー枠をカタログと詳細に小さく置く余地を残す。
- **Pro（買い切り Lifetime）**：在庫は「単品」ではなく **Blocks（組み合わせセクション）と Templates（完成ページ）＋上級部品**。サブスクにしない理由は Cue と同じ（コピーして終わる道具だから）。
- 価格帯の目安： **$129 起点（$129〜$199）**（2026-11-01 競合調査で改定：買い切りの標準帯は $129〜$299）。確定は販売開始時。
- 静的サイトでの販売の形：決済は Lemon Squeezy か Gumroad（ライセンスキー発行込み）、Pro 在庫はキーで開く非公開ダウンロード（Cloudflare 側で配信）。会員サイトは作らない。
- 受託（カスタム部品制作）は beUI 式に併設可能だが、現場仕事との兼ね合いで初期は置かない。

## 10. SEO ・成長

- 詳細ページが検索の着地点。「vanilla css [部品名]」「[部品名] without framework」のクエリを取りに行く（meta の keywords で管理）。
- ブログはチュートリアル型のみ（部品ページへの内部リンクを必ず張る）。
- GitHub に部品リポジトリを公開し、README からサイトへ送る（ffmpeg-skill と同じ流入の作り方）。
- ローンチ： 25 部品＋Docs が揃った時点で Product Hunt / Hacker News を1回打つ。それまでは静かに在庫を増やす。
- 計測： Cloudflare Web Analytics（軽量・無料）を入れる。凝った分析基盤は作らない。

## 11. 運用

- デプロイ： build.py → deploy.py（custom.cloudflare-pages）。プレビューは branch デプロイで確認してから main へ。
- 部品の版管理： meta の since / updated と changelog で追う。破壊的変更は部品名を変えず notes に明記。
- 作業の置き場： サイドチャット「KATA UI 開発」。設計の正本はこのファイル。

## 12. ロードマップ

- **Phase 1（完了）**：レジストリ化、生成サイト、ドメイン、モバイル対応。部品 10。
- **Phase 2**：部品 25（Select / Accordion / Tooltip / Pagination / Breadcrumbs / Alert / Skeleton / Spinner / Avatar / Separator / Textarea / Radio group / Progress / Command / Popover）。Docs 4本、検索＋⌘K、単一ファイル生成、registry.json、changelog、keywords/since 追加、Web Analytics。
- **Phase 3**：Blocks 10 種＋ Templates 2 種を Pro 在庫として制作、/pricing 有効化、決済とキー配信の実装、AI プロンプト版、llms.txt。
- **Phase 4**：需要のある部品から React 移植＋ shadcn レジストリ公開、MCP サーバー検討。

## 13. やらないこと

- フレームワーク版を先に作らない（React 移植は Phase 4 の需要ベース）
- 会員登録・コメント・いいね等のコミュニティ基盤を持たない（Pro 販売までは完全静的）
- 部品の見栄え競争（Awwwards 系）に寄せない。実務で正確に動くことが商品
- マーケットプレイス化（第三者の出品を受け付ける店）にしない。在庫と運営の事業になり、本来の「自分の部品を売る店」から変質するため（2026-11-01 調査結論）

---

## 付録： 参考・競合メモ

### Cue — https://www.cuedesign.space/ （2026-11-01 梶山さん共有）
- Awwwards 級サイトから手で選んだ「ベストなコンポーネント」のキュレーションライブラリ。自称 "taste layer"。
- 配布形態が独特： 部品ごとに **AI プロンプト**（Bolt / v0 / Cursor / Claude 等に貼る用）を売る。React ソースと MCP サーバーは展開中。
- 価格： Free（閲覧＋プロンプトコピー 24h 2回まで）／ Cue+ Lifetime **$129 買い切り**（founding 50名限定、以後 $249）。サブスクにしない理由は「コピーして終わる道具だから」。
- 姿勢： "Taste over volume" — グリッドを埋めるための量産を否定し、キュレーションの目利きが差別化。
- KATA への示唆： (1) 収益化は買い切り Lifetime も有力な型（§9 に採用）。(2) コードだけでなく「AI に貼るプロンプト」を配布形態に加える余地がある（§4 派生物）。(3) Cue が "見栄え・目利き" 側なので、KATA の「実務部品・Vanilla で完結」とは正面競合せず棲み分け可能。

### beUI — https://beui.dev/ （2026-11-01 梶山さん共有）
- React / Next.js / React Native 向けの「アニメーションするコンポーネント」集。Motion（Framer Motion）+ Tailwind 製。
- 配布は **shadcn レジストリ経由**（`bunx shadcn add @beui/...` の1コマンド導入）。コピペ元コードも公開。
- 収益モデル： 本体は **Free & MIT オープンソース**（スポンサー表示あり）／ **beUI Pro** は 350+ のプレミアムブロック＋テンプレート＋アニメーションイラストを **Lifetime 買い切り**、非公開レジストリ、MCP アクセス、Agent Skill 付き。受託制作（Work with me）も併設。
- KATA への示唆： (1)「無料コア → Pro 買い切り」の型は Cue と beUI で共通する有力パターン（§9 に採用）。(2) 導入は「1コマンド」が現代の標準体験 — Vanilla では単一ファイル・ダウンロードと registry.json で代替する（§8）。(3) Pro 特典に **MCP / Agent Skill** を入れるのも両者に共通。AI ツール経由の配布が新しい接点になっている。

## 14. 競合調査の反映（2026-11-01、research/00-synthesis.md）

33 サイトの実物調査を受けた決定：

- 詳細ページ型に「仕様表（クラス・状態・使用トークン）」「When to use / When not to use」「Anatomy（JS を伴う部品）」を追加する（HeroUI / Ark / Ant の型）。
- JS 部品のプレビューには、デモの前に発火条件・操作方法を明示する（Skiper / Animata の型）。プレビューのツールバー（幅・ダーク・コード・コピー）は全バリアントで統一する（Meraki の型）。
- llms.txt / registry.json を Phase 2 の前半に前倒しする（Mantine / Preline / Flowbite の AI 配布が標準装備化しているため）。MCP は Phase 3 候補のまま。
- Pro 価格の目安を $129 起点に改定（§9 に反映済み）。
- カタログのフィルタ軸に KATA 独自の構造ラベル（No JS / Single file / Dark ready）を採用する（Webflow の構造ラベル方式を KATA 流に）。
- トップページは文章でなく実物の UI の実演密度で見せる（shadcn / HeroUI の型）。Phase 2 のトップ改修項目とする。

### ReactDrops — https://reactdrops.dev/ （2026-11-01 梶山さん共有）
- React コンポーネント＋アニメーション＋エフェクトの「ドロップ（小出しリリース）」型ストア。毎週新作を足す運営リズムが売り。
- 訴求は「Every page looks like AI slop nowadays」— AI 生成っぽい没個性への反動を正面に置き、"stand out（目立つ）" を価値にしている。Cue の taste 路線に近いが、言葉はもっと攻撃的で分かりやすい。
- 「A head start for your AI」— AI に渡す前提の下ごしらえも訴求に含む。
- KATA への示唆： (1) 週次ドロップという更新リズムは changelog／新着の見せ方として借りられる。(2) 「AI slop ではない」の言い方は強いが、KATA は実務・正確さ側なので、対抗軸は「量産された無個性」vs「素のコードで自分のものになる」の言い換えが合う。

#### Cue 追記（2026-11-02 本人メモ依頼で再確認）
- 自称 "the taste layer on top of the tools people already use" — ホスティングもAIモデルも持たず、キュレーションとプロンプトだけを売る割り切り。
- 配布：AI プロンプトが現行の主力。React ソースと **MCP サーバー**（Cursor / Claude Desktop から直接参照）は "actively rolling out"。
- 機械可読ページ /llms.txt と /llms-full.txt を公式に用意（AI に読ませる前提のサイト構成）。KATA の Phase 2 計画（llms.txt / registry.json）と同方向。
- Cue+ Founding Lifetime $129 は **50名限定**、売り切れ後に $249。希少性で初期価格を正当化する型。


## Shared shape and elevation migration

The approved migration keeps `system/tokens.json` as the canonical foundation
source. `tools/sync_shape_tokens.py` generates marked radius/elevation regions in
`tokens.css`; `build.py` runs that adapter and renders/publishes the same JSON on
`/design-system/`. Run `python3 -m tools.sync_shape_tokens --check` to detect drift.
Component files consume the shared variables. No component namespace is added to
the global token file.

At the 8px base, xs/sm/md/lg/xl are 3/6/8/12/16px. Their coefficients are
.375/.75/1/1.5/2. Foundry controls only `--k-radius`, including persisted zero.
Full is explicitly fixed at 999px; circular 50% geometry and Lab geometry remain
fixed. This replaces the previous independent 6px/12px scale entries and the
99px full default while retaining every existing token name.

Elevation uses xs/sm/pop/modal, with a preserved overlay alias to pop. Defaults
come from the most frequent matching existing shadow geometries; dark variants
use stronger black opacity without changing the four geometries. Inset and line
rings preserve separate decorative roles. Backdrops mix a zinc palette token
with transparency and have a darker dark-mode recipe.

Intentional drift resolved: static radius values now derive from the base;
Foundry no longer rounds/overrides sm and lg; the previous overlay geometry is
normalized to pop. These are approved visual changes, not checker exceptions.
The audit rules are unchanged. Artistic Lab geometry, duration and easing are
outside this migration. Only the four named UI backdrops change independent
paint declarations; colors within normalized shadows follow the shadow scale.


### Shared text-contrast roles

Shared JSON owns text/surface roles. Muted text uses #71717a in light and #90909a
in dark. Danger text uses danger-ink; strong danger surfaces use white on-color.
Accent foreground uses accent-ink; full accent surfaces use adaptive on-accent.
Foundry and exported themes share WCAG luminance-based role math. Core vermilion,
dark canvas and default accent hue are unchanged. Measurements and limits:
docs/review/text-contrast/README.md. Mold checks remain independent of this
browser-based preview measurement; do not claim complete WCAG conformance.
