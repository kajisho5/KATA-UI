# KATA — 部品制作の型（The Mold）

KATA UI の全コンポーネントは、この「型」から鋳造する。新規部品も改修も、この型に合わないものは公開しない。
設計の正本は DESIGN.md、本書は「部品をどう作るか」の正本。雛形は `template/` フォルダ。検品は `check.py`。

---

## 0. KATA の顔（デザインの署名）

型から鋳造された部品は、並べたときに「KATA のものだ」と分かる顔を持つ。制作時はこの署名を守る。

- **色**： zinc ニュートラルが支配色。主役は #18181B の黒、白地、境界は影よりヘアライン。ティール（#0E9594 系）は「一点だけ」差す UI アクセント。色数を増やさない。唯一の例外：朱色（#EB471F、判子の朱）は「芯」にだけ使う。ロゴマークの右下の1/4と、部品のアクティブ状態の芯（スイッチのツマミの中心、ラジオの点）がそれで、2026-11-02 に KATA の視覚的署名として決定。トークン名は --k-core。面や文字には使わない。
- **形**： 角丸は共通の 3 / 6 / 8 / 12 / 16px 段階（基準 8px、Foundry 連動）。面で構成するタイル感。丸みで柔らかくしない。
- **質感**： フラット。影は浮かせるためでなく、境界と最小の奥行きのため（ring shadow が基本）。プレビューはドット地のステージ。
- **文字**： Inter。数字は等幅（Geist Mono）。字間と行間は「文字の型」（次節）で固定する。場当たりで決めない。
- **寸法**： 高さは 32 / 38 / 44 の3段。余白は4の倍数。部品同士の寸法を揃えることが「型」の見た目を作る。
- **動き**： 実用部品は速く、小さく（130〜220ms)。バウンスや大きな弾みは使わない。Motion ライン（2026-11-02 新設）は別枠で、滑らかさそのものが商品。ただし精密・機械的であること、派手な演出にしないことは共通の線引き。
- **声**： 英語コピーは短く断定する（"Parts you copy. Code you own."）。説明は1文で切る。煽らない。
- **記号**： ロゴは枠なしの4分割正方形（2026-11-02 本人決定、A1 Mold から変更）： 左上＝墨、右上＝市松の入れ子（正方形の中にまた正方形——型の中の型）、左下＝灰、右下＝朱。

### Shared motion roles and reduced-motion ownership

- `--k-ease`: entrance and general transitions (out-shaped).
- `--k-ease-in-out`: repositioning and exit transitions (slow start and slow finish).
- `--k-ease-spring`: weak overshoot.
- `--k-ease-bounce`: strong overshoot.

Under `prefers-reduced-motion: reduce`, tokens.css sets only `--k-mscale:0 !important`.
It must not apply universal animation, transition, or scroll overrides: copied KATA
styles must not disable motion owned by the host application. Scaled KATA state
transitions become zero-duration; spinner, skeleton, marquee and Lab loop components
stop their own animations (or hide the animated decoration) in component CSS.
Completion logic must still work with no end event. The misleading `--k-ease-out`
name is retained only as a deprecated alias of `--k-ease-in-out` for API compatibility;
all first-party consumers use the corrected name. This is a naming/scope correction,
not a static audit exception or a change to the four curve shapes.

The motion multiplier is `--k-mscale`, default 1. Every KATA duration must multiply
it. Discrete state transitions use `--k-dur-fast/base/slow` (130/180/220ms before
scaling). Continuous effects keep their original period as
`calc(<time> * var(--k-mscale))`. An end-event waiter must complete immediately
when computed duration is zero and have a duration/delay-based timeout fallback.
Reopening cancels obsolete listeners and timers.

## 0.5 文字の型（字間・行間は固定値）

- **入力欄はモバイルで 16px**：テキスト入力部品（Input / Textarea / Select / Tag Input / Command 等）は `@media (max-width:640px)` で font-size:16px にする。iOS Safari は 16px 未満の欄にフォーカスするとページを自動ズームし、戻らない — デザインではなくプラットフォームの型。

字間ゼロの本文や、和文の詰めは「当たり前」の欠品として扱う（2026-11-02、伝統色パレットの実例から成文化）。値は tokens.css の `--k-ls-*` / `--k-lh-*` と一致させる。

| 用途 | 字間 | 行間 |
|---|---|---|
| Display（30px〜） | -0.025em | 1.1 |
| 見出し（19〜24px） | -0.01〜-0.02em | 1.3 |
| カード見出し（14〜18px） | -0.01〜-0.015em | 1.35 |
| 本文（13.5〜15px） | +0.012em | 1.7（長文は 1.85） |
| 小文字（11〜12.5px） | +0.01em | 1.6 |
| ラベル（大文字） | +0.08〜+0.14em | — |
| マイクロラベル（〜12px・大文字） | +0.14〜+0.18em | — |
| 等幅データ | +0.02〜+0.03em | — |
| 和文・表示（漢字名など） | +0.05〜+0.08em | 1.3 |
| 和文・本文 | +0.04em | 1.85〜1.9 |
| 和文・小（かな読みなど） | +0.04〜+0.06em | — |

- 縦書きの字間は列の字送りとして別扱い（+0.3em 前後）。横書きの表は適用しない。

- 和文に負の字間は使わない。
- かな読み・ふりがなは分かちの単位で折り返す。語の途中で割らない（nowrap、または flex の単位にする）。
- 部品 CSS に字間を直書きする場合も、この表の値以外を使わない。


## 0.6 細部 — the details are the product

部品のCSSは「動けばいい」では出荷しない。各部品に最低限入れる細部の型（2026-11-02 梶山指示で明文化。今日の実例つき）:

- **動きは物理として正しく**: 振り子の向き・バネの戻り・重力の向きを実測で確かめる（Newton's Cradle は回転符号が逆で玉が列にめり込んでいた）。
- **ダークで変わる**: 色は意味トークン経由。canvas は周囲のテーマを読んで追随する（Wagara はスナップショット読みで Paper のまま固まっていた）。
- **タッチで動く**: pointer 系は touch-action を付け、指ドラッグで実測する（Magnet は「押せるだけ」だった）。
- **入力はモバイル16px**（§0.5 の入力ルール）: iOS の自動ズームは故障に見える。
- **余白のリズムは一律**: 見出しの上下など、同じ役割の間隔はブロック境界で変わらない。目分量でなく実測値で揃える。
- **状態を全部作る**: hover / active / focus-visible / disabled / 空・多すぎ・長すぎ の各状態と、その間の transition。キーボードのフォーカス環は tokens.css の床が保証するが、部品固有の見せ方が要る所は部品で作る。
- **光学補正**: アイコンと文字の中心、±1px の見えのズレは実寸スクリーンショットで詰める。拡大して見るのが標準手順。
- **prefers-reduced-motion**: tokens.css changes only --k-mscale; each component stops its own loops. Host application transitions must remain untouched.
- **フォーム部品は -webkit-appearance も併記**: iOS Safari は標準 appearance だけでは native の白い欄・青いラジオを手放さない。背景や枠を自前で描く input / select / checkbox / radio は `-webkit-appearance:none;appearance:none;` を必ず対で書く（2026-11-02、カタログのギャラリーで発覚）。
- **配布ファイルの URL は全て内容ハッシュ付き**: バンドル（kata-ui.css / kata-ui.js）も例外にしない。バージョンなしの URL は端末に古いコピーを固定する（2026-11-02、実機で発覚）。
- **カード（<a>）の中にプレビューを入れる時は内部リンクを span 化**: プレビュー内の <a> は HTML の入れ子禁止で外側のカードをパーサに壊される（カタログで10部品が空表示になった）。ギャラリーの stage は inert が前提なので、card() が自動で span 化し、build が残存を assert する。

## 1. フォルダの型

```
components/<slug>/
  meta.json        部品の素性（§2）
  preview.html     実演マークアップのみ（script 禁止、§5）
  <slug>.css       その部品の全スタイル（§3）
  <slug>.js        必要な場合のみ（§4）
```

- slug は英小文字＋ハイフン、部品名そのもの（button, data-table）。
- ファイルを増やさない。バリアントは別ファイルにせず、クラスで表す。

## 2. meta.json の型

必須： `title`（英）、`category`（Actions / Forms / Display / Feedback のいずれか）、`description`（英1文、60〜140字目安）、`tags`（2〜4個）、`status`（stable / beta）、`usage`、`a11y`。
任意： `stage`（preview の並び、row / col、既定 row）、`keywords`（検索クエリ想定語）、`since` / `updated`（YYYY-MM-DD）、`pro`（既定 false）。

- `usage`：使いどころ＋「やってはいけないこと」を1〜3文で。
- `a11y`：キーボード操作、フォーカス、aria の要点を具体的に。「対応しています」で済ませない。

## 3. CSS の型

- **色は tokens.css の `--k-*` 変数だけ**。16進数カラーの直書きは禁止（check.py が検出する）。
- Shared UI shadow/backdrop recipes come from system/tokens.json; raw neutral paint is not an exception. Lab shadow geometry follows the paint/provenance profile below. Propose missing shared roles in the canonical JSON, never directly in tokens.css.
- JS 内で色が要る場合も、トークンの値を写した定数1箇所に集約する（例： toast の --k-success）。
- クラス名は意味で付ける（.btn, .badge, .field）。バリアントは接尾辞（.btn-pri, .badge.asagi）、サイズは .btn-sm の形。状態は .on / .open / [disabled] 等、既存部品と揃える。
- ダークはトークンの差し替えで成立させる。部品側に [data-theme] の分岐を書かない。
- 寸法の物差し： 高さ 32 / 38 / 44、角丸 8（大物 12）、フォーカスリングは --k-ring。

## 4. JS の型

- 依存なし・import なし・単体で動く。フレームワーク前提の書き方をしない。
- Data attributes select instances. Generate collision-checked IDs for ARIA/label associations and preserve application IDs; samples must not carry fixed IDs. See implementation contract item 11.
- Esc で閉じる、フォーカスを戻す、といった後始末は部品の責任。
- JS がなくても「見た目と意味」が成立する部品は JS を置かない（Switch / Checkbox が手本）。

### Keyboard direction

Horizontal arrow keys follow the visual direction. In RTL, ArrowLeft moves forward.
ArrowUp/Down, Home/End and PageUp/Down keep their meanings. Numeric OTP sequences
stay explicitly LTR inside RTL pages.

## 5. preview.html の型

- 実演だけを書く。説明文や見出しは入れない（それは meta と生成器の仕事）。
- 代表バリアントを全部見せる。JS 部品は「どう触ると何が起きるか」が分かる初期状態にする（発火条件は詳細ページ側で明示する）。
- 他部品の CSS が要る場合は `<link rel="stylesheet" href="/components/<dep>/<dep>.css">` を末尾に置く（依存として自動表示される）。
- 色は currentColor かトークン参照。16進数の直書き禁止。
- 例示データは架空のものだけ（実在のクライアント名・担当者名・金額を入れない）。

## 6. 検品（check.py ＋ 目視）

自動（check.py、全項目必須）：

- 必須ファイルと meta の必須項目、category / status の値
- CSS / preview に色の直書きがないこと
- preview に script がないこと、JS に import がないこと

目視（公開前に必ず）：

- モバイル幅（360px 前後）で横はみ出し・重なりがない
- ダーク切替で破綻しない
- キーボードだけで全操作でき、フォーカスが見える
- バリアント切替・幅切替が詳細ページで機能する

`status: stable` は自動＋目視の全部を通った部品だけ。それ以外は beta で出す。

## 7. 部品の追加手順

1. `cp -r template components/<slug>` して、雛形の中身を置き換える
2. `python3 check.py <slug>` が OK になるまで直す
3. `python3 build.py` → プレビューブランチにデプロイして目視検品
4. Open a main-targeted PR with a changelog entry for owner review. The owner handles merge and release; the implementation agent does not deploy to main.

## アイコンの型

部品と同じく、アイコンも型から作る。無法地帯にしない。

- **グリッド**： viewBox は 24×24 固定。線画（stroke）で描き、塗りは持たない（例外は署名の芯のみ）。
- **線**： stroke-width は **1.7**（24 グリッド基準）。linecap は square、linejoin は bevel（2026-11-02 に round / 2 から変更 — シャープな線が KATA の型）。currentColor で描き、色は置かれた文脈が決める。
- **サイズ**： 表示は 12 / 14 / 16 / 20 / 24 の物差しだけ。それ以外の寸法で置かない。
- **置き場所**： 正本は `icons/<name>.svg`（単一ファイル）。プレビューやサイトに直書きする場合も、このファイルと同一の形・同一の stroke でなければならない（check.py が stroke-width を検品する）。
- **増やし方**： 幾何学で描けるものだけを採用し、フリーハンドの有機的な形は入れない。
- **KATA の顔**： 素材は3つの形だけ——円、45°の線、r2 の角。有機的なフリーハンド曲線は使わない。一部のアイコンは中心に **芯（塗りの点）** を持つ（target / radio / wifi / thermometer / blocks / component）。これは Switch と Radio を貫く署名で、置くのは意味の中心がある glyph だけ。乱用しない。
- **互換**： Lucide と同一規格（24/2/round）。KATA にないアイコンは Lucide から混ぜて使える、が公式の線引き。数を自前で追わない。

## Brand marks (exception)
`icons/brands/` holds third-party brand marks (social / AI services). They do NOT follow the three-shape mold — a mark keeps its owner's geometry — and they are provided for nominative use only (social links, sign-in, integration grids). Trademarks belong to their owners; never use a brand mark as part of KATA's own identity.

## Mold definition: checker profiles and token provenance

This section defines the current checker policy. It supersedes earlier blanket
statements about token-only geometry where they conflict with the profiles below.
A passing static check is not a browser or accessibility certification.

**A. Profiles.** A component whose `meta.category` is `Motion` or `KATAYABURI`
uses the `lab` profile. Every other component, block and template uses `ui`.
In `ui`, radius, duration (including delay), shadow, color and border values must
come from shared `tokens.css` tokens, except the primitives configured below.
In `lab`, color, duration and easing must come from those tokens. Shadow paint
must use shared tokens, while glow offsets, blur and spread remain effect geometry.
Lab radius, border geometry, dimensions and positions may use local literal geometry.
A raw border color still fails in Lab; permission for border geometry does not
permit arbitrary colors. UI easing is not a token-required kind under this policy.

**B. Local variables are not a bypass.** The checker follows local custom
properties, both `--k-*` and other `--*` names, from their use to the final value.
A local alias is valid for a token-required kind only when it reaches a shared
token, an arithmetic expression derived from shared tokens, or a configured
primitive. Moving `8px` into `--local-radius` does not make a UI radius valid.
A local override of a shared token name is checked before that shared definition.
Cycles, unresolved values without a valid fallback and unsupported value syntax
are findings, not silent passes. Raw fallbacks are checked too. The consuming
property and profile determine the value kind: the same local geometry may pass
as a Lab radius and fail as a UI radius.

**C. Spacing and type checks.** `spacing-values` covers gap (including row/column
gap), margin, padding and inset, including their logical longhands. `type-values`
covers font-size and line-height, including sizes/leading in font shorthands.
Font families and weights in a shorthand are outside the type-value check.
Since mold v5 (T3) both **fail** for `ui` parts and stay `warn` for `lab` parts,
where literal spacing is nonblocking migration advice and geometry is permitted.
Rationale: the v4 scales cover every UI value (4px spacing grid with 1px and 2px
steps; text steps plus 15px; the §0.5 leading table), and #39–#41 replaced 762
spacing values, 433 font sizes and 84 line heights in UI parts, so a raw value
in a UI part is now a regression, not legacy. The promotion was made at 0 UI
findings, so the pass count did not drop (164 / 164 before and after).
Grammar, not exceptions:
- A negated token, `calc(var(--k-space-2) * -1)`, is a token. `-1` is a number in
  CSS syntax; an earlier lexer read it as an identifier and reported it. A raw
  negative length (`-4px`) still fails.
- `env(safe-area-inset-top|right|bottom|left)` is device geometry (notch, home
  indicator) that no token can express; it is accepted in spacing only
  (`environment_spacing_variables`). Other `env()` names and raw fallbacks fail.
- Relative sizes that must follow the surrounding text use a shared em token
  (`--k-text-code`, inline code), not a raw `em` literal.
Fixtures: tests/mold/cases.json (UI raw spacing/type fail, Lab warns, negated
token, raw negative, safe-area with token and raw fallback, other `env()`).

**D. JavaScript errors.** `js-single-instance` and `js-global-bindings` are
errors. The existing detectors report hard-coded `document.querySelector` data
roots and top-level `const`/`let` bindings. Their lexical limitations must be
reported; they do not prove initialization, keyboard or IME correctness. Test
multiple instances and repeated loading in a browser as well.

**E. Namespace ownership.** Component token namespaces come only from the folder
slug and an optional string `meta.prefix`. Prefixes may be written as `short`,
`k-short` or `--k-short-`; they identify the same namespace. Do not infer ownership
from the first CSS class. In particular, Carousel Ring's `.k-ring` does not own
the shared danger focus token `--k-ring-danger`. Genuine component-specific global
namespaces still fail `shared-token-scope`.

**F. Configuration, not hidden exceptions.** Primitive allowances live in
`check.config.json`: zero, a 1px border width on the configured border properties,
100%, transparent, currentColor, inherit and the other explicitly listed keywords.
Grammar allowances for arithmetic, gradients, border styles, font weights and
Foundry's external numeric `--k-mscale` also live there. A border width exception
does not exempt its color. New exceptions need an explicit path, property, value
and reason; do not add blanket exemptions to reach a target score.

JSON includes each item's profile, per-kind findings and reasons, advisory
finding counts, and the exact pass/fail summary. Publish those measured results,
even when a stricter policy reduces the score. Keep checker changes separate from
component repairs so the effect of each is reviewable.


## Static audit precision — geometry, motion and focus evidence

These rules refine the profile contract above. They describe semantic categories,
not exceptions for individual components. `check.config.json` is the policy source;
`tests/mold/accuracy.json` contains passing and failing examples.

- **Radius:** `50%` is circular geometry and is allowed. Other UI radius literals
  remain errors. Pixel radii of at least 99px are reported as `radius-full` and
  must use the existing shared `--k-radius-full`. This subtype does not remove
  the Lab profile's geometry permission. A shared token remains the provenance
  terminal; raw local aliases do not become shared tokens.
- **Color:** `color-scheme` selects browser rendering behavior; it is not a paint
  color. `transparent`, `currentColor` and `inherit` are permitted primitives.
  Literal paint colors still fail.
- **Easing:** CSS standard timing keywords and `steps(...)` / `linear(...)` are
  language primitives. Custom `cubic-bezier(...)` curves require shared tokens
  where the profile checks easing. UI retains its existing required kinds;
  this revision does not add easing to UI's required kinds.
- **Border:** border width is geometry, not mold. Widths from 1px through 3px,
  including fractional widths, are allowed. Border paint is still checked
  independently, so `2px solid #fff` fails. Wider widths and other units still
  require tokens in the UI profile. Lab geometry remains allowed.
- **Duration:** a complete `calc(<time> * var(--k-mscale))` product, in either
  order, is controlled by Foundry's motion multiplier in both profiles. The time
  factor may resolve through local aliases, but cycles and unknown variables
  fail. An overridden local multiplier is not trusted. Merely mentioning the
  multiplier, adding an uncontrolled time, or multiplying by another variable
  does not establish control. This is a motion policy, not a general exemption
  for raw values inside `calc()`.
- **Inline data colors:** in `preview.html` and `examples.html` only, inline
  color-property declarations on elements carrying `data-swatch` or `aria-label`
  describe sample data. The exception applies to those declarations only. It
  does not excuse stylesheet paint, unmarked elements, SVG attributes, shadows,
  radius, duration or local-variable definitions. Label validity remains a
  separate accessible-name check. Legacy hex scanning uses the same boundary.
- **UI shadow:** hand-built zero-offset, zero-blur ring shadows with literal pixel
  spread are reported as `shadow-ring`, including local aliases. Use an existing
  shared `--k-ring` family token. Blurred elevation shadows remain `shadow` errors;
  neither subtype is an allowance.
- **Focus:** inspect own CSS, declared dependency CSS and `tokens.css` together.
  Read metadata dependencies, stylesheet links and the builder's `parts:` combo
  declarations, including transitive dependencies. Count missing evidence once
  per file, tag and normalized class set (or role); retain occurrence counts in
  JSON. Ancestor classes alone do not match the focused element.
  Since mold v3 (T2 step 4) a control passes in one of two ways:
  1. **Own ring.** A matching `:focus-visible` or `:focus` rule draws a ring
     (`box-shadow` other than none, or a visible outline / outline color). A
     focus rule that only removes the outline is not evidence. A host rule such
     as `.host:has(input:focus-visible) .grip{...}` counts when the host is an
     ancestor of the control.
  2. **Shared floor.** `tokens.css` has a zero-specificity floor that draws a
     2px `--k-ink` outline (`global_focus_outline_tokens`) or a `--k-ring`
     box-shadow (`global_focus_ring_tokens`), and no part rule that applies at
     rest or on focus removes the outline (`outline:none`/`0`,
     `outline-style:none`, `outline-width:0`) for that control.
  Rationale: the floor was measured. `tools/verify_focus_ring.py` renders every
  part in Chromium, walks its Tab stops in light and dark and counts pixels
  whose focused and blurred colors reach 3:1; it also reports rings cut by an
  overflow-clipping ancestor. Once the floor itself reached 3:1 (#34) and the
  part-owned weak and clipped rings were fixed (#35, #36), the measurement found
  0 weak, 0 invisible and 0 clipped stops among 437. Requiring each part to
  restate the floor added no evidence; detecting parts that cancel it does. The
  measurement runs in CI (`--check`), so the static rule is not the only gate.
  Fixtures: tests/mold/accuracy.json keeps the per-element cases with
  `no_focus_floor` and adds cancellation, replacement, `:focus`, hover-only and
  `:has()` cases. Static evidence still does not prove cascade order, contrast
  or clipping; only the browser measurement does, and it is Chromium only.


### Shared shape scale (approved value migration)

The 3/6/8/12/16px scale maps existing UI corner values to shared tokens; each
level follows the 8px base. The fixed 999px full token preserves pill intent.
Foundry changes the base only. Lab radius geometry remains outside this mapping.
Four semantic elevation levels and theme-aware backdrops replace repeated shadow
recipes. This is a foundation-value migration; no checker rule or allowlist is
changed to obtain a higher score. Canonical values live in system/tokens.json.


### Lab shadow paint versus glow geometry

Glow geometry is part of the effect; only its color must come from the mold.
For the Lab profile (Motion / KATAYABURI), box-shadow, text-shadow and filter
drop-shadow offsets, blur and spread are effect geometry. Shared --k-* paint
and token-only color-mix expressions are valid without normalizing that geometry
to UI elevation tiers. Raw rgba/hex/named paint still fails, including raw paint
inside mixes, local aliases, overrides and fallbacks. Existing configured
no-paint/inheritance primitives remain valid; unresolved/cyclic variables fail.
UI shadow geometry still requires shared shadow tokens. This profile distinction
restores artistic glows rather than exchanging the effect for a UI drop shadow;
it is not a component-specific score exception. tests/mold/lab-shadows.json covers
both accepted and rejected paint provenance for all three shadow properties.

Filter aliases that resolve to drop-shadow are inspected as shadows too; wrapping a raw paint value in a local filter variable must not bypass this rule.


See implementation contract item 6 for distinct selection, surface-offset and keyboard-focus rings.


## Approved implementation contract

These numbered decisions are the implementation target, not a claim that all
legacy parts meet them. Read docs/HANDOFF.md for measured status and discrepancies.
Existing profile and precision definitions above remain the checker policy; this
index does not add checks or exceptions.

1. **Source of truth.** system/tokens.json generates tokens.css through the build
   token synchronizer. Never hand-edit generated token CSS.
2. **Local versus shared values.** The namespace rule is defined in profile item E.
   Do not add --k-<slug>-* component tokens to the mold. Component-local custom
   properties belong on the root class in that component's own stylesheet;
   provenance still follows profile item B.
3. **Profiles.** Use the ui/lab split and required value kinds in profile item A
   above. Motion and KATAYABURI are Lab. The Lab shadow-paint section preserves
   glow geometry while requiring token paint. Do not reinterpret geometry as paint.
4. **Geometry.** Use the configured precision rules above: 1–3px border widths,
   circular 50% radii and layout percentages are primitives; pills reference
   --k-radius-full. An allowed width never excuses a raw border color.
5. **Shared scales.** The existing shape scale has --k-radius-xs/sm/md/lg/xl
   derived from --k-radius; full intentionally stays a fixed 999px pill token.
   Shared elevation roles are --k-shadow-xs/sm/pop/modal, plus --k-shadow-edge
   if present. Backdrops use --k-backdrop. A shared glow role is named --k-glow;
   it is not present in this checkout and must not be assumed to exist.
6. **Distinct rings.** --k-ring is keyboard focus only: since mold v3 a 2px
   page-colored gap plus a 2px ink ring (3:1 in both themes), matching the 2px
   ink focus-floor outline in tokens.css. --k-ring-selected is
   persistent selection; --k-ring-offset separates a ring from a colored surface.
   A selected item with focus must retain visible evidence of both states.
   Semantic ring colors resolve through the active theme and Foundry.
7. **Text and surfaces.** --k-danger is a surface; --k-danger-ink is text.
   --k-on-accent is text on accent and switches by accent luminance via relative
   color, with static ink fallback. --k-accent-ink is accent used as text.
   --k-on-color is white on fixed dark surfaces and strong danger surfaces.
   Text must measure at least 4.5:1 in both themes, including placeholder, hint,
   hover and active. Measure disabled text but apply its contrast exemption.
   This is an acceptance requirement, not a catalog-wide certification.
   Core vermilion #eb471f and dark canvas #18181b remain unchanged.
8. **Fixed palette.** Zinc-50/950, asagi, yamabuki and tsutsuji are fixed paint;
   they do not invert with the theme. Highlights on fixed-hue surfaces use fixed
   light tokens, not the inverting --k-bg pair.
9. **Motion.** Use the shared motion roles and reduced-motion ownership section
   above. The multiplier, discrete/loop timing, four curve meanings, scoped
   reduced motion and completion-fallback requirements are defined there.
10. **Mold compatibility.** tokens.css carries KATA mold vN and --k-mold. Parts
    declare requires mold >= N. The CLI must warn when selected parts require a
    newer mold and must not automatically replace existing tokens.css during add.
    An explicit owner-requested update follows /docs/update-mold/. This CLI
    implementation is pending PR #25 on the current main; do not claim it ships.
11. **JS parts.** Combobox supplies the initialization reference: IIFE;
    querySelectorAll for every instance; data-kata-ready; preserved existing IDs,
    otherwise collision-checked generated IDs. Samples have no fixed id/for/
    aria-controls. Every text input guards isComposing, keyCode 229 and
    compositionstart/end; a composition-confirming Enter must not select/submit.
    Null relatedTarget never closes a part. Outside dismissal uses pointerdown;
    showModal parts do not close on focusout. Window blur dismisses transient
    menus only. An exit waits for the end event plus a duration/delay timeout,
    finishes immediately at zero duration, and cancels stale work on reopen.
    Register document/window shortcuts, blur and resize once per part type,
    never once per instance. Prefer native change/input/toggle/close/cancel;
    otherwise dispatch kata-<slug>-<action> as a bubbling CustomEvent with detail
    and document a usage listener. Open/close/select/drag must work at multiplier
    zero and with reduced motion. Combobox itself still has gaps; it is not a
    blanket implementation or accessibility certificate.
12. **Keyboard.** Use the Keyboard direction section above, including the OTP
    LTR exception. Keep vertical/week/month/year key meanings unchanged.
13. **Dialogs.** Modal and Drawer close on Escape and backdrop click, trap focus
    while open and restore the opener on close. Alert Dialog never dismisses on
    backdrop click; native cancel/Escape closes it unless the application vetoes
    cancel. Start Alert Dialog focus on the least destructive action, then use
    the documented non-primary/dialog fallback.
14. **Samples.** Every button has an explicit type; every input/select has a
    label. Avoid inline presentation styles; compose Field and shared classes.
    A pasted sample must work twice on one page. Existing inline-data exceptions
    in the checker are not proof that a sample meets this stricter authoring rule.
15. **Accessibility metadata.** Describe only implemented behavior and identify
    real IME, screen-reader and browser/device checks still needed. Do not infer
    a full ARIA pattern from one passing static rule.
16. **Stable.** Require every static failure check to pass, plus a
    tests/<slug>-multi.html page (three instances, one RTL, script loaded twice,
    console clean), and manual IME/screen-reader evidence recorded in the PR.
    For non-text parts record why IME is inapplicable. Otherwise keep Beta and
    explain the missing evidence. Existing legacy Stable labels are not evidence
    that this release procedure has been completed.
