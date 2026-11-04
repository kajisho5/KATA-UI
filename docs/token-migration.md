# Token migration plan

対象: `main` の `95d4c11a1402ea212b0e3db483358b237cbece79`。2026-11-03（日本時間）に集計。部品コード・tokens.css・検査器は変更しない、提案のみ。

## A–F適用後の検査結果（最新スナップショット）

この節が現行の検査結果。後半の20/164・433件・JS警告の記述は、PR #14で調査した**変更前の履歴資料**として維持する。今回は部品を修正せず、検査の根拠をKATA.mdへ追記してA–Fを実装した。

| 指標 | 修正前 | 修正後 |
|---|---:|---:|
|合格|20|21|
|不合格|144|143|
|対象|164|164|
|warnレコード数（対象×検査）|34|318|

合格数が増えたのはLabの幾何を許可するという決定Aによるもの。JSエラー化と参照追跡で新たな不合格も出ている。数字を合わせるallowlist追加や部品修正はない。

### 種類ごとの検査所見数

「所見」は検査のfindings数。「影響対象」はその検査がfail/warnになった対象数。token-valuesは今回から**宣言×値の種類**単位で、1宣言にduration/easingの両方があれば2件。参照経路の複数理由は同じ所見のreasonsへまとめる。旧433件（1宣言=1件）と単純な増減だけで比較しない。

|検査|修正後severity|修正前所見|修正後所見|修正後の影響対象|
|---|---|---:|---:|---:|
|accessible-label|fail|1|1|1|
|button-type|fail|0|0|0|
|focus-visible|fail|456|456|66|
|js-global-bindings|fail|57|57|18|
|js-single-instance|fail|24|24|16|
|legacy-contract|fail|0|0|0|
|reduced-motion|fail|0|0|0|
|shared-token-scope|fail|3|2|1|
|spacing-values|warn|0|892|161|
|token-values|fail|433|464|133|
|type-values|warn|0|638|157|
|variant-hover|fail|0|0|0|

JSの旧34レコード（24+57=81所見）はfailへ格上げ済み。新しい318 warnレコードはspacing/typeによるもの。`summary.findings`が実所見数、`summary.warnings`がwarnレコード数。

### token-valuesの値の種類 / profile別

|値の種類|ui所見|lab所見|合計|
|---|---:|---:|---:|
|radius|206|0|206|
|duration|51|57|108|
|shadow|39|10|49|
|border|36|0|36|
|color|20|15|35|
|easing|0|30|30|

|profile|対象|合格|不合格|
|---|---:|---:|---:|
|ui|121|12|109|
|lab|43|9|34|

### 合否が変わった対象

|対象|修正前→修正後|根拠|
|---|---|---|
|components/fireworks|不合格→合格|Labのradius/border幾何を許可（A）|
|components/goo-cursor|不合格→合格|Labのradius/border幾何を許可（A）|
|components/gravity-playground|不合格→合格|Labのradius/border幾何を許可（A）|
|components/horizontal-reel|不合格→合格|Labのradius/border幾何を許可（A）|
|components/kata-rain|不合格→合格|Labのradius/border幾何を許可（A）|
|components/meter|合格→不合格|token-values: components/meter/meter.css: background-image: linear-gradient(90deg,rgba(255,255,255,.5) 1px,transparent 1px) [color] — raw color: rgba(255,255,255,.5)|
|components/particle-net|不合格→合格|Labのradius/border幾何を許可（A）|
|components/popover|合格→不合格|js-single-instance: document.querySelector('[data-popover], js-global-bindings: const wrap|
|components/radar-chart|合格→不合格|token-values: components/radar-chart/radar-chart.css: border-radius: 50% [radius] — raw radius: 50%|
|components/result|合格→不合格|token-values: components/result/result.css: border-radius: 50% [radius] — raw radius: 50%|
|components/scatter-chart|合格→不合格|token-values: components/scatter-chart/scatter-chart.css: border-radius: 50% [radius] — raw radius: 50%|
|components/stacking-cards|不合格→合格|Labのradius/border幾何を許可（A）|
|components/table|合格→不合格|token-values: components/table/table.css: border-radius: 50% [radius] — raw radius: 50%|

### 失敗の組み合わせ（修正後）

|失敗した検査の組み合わせ|対象数|
|---|---:|
|token-values|71|
|focus-visible, token-values|46|
|なし（合格）|21|
|focus-visible, js-global-bindings, js-single-instance, token-values|8|
|focus-visible|7|
|js-global-bindings, js-single-instance, token-values|4|
|js-global-bindings, js-single-instance|2|
|focus-visible, js-global-bindings, token-values|2|
|accessible-label, focus-visible, js-global-bindings, js-single-instance, token-values|1|
|focus-visible, js-global-bindings, js-single-instance|1|
|focus-visible, shared-token-scope, token-values|1|

### 全対象ごとの失敗検査（修正後）

|対象|profile|合否|落ちた検査|spacing/typeのwarn所見数|
|---|---|---|---|---:|
|components/accordion|ui|不合格|token-values|7|
|components/accordion-gallery|lab|不合格|token-values|3|
|components/alert|ui|合格|なし|6|
|components/alert-dialog|ui|不合格|token-values, js-single-instance, js-global-bindings|7|
|components/aspect-ratio|ui|不合格|token-values|3|
|components/aurora|lab|不合格|token-values|5|
|components/avatar|ui|不合格|token-values, focus-visible|15|
|components/badge|ui|不合格|token-values|12|
|components/bar-chart|ui|不合格|token-values|10|
|components/beam-border|lab|不合格|token-values|8|
|components/blur-in|lab|不合格|token-values|4|
|components/bottom-navigation|ui|不合格|token-values, focus-visible|15|
|components/bounce-letters|lab|不合格|token-values|3|
|components/breadcrumbs|ui|不合格|focus-visible|3|
|components/burst-button|lab|不合格|token-values, focus-visible|6|
|components/button|ui|不合格|token-values, focus-visible|3|
|components/button-group|ui|合格|なし|3|
|components/calendar|ui|不合格|token-values, focus-visible|10|
|components/candlestick-chart|ui|合格|なし|6|
|components/card|ui|不合格|token-values, focus-visible|29|
|components/carousel|ui|不合格|token-values, focus-visible, js-single-instance, js-global-bindings|10|
|components/carousel-ring|lab|不合格|token-values|8|
|components/cascader|ui|不合格|token-values, focus-visible|7|
|components/checkbox|ui|不合格|token-values, focus-visible|7|
|components/chip|ui|不合格|token-values, focus-visible|4|
|components/collapsible|ui|不合格|token-values, focus-visible|6|
|components/color-picker|ui|不合格|token-values, focus-visible, js-single-instance, js-global-bindings|5|
|components/combobox|ui|合格|なし|4|
|components/command|ui|不合格|token-values, focus-visible, js-single-instance, js-global-bindings|13|
|components/comparison-slider|lab|不合格|token-values, focus-visible|5|
|components/confetti-cannon|lab|不合格|focus-visible|2|
|components/context-menu|ui|不合格|token-values, focus-visible, js-single-instance, js-global-bindings|8|
|components/converge|lab|不合格|token-values|4|
|components/copy-field|ui|不合格|token-values, focus-visible|7|
|components/counter|lab|合格|なし|10|
|components/data-table|ui|不合格|token-values, focus-visible, js-single-instance, js-global-bindings|12|
|components/date-picker|ui|不合格|token-values, accessible-label, focus-visible, js-single-instance, js-global-bindings|8|
|components/descriptions|ui|合格|なし|7|
|components/dock|lab|不合格|token-values|7|
|components/donut-chart|ui|不合格|token-values|10|
|components/drawer|ui|不合格|token-values, js-single-instance, js-global-bindings|7|
|components/dropdown|ui|不合格|token-values, focus-visible|7|
|components/dual-range|ui|不合格|token-values|2|
|components/empty-state|ui|不合格|token-values|7|
|components/field|ui|不合格|focus-visible|10|
|components/file-upload|ui|不合格|token-values, focus-visible, js-single-instance, js-global-bindings|10|
|components/fireworks|lab|合格|なし|1|
|components/follow-frame|lab|不合格|js-single-instance, js-global-bindings|4|
|components/funnel-chart|ui|不合格|token-values|7|
|components/gauge|ui|合格|なし|5|
|components/glass-panel|ui|不合格|token-values|9|
|components/glow-button|lab|不合格|token-values, focus-visible|10|
|components/glow-cards|lab|不合格|token-values|11|
|components/goo-cursor|lab|合格|なし|2|
|components/goo-tabs|lab|不合格|token-values, focus-visible|6|
|components/gravity-playground|lab|合格|なし|4|
|components/hanko|ui|不合格|token-values|13|
|components/heatmap|ui|不合格|token-values|8|
|components/horizontal-reel|lab|合格|なし|8|
|components/hover-card|ui|不合格|token-values, focus-visible|7|
|components/input|ui|不合格|token-values, focus-visible|13|
|components/input-group|ui|不合格|focus-visible|6|
|components/input-otp|ui|不合格|token-values, focus-visible, js-global-bindings|2|
|components/jelly-buttons|lab|不合格|token-values, focus-visible|6|
|components/kaleidoscope|lab|不合格|focus-visible|6|
|components/kata-rain|lab|合格|なし|1|
|components/kbd|ui|不合格|token-values|5|
|components/kintsugi-card|ui|不合格|token-values|10|
|components/line-chart|ui|合格|なし|6|
|components/liquid-button|lab|不合格|token-values|7|
|components/list|ui|不合格|token-values, focus-visible|6|
|components/magnet|lab|不合格|token-values|4|
|components/marquee|lab|不合格|token-values|14|
|components/menubar|ui|不合格|token-values, focus-visible|18|
|components/meteors|lab|不合格|token-values|5|
|components/meter|ui|不合格|token-values|9|
|components/modal|ui|不合格|token-values, focus-visible|9|
|components/navigation-menu|ui|不合格|token-values, focus-visible|13|
|components/newtons-cradle|lab|不合格|token-values|1|
|components/noren|ui|不合格|token-values|5|
|components/orbit|lab|不合格|token-values|4|
|components/pagination|ui|不合格|token-values, focus-visible|6|
|components/particle-net|lab|合格|なし|5|
|components/particle-word|lab|不合格|focus-visible|7|
|components/popover|ui|不合格|js-single-instance, js-global-bindings|7|
|components/progress|ui|不合格|token-values|5|
|components/qr-code|ui|不合格|token-values|16|
|components/radar-chart|ui|不合格|token-values|4|
|components/radio|ui|不合格|token-values|6|
|components/rating|ui|不合格|token-values|4|
|components/reorder|lab|不合格|focus-visible, js-single-instance, js-global-bindings|10|
|components/result|ui|不合格|token-values|8|
|components/scatter-chart|ui|不合格|token-values|6|
|components/scramble|lab|合格|なし|3|
|components/scroll-area|ui|不合格|token-values, focus-visible|5|
|components/scrollspy|ui|不合格|token-values, focus-visible|10|
|components/segmented|ui|不合格|token-values|5|
|components/select|ui|不合格|token-values, focus-visible|8|
|components/separator|ui|合格|なし|7|
|components/shine-text|lab|不合格|token-values|4|
|components/sidebar|ui|不合格|token-values, focus-visible|43|
|components/skeleton|ui|不合格|token-values|3|
|components/slider|ui|不合格|token-values|6|
|components/sparkles|lab|不合格|token-values|8|
|components/sparkline|ui|合格|なし|19|
|components/speed-dial|ui|不合格|token-values, focus-visible|6|
|components/spinner|ui|不合格|token-values|1|
|components/split-panel|ui|不合格|token-values, js-single-instance, js-global-bindings|9|
|components/spotlight|lab|不合格|token-values|14|
|components/stacking-cards|lab|合格|なし|10|
|components/stat|ui|合格|なし|8|
|components/stepper|ui|不合格|token-values|8|
|components/steps|ui|不合格|token-values|3|
|components/switch|ui|不合格|token-values|10|
|components/table|ui|不合格|token-values|6|
|components/tabs|ui|不合格|token-values, focus-visible|9|
|components/tag-input|ui|不合格|token-values, focus-visible, js-single-instance, js-global-bindings|4|
|components/tategaki|ui|不合格|token-values|11|
|components/text-reveal|lab|不合格|token-values|4|
|components/textarea|ui|不合格|token-values, focus-visible|7|
|components/tilt-card|lab|不合格|token-values|8|
|components/time-picker|ui|不合格|token-values, focus-visible|11|
|components/timeline|ui|不合格|token-values|6|
|components/toast|ui|不合格|shared-token-scope, token-values, focus-visible|10|
|components/toggle|ui|不合格|token-values|6|
|components/tooltip|ui|不合格|token-values|5|
|components/torn-ticket|ui|不合格|token-values|11|
|components/tour|ui|不合格|token-values|13|
|components/tracing-beam|lab|不合格|token-values|7|
|components/transfer|ui|不合格|token-values, focus-visible|14|
|components/tree|ui|不合格|token-values, focus-visible|5|
|components/typeset|ui|不合格|token-values, focus-visible|32|
|components/typewriter|lab|不合格|token-values|2|
|components/wagara|ui|不合格|token-values, focus-visible|17|
|components/warp-tunnel|lab|不合格|token-values|3|
|components/word-rotate|lab|不合格|token-values|3|
|blocks/app-shell|ui|不合格|token-values, focus-visible|21|
|blocks/cookie-consent|ui|不合格|token-values, focus-visible|6|
|blocks/cta-band|ui|不合格|token-values|5|
|blocks/faq|ui|不合格|focus-visible|7|
|blocks/filter-toolbar|ui|不合格|token-values|3|
|blocks/integrations|ui|不合格|token-values|10|
|blocks/invoice|ui|不合格|token-values|24|
|blocks/kanban|ui|不合格|token-values|16|
|blocks/login|ui|不合格|token-values, focus-visible|12|
|blocks/logo-cloud|ui|合格|なし|4|
|blocks/order-confirmation|ui|不合格|token-values|17|
|blocks/plan-compare|ui|不合格|token-values|3|
|blocks/pricing|ui|不合格|token-values, js-single-instance, js-global-bindings|19|
|blocks/roadmap|ui|不合格|token-values|12|
|blocks/settings|ui|不合格|token-values, focus-visible|17|
|blocks/site-footer|ui|不合格|token-values, focus-visible|20|
|blocks/site-header|ui|不合格|token-values, focus-visible, js-single-instance, js-global-bindings|10|
|blocks/stat-cards|ui|不合格|token-values|3|
|blocks/team|ui|不合格|token-values|8|
|blocks/testimonials|ui|合格|なし|9|
|blocks/use-cases|ui|不合格|token-values, focus-visible, js-global-bindings|20|
|templates/blog-article|ui|不合格|token-values, focus-visible|50|
|templates/checkout|ui|不合格|token-values|27|
|templates/dashboard|ui|不合格|token-values, focus-visible|27|
|templates/inbox|ui|不合格|token-values, focus-visible|39|
|templates/landing|ui|不合格|token-values, focus-visible|14|
|templates/product-page|ui|不合格|token-values, focus-visible|38|
|templates/settings-page|ui|不合格|token-values, focus-visible|31|

### 実装・検証の根拠

- `check.config.json`: ui/labの必須種類、Motion/KATAYABURI分類、0/100%/1px境界/transparent/currentColor/inherit等の許可値を管理。部品個別のallowlistは空。
- `tools/token_values.py`: 関数とvarを分解し、使用先の種類を保ってローカル定義を追う。shared-nameのローカル上書き、raw fallback、未解決参照、循環も検出。`calc`内の数値係数だけでは合格せず共有トークンへの到達を確認する。
- `tools/mold_rules.py`: メタデータからprofile、slug/meta.prefixからnamespaceを決める。先頭クラスを使わないためCarousel Ringの--k-ring-danger誤検知はなくなり、Toastの真の専用グローバル2所見は残る。
- spacing/typeは新しいwarn検査。Labのspacing警告は参考情報であり、geometryをfailにはしない。
- JSON schema_version=2。各対象にprofile、各値検査にdetails/by_kind、summaryにfindings/by_profileを追加。部品側のコードは未変更。
- `tests/mold/cases.json` に86個の陽性/陰性fixture。生値/alias/shared/calc、ui/lab、scope、JS severity、important、inline/embedded CSS等を標準unittestから検証する。

### 検出限界と次の判断

依存CSS・例HTML内を含むローカル変数の候補定義はすべて辿り、どれか1つが違反なら報告する。実際のselector/media/cascadeで使用される定義だけを確定する解析ではないため、条件付き定義では保守的な所見が出る可能性がある。未使用変数自体を名前から型推測してfailにするのではなく、検査対象propertyからの参照を追う。

値パーサーは標準ライブラリの字句/関数解析で、CSS仕様全体のvalidatorではない。未知の値構文は黙ってpassにせず所見にする。CSSの型としてそのトークンが正しいか、色contrast、実ブラウザーの計算済み値までは証明しない。JS検査は今回severity変更のみで、既存の字句的な検出限界は残る。部品修正・JS ASTへの移行・UI状態テストは別PRで行う。

後半の移行表にあるLab radius/border幾何の「旧違反」は決定Aで必須ではなくなった。色/time/shadow/easingの違反まで免除されたわけではない。将来の修正対象は、この節と最新mold-results.jsonを基準に選ぶ。

## 追加調査: 合否の組み合わせと検査の実効範囲

この節は最新main `95d4c11a1402ea212b0e3db483358b237cbece79` でcheck.pyを再実行した結果。下記の試算・検出実験はすべてリポジトリ外の一時ファイルで行い、部品・tokens.css・検査器は変更していない。既存の値別対応表は同じ433所見に対するものとして維持する。

### 失敗パターン（errorのみ。warningを含めない）

| パターン | UI | Lab | 合計 |
|---|---:|---:|---:|
|token-valuesのみ|46|31|77|
|focus-visibleのみ|5|0|5|
|両方のみ|50|9|59|
|その他|2|1|3|
|合格|18|2|20|
|合計|121|43|164|

「両方のみ」は2検査だけに失敗する対象。他の失敗も伴うものは「その他」へ入れる。以下の一覧はcomponentsだけでなく、check.pyの全対象であるblocks/templatesも含む。

#### token-valuesだけ直せば現行判定に合格する77対象

この「合格」は現在のwarning除外ルールでの試算。JS警告がある対象も注記する。token-valuesの所見をすべて直す以外に変更がなく、他の検査結果が維持されることが条件。JS警告まで解決済みという意味ではない。

| 対象 | 分類 | token-values所見数 | JS警告カテゴリ |
|---|---|---:|---|
|`components/accordion`|UI|1|なし|
|`components/accordion-gallery`|Lab|3|なし|
|`components/alert-dialog`|UI|3|js-global-bindings, js-single-instance|
|`components/aspect-ratio`|UI|1|なし|
|`components/aurora`|Lab|5|なし|
|`components/badge`|UI|1|なし|
|`components/bar-chart`|UI|1|なし|
|`components/beam-border`|Lab|3|なし|
|`components/blur-in`|Lab|1|なし|
|`components/bounce-letters`|Lab|1|なし|
|`components/converge`|Lab|17|なし|
|`components/dock`|Lab|6|なし|
|`components/donut-chart`|UI|1|なし|
|`components/drawer`|UI|2|js-global-bindings, js-single-instance|
|`components/dual-range`|UI|7|なし|
|`components/empty-state`|UI|1|なし|
|`components/fireworks`|Lab|1|なし|
|`components/follow-frame`|Lab|4|js-global-bindings, js-single-instance|
|`components/funnel-chart`|UI|1|なし|
|`components/glass-panel`|UI|3|なし|
|`components/glow-cards`|Lab|4|なし|
|`components/goo-cursor`|Lab|1|なし|
|`components/gravity-playground`|Lab|2|なし|
|`components/hanko`|UI|6|なし|
|`components/heatmap`|UI|2|なし|
|`components/horizontal-reel`|Lab|2|なし|
|`components/kata-rain`|Lab|1|なし|
|`components/kbd`|UI|1|なし|
|`components/kintsugi-card`|UI|1|なし|
|`components/liquid-button`|Lab|4|なし|
|`components/magnet`|Lab|4|なし|
|`components/marquee`|Lab|1|なし|
|`components/meteors`|Lab|4|なし|
|`components/newtons-cradle`|Lab|5|なし|
|`components/noren`|UI|6|なし|
|`components/orbit`|Lab|9|なし|
|`components/particle-net`|Lab|1|なし|
|`components/progress`|UI|1|なし|
|`components/qr-code`|UI|1|なし|
|`components/radio`|UI|3|なし|
|`components/rating`|UI|2|なし|
|`components/segmented`|UI|4|なし|
|`components/shine-text`|Lab|2|なし|
|`components/skeleton`|UI|1|なし|
|`components/slider`|UI|6|なし|
|`components/sparkles`|Lab|2|なし|
|`components/spinner`|UI|3|なし|
|`components/split-panel`|UI|2|js-global-bindings, js-single-instance|
|`components/spotlight`|Lab|2|なし|
|`components/stacking-cards`|Lab|2|なし|
|`components/stepper`|UI|1|なし|
|`components/steps`|UI|2|なし|
|`components/switch`|UI|5|なし|
|`components/tategaki`|UI|2|なし|
|`components/text-reveal`|Lab|1|なし|
|`components/tilt-card`|Lab|4|なし|
|`components/timeline`|UI|1|なし|
|`components/toggle`|UI|3|なし|
|`components/tooltip`|UI|4|なし|
|`components/torn-ticket`|UI|3|なし|
|`components/tour`|UI|7|なし|
|`components/tracing-beam`|Lab|3|なし|
|`components/typewriter`|Lab|1|なし|
|`components/warp-tunnel`|Lab|3|なし|
|`components/word-rotate`|Lab|1|なし|
|`blocks/cta-band`|UI|2|なし|
|`blocks/filter-toolbar`|UI|1|なし|
|`blocks/integrations`|UI|3|なし|
|`blocks/invoice`|UI|1|なし|
|`blocks/kanban`|UI|4|なし|
|`blocks/order-confirmation`|UI|2|なし|
|`blocks/plan-compare`|UI|1|なし|
|`blocks/pricing`|UI|1|js-global-bindings, js-single-instance|
|`blocks/roadmap`|UI|2|なし|
|`blocks/stat-cards`|UI|1|なし|
|`blocks/team`|UI|1|なし|
|`templates/checkout`|UI|3|なし|

77対象のtoken-valuesだけをすべて修正し他の結果が変わらなければ、現行ルールでは20+77=97/164合格になる試算。この77対象のうち5対象にはJS警告があるため、将来JS警告をerrorにする場合は同じ計算を使わず再集計する。

#### focus-visibleのみの対象

| 対象 | 所見数 |
|---|---:|
|`components/breadcrumbs`|3|
|`components/button`|1|
|`components/field`|2|
|`components/input-group`|5|
|`blocks/faq`|1|

#### その他3対象の内訳

|対象|失敗した検査|
|---|---|
|`components/carousel-ring`|shared-token-scope, token-values|
|`components/date-picker`|accessible-label, focus-visible, token-values|
|`components/toast`|focus-visible, shared-token-scope, token-values|

#### 全164対象の失敗パターン

|対象|パターン|失敗した検査|警告カテゴリ|
|---|---|---|---|
|`components/accordion`|token-valuesのみ|token-values|なし|
|`components/accordion-gallery`|token-valuesのみ|token-values|なし|
|`components/alert`|合格|なし|なし|
|`components/alert-dialog`|token-valuesのみ|token-values|js-global-bindings, js-single-instance|
|`components/aspect-ratio`|token-valuesのみ|token-values|なし|
|`components/aurora`|token-valuesのみ|token-values|なし|
|`components/avatar`|両方のみ|focus-visible, token-values|なし|
|`components/badge`|token-valuesのみ|token-values|なし|
|`components/bar-chart`|token-valuesのみ|token-values|なし|
|`components/beam-border`|token-valuesのみ|token-values|なし|
|`components/blur-in`|token-valuesのみ|token-values|なし|
|`components/bottom-navigation`|両方のみ|focus-visible, token-values|なし|
|`components/bounce-letters`|token-valuesのみ|token-values|なし|
|`components/breadcrumbs`|focus-visibleのみ|focus-visible|なし|
|`components/burst-button`|両方のみ|focus-visible, token-values|なし|
|`components/button`|focus-visibleのみ|focus-visible|なし|
|`components/button-group`|合格|なし|なし|
|`components/calendar`|両方のみ|focus-visible, token-values|なし|
|`components/candlestick-chart`|合格|なし|なし|
|`components/card`|両方のみ|focus-visible, token-values|なし|
|`components/carousel`|両方のみ|focus-visible, token-values|js-global-bindings, js-single-instance|
|`components/carousel-ring`|その他|shared-token-scope, token-values|なし|
|`components/cascader`|両方のみ|focus-visible, token-values|なし|
|`components/checkbox`|両方のみ|focus-visible, token-values|なし|
|`components/chip`|両方のみ|focus-visible, token-values|なし|
|`components/collapsible`|両方のみ|focus-visible, token-values|なし|
|`components/color-picker`|両方のみ|focus-visible, token-values|js-global-bindings, js-single-instance|
|`components/combobox`|合格|なし|なし|
|`components/command`|両方のみ|focus-visible, token-values|js-global-bindings, js-single-instance|
|`components/comparison-slider`|両方のみ|focus-visible, token-values|なし|
|`components/confetti-cannon`|両方のみ|focus-visible, token-values|なし|
|`components/context-menu`|両方のみ|focus-visible, token-values|js-global-bindings, js-single-instance|
|`components/converge`|token-valuesのみ|token-values|なし|
|`components/copy-field`|両方のみ|focus-visible, token-values|なし|
|`components/counter`|合格|なし|なし|
|`components/data-table`|両方のみ|focus-visible, token-values|js-global-bindings, js-single-instance|
|`components/date-picker`|その他|accessible-label, focus-visible, token-values|js-global-bindings, js-single-instance|
|`components/descriptions`|合格|なし|なし|
|`components/dock`|token-valuesのみ|token-values|なし|
|`components/donut-chart`|token-valuesのみ|token-values|なし|
|`components/drawer`|token-valuesのみ|token-values|js-global-bindings, js-single-instance|
|`components/dropdown`|両方のみ|focus-visible, token-values|なし|
|`components/dual-range`|token-valuesのみ|token-values|なし|
|`components/empty-state`|token-valuesのみ|token-values|なし|
|`components/field`|focus-visibleのみ|focus-visible|なし|
|`components/file-upload`|両方のみ|focus-visible, token-values|js-global-bindings, js-single-instance|
|`components/fireworks`|token-valuesのみ|token-values|なし|
|`components/follow-frame`|token-valuesのみ|token-values|js-global-bindings, js-single-instance|
|`components/funnel-chart`|token-valuesのみ|token-values|なし|
|`components/gauge`|合格|なし|なし|
|`components/glass-panel`|token-valuesのみ|token-values|なし|
|`components/glow-button`|両方のみ|focus-visible, token-values|なし|
|`components/glow-cards`|token-valuesのみ|token-values|なし|
|`components/goo-cursor`|token-valuesのみ|token-values|なし|
|`components/goo-tabs`|両方のみ|focus-visible, token-values|なし|
|`components/gravity-playground`|token-valuesのみ|token-values|なし|
|`components/hanko`|token-valuesのみ|token-values|なし|
|`components/heatmap`|token-valuesのみ|token-values|なし|
|`components/horizontal-reel`|token-valuesのみ|token-values|なし|
|`components/hover-card`|両方のみ|focus-visible, token-values|なし|
|`components/input`|両方のみ|focus-visible, token-values|なし|
|`components/input-group`|focus-visibleのみ|focus-visible|なし|
|`components/input-otp`|両方のみ|focus-visible, token-values|js-global-bindings|
|`components/jelly-buttons`|両方のみ|focus-visible, token-values|なし|
|`components/kaleidoscope`|両方のみ|focus-visible, token-values|なし|
|`components/kata-rain`|token-valuesのみ|token-values|なし|
|`components/kbd`|token-valuesのみ|token-values|なし|
|`components/kintsugi-card`|token-valuesのみ|token-values|なし|
|`components/line-chart`|合格|なし|なし|
|`components/liquid-button`|token-valuesのみ|token-values|なし|
|`components/list`|両方のみ|focus-visible, token-values|なし|
|`components/magnet`|token-valuesのみ|token-values|なし|
|`components/marquee`|token-valuesのみ|token-values|なし|
|`components/menubar`|両方のみ|focus-visible, token-values|なし|
|`components/meteors`|token-valuesのみ|token-values|なし|
|`components/meter`|合格|なし|なし|
|`components/modal`|両方のみ|focus-visible, token-values|なし|
|`components/navigation-menu`|両方のみ|focus-visible, token-values|なし|
|`components/newtons-cradle`|token-valuesのみ|token-values|なし|
|`components/noren`|token-valuesのみ|token-values|なし|
|`components/orbit`|token-valuesのみ|token-values|なし|
|`components/pagination`|両方のみ|focus-visible, token-values|なし|
|`components/particle-net`|token-valuesのみ|token-values|なし|
|`components/particle-word`|両方のみ|focus-visible, token-values|なし|
|`components/popover`|合格|なし|js-global-bindings, js-single-instance|
|`components/progress`|token-valuesのみ|token-values|なし|
|`components/qr-code`|token-valuesのみ|token-values|なし|
|`components/radar-chart`|合格|なし|なし|
|`components/radio`|token-valuesのみ|token-values|なし|
|`components/rating`|token-valuesのみ|token-values|なし|
|`components/reorder`|両方のみ|focus-visible, token-values|js-global-bindings, js-single-instance|
|`components/result`|合格|なし|なし|
|`components/scatter-chart`|合格|なし|なし|
|`components/scramble`|合格|なし|なし|
|`components/scroll-area`|両方のみ|focus-visible, token-values|なし|
|`components/scrollspy`|両方のみ|focus-visible, token-values|なし|
|`components/segmented`|token-valuesのみ|token-values|なし|
|`components/select`|両方のみ|focus-visible, token-values|なし|
|`components/separator`|合格|なし|なし|
|`components/shine-text`|token-valuesのみ|token-values|なし|
|`components/sidebar`|両方のみ|focus-visible, token-values|なし|
|`components/skeleton`|token-valuesのみ|token-values|なし|
|`components/slider`|token-valuesのみ|token-values|なし|
|`components/sparkles`|token-valuesのみ|token-values|なし|
|`components/sparkline`|合格|なし|なし|
|`components/speed-dial`|両方のみ|focus-visible, token-values|なし|
|`components/spinner`|token-valuesのみ|token-values|なし|
|`components/split-panel`|token-valuesのみ|token-values|js-global-bindings, js-single-instance|
|`components/spotlight`|token-valuesのみ|token-values|なし|
|`components/stacking-cards`|token-valuesのみ|token-values|なし|
|`components/stat`|合格|なし|なし|
|`components/stepper`|token-valuesのみ|token-values|なし|
|`components/steps`|token-valuesのみ|token-values|なし|
|`components/switch`|token-valuesのみ|token-values|なし|
|`components/table`|合格|なし|なし|
|`components/tabs`|両方のみ|focus-visible, token-values|なし|
|`components/tag-input`|両方のみ|focus-visible, token-values|js-global-bindings, js-single-instance|
|`components/tategaki`|token-valuesのみ|token-values|なし|
|`components/text-reveal`|token-valuesのみ|token-values|なし|
|`components/textarea`|両方のみ|focus-visible, token-values|なし|
|`components/tilt-card`|token-valuesのみ|token-values|なし|
|`components/time-picker`|両方のみ|focus-visible, token-values|なし|
|`components/timeline`|token-valuesのみ|token-values|なし|
|`components/toast`|その他|focus-visible, shared-token-scope, token-values|なし|
|`components/toggle`|token-valuesのみ|token-values|なし|
|`components/tooltip`|token-valuesのみ|token-values|なし|
|`components/torn-ticket`|token-valuesのみ|token-values|なし|
|`components/tour`|token-valuesのみ|token-values|なし|
|`components/tracing-beam`|token-valuesのみ|token-values|なし|
|`components/transfer`|両方のみ|focus-visible, token-values|なし|
|`components/tree`|両方のみ|focus-visible, token-values|なし|
|`components/typeset`|両方のみ|focus-visible, token-values|なし|
|`components/typewriter`|token-valuesのみ|token-values|なし|
|`components/wagara`|両方のみ|focus-visible, token-values|なし|
|`components/warp-tunnel`|token-valuesのみ|token-values|なし|
|`components/word-rotate`|token-valuesのみ|token-values|なし|
|`blocks/app-shell`|両方のみ|focus-visible, token-values|なし|
|`blocks/cookie-consent`|両方のみ|focus-visible, token-values|なし|
|`blocks/cta-band`|token-valuesのみ|token-values|なし|
|`blocks/faq`|focus-visibleのみ|focus-visible|なし|
|`blocks/filter-toolbar`|token-valuesのみ|token-values|なし|
|`blocks/integrations`|token-valuesのみ|token-values|なし|
|`blocks/invoice`|token-valuesのみ|token-values|なし|
|`blocks/kanban`|token-valuesのみ|token-values|なし|
|`blocks/login`|両方のみ|focus-visible, token-values|なし|
|`blocks/logo-cloud`|合格|なし|なし|
|`blocks/order-confirmation`|token-valuesのみ|token-values|なし|
|`blocks/plan-compare`|token-valuesのみ|token-values|なし|
|`blocks/pricing`|token-valuesのみ|token-values|js-global-bindings, js-single-instance|
|`blocks/roadmap`|token-valuesのみ|token-values|なし|
|`blocks/settings`|両方のみ|focus-visible, token-values|なし|
|`blocks/site-footer`|両方のみ|focus-visible, token-values|なし|
|`blocks/site-header`|両方のみ|focus-visible, token-values|js-global-bindings, js-single-instance|
|`blocks/stat-cards`|token-valuesのみ|token-values|なし|
|`blocks/team`|token-valuesのみ|token-values|なし|
|`blocks/testimonials`|合格|なし|なし|
|`blocks/use-cases`|両方のみ|focus-visible, token-values|js-global-bindings|
|`templates/blog-article`|両方のみ|focus-visible, token-values|なし|
|`templates/checkout`|token-valuesのみ|token-values|なし|
|`templates/dashboard`|両方のみ|focus-visible, token-values|なし|
|`templates/inbox`|両方のみ|focus-visible, token-values|なし|
|`templates/landing`|両方のみ|focus-visible, token-values|なし|
|`templates/product-page`|両方のみ|focus-visible, token-values|なし|
|`templates/settings-page`|両方のみ|focus-visible, token-values|なし|

### token-valuesの検出範囲を実行で確認

根拠: [tools/mold_rules.py](../tools/mold_rules.py) の `scan()`。property名にradius/shadow/duration/colorを含むか、background/border/animation/transition/fill/strokeのいずれかなら検査する。値中のpx/rem/em/ms/s、hexや色関数等を探す。宣言名が`--`で始まる場合は内容ごとスキップする。

調査方法: 一時ディレクトリの`components/sample/sample.css`を下のCSSに差し替え、現行の`inspect()`を呼んでtoken-valuesの結果だけを取り出した。候補以外の失敗はこの表では数えない。これは将来の修正を適用した数字ではない。

| 一時CSS | token-values結果 | 解釈 |
|---|---|---|
|`.sample{gap:7px}`|pass|検出しない|
|`.sample{margin:7px}`|pass|検出しない|
|`.sample{padding:7px}`|pass|検出しない|
|`.sample{font-size:14px}`|pass|検出しない|
|`.sample{font:14px sans-serif}`|pass|検出しない|
|`.sample{row-gap:7px}`|pass|検出しない|
|`.sample{column-gap:7px}`|pass|検出しない|
|`.sample{border-radius:7px}`|fail|検出される|
|`.sample{box-shadow:0 1px 2px #000}`|fail|検出される|
|`.sample{transition:opacity .13s}`|fail|検出される|
|`.sample{animation:spin .13s}`|fail|検出される|
|`.sample{animation-duration:130ms}`|fail|検出される|
|`.sample{animation-delay:.13s}`|pass|検出しない|
|`.sample{transition-delay:.13s}`|pass|検出しない|
|`.sample{--local-gap:7px;gap:var(--local-gap)}`|pass|検出しない|
|`.sample{--local-time:.13s;transition:opacity var(--local-time)}`|pass|検出しない|
|`.sample{transition:opacity var(--k-dur-1)}`|pass|既存共通トークン参照。正常な通過|
|`.sample{gap:calc(7px + var(--k-space-1))}`|pass|検出しない|
|`.sample{transition:opacity calc(.13s * 1)}`|fail|検出される|

#### button.cssの7pxと.13sが現在出ない理由

履歴`55968f1`のButtonには`gap:7px;transition:background .13s`があった。現在は[components/button/button.css](../components/button/button.css)の`.btn`内で`--k-btn-gap:7px;gap:var(--k-btn-gap)`になっている。**7pxという数値は残っている**。gap自体が検査対象外、かつローカルcustom property定義もスキップされるため、現検査はどちらの形でも失敗にしない。既存の共通spacingトークンへ移行済みと扱ってはいけない。

`.13s`は現在のButtonから消えており、transitionは`calc(var(--k-dur-1) * var(--k-mscale, 1))`を使う。`tokens.css`の`--k-dur-1:130ms`は共有定義なので、こちらは**共通トークン化済み**。同じ生の`.13s`をtransitionへ再導入した一時実験はfailになった。ただし`--local-time:.13s;transition:opacity var(--local-time)`へ移すとpassになるので、時間の間接参照に検査の穴がある。現Buttonの`--k-btn-spin-duration:700ms`もこの定義スキップの対象。

#### 検査強化案（このPRでは未実装）

1. 対象propertyを明示的な集合へ広げる。gap/row-gap/column-gap、margin/paddingと全logical longhand、font-sizeおよびfont shorthand、transition/animationのdurationとdelayを含める。`animation-delay`/`transition-delay`は現状durationという文字を含まないため検査漏れ。
2. CSSパーサーで値を単位付きトークンへ分解し、shorthand、calc、var fallback、複数のanimation/transitionを検証する。文字列/コメント/URLを除外し、負値や指数表記・単位の大文字小文字も回帰テストする。単純な正規表現の拡張だけで済ませない。
3. 使用箇所からvarの定義を辿り、共有トークン終端か、ローカル生値終端かを記録する。ローカル変数名に置き換えるだけの迂回は検出する。循環/未解決/実行時値は不明として別の所見にし、黙って合格させない。
4. AGENTSは部品ルートのローカル変数を許容しているので、幾何学的なローカル値を全部一律禁止しない。spacing/font/color/timeの標準化対象と、Lab固有の座標・形状・ユーザー選択色を区別する方針を明文化する。例外は範囲/理由を記録し、グローバル専用トークンへの移動で回避させない。
5. 追加対象の1所見=1宣言というカウント定義を維持し、既存433件と追加違反は別々に集計する。前節のspacing947・font-size533は棚卸し件数で、将来の厳密パーサー/定義解決後の失敗数ではない。新しい合格数を推測して公称しない。

### JS警告の合否への影響

根拠: [check.py](../check.py) の `passed = not any(c['status']=='fail' ...)`。js-single-instance/js-global-bindingsは[tools/mold_rules.py](../tools/mold_rules.py)でseverity=warningとして記録され、発見時status=warn。**今は合否に入らない**。summary.warnings=34は所見総数ではなく、warnになった「対象×検査」レコード数。

|検査|警告のある対象数|警告所見数|
|---|---:|---:|
|js-single-instance|16|24|
|js-global-bindings|18|57|

#### 同じJSONを使った失敗格上げの試算

| 条件 | 合格 | 不合格 | 新たに不合格になる対象 |
|---|---:|---:|---|
|現行|20|144|なし|
|single-instanceのみfail化|19|145|components/popover|
|global-bindingsのみfail化|19|145|components/popover|
|両方fail化|19|145|components/popover|

両方の警告は合わせて18対象にある。重複を除いた新規の不合格はPopoverだけで、既に不合格の対象は不合格数を増やさない。Popoverは単一dataセレクターとトップレベルconst（wrap/popBtn/popPanel）の両方に警告がある。

#### 格上げする実装案（未適用）

JSパーサーのASTでProgram直下のbindingとDOM単一取得を調べる。IIFE/モジュールスコープ、明示的な単一ページシェル、querySelectorAllによる複数初期化を区別する。現在のregexは文字列/テンプレート式/正規表現/構文で誤認の余地があるため、先に陽性/陰性のfixtureを整備し、再現できる違反からerrorへ格上げする。根拠のある例外は設定へ理由付きで限定し、全体一括allowlistにしない。IIFE化後は複数配置・二重ロード・IME・focusoutをブラウザーで検証する。上の19/164は現行warningを機械的にfail扱いした試算であり、AST導入後の確定値ではない。

### shared-token-scope: --k-ring-dangerの誤検知

結論: **Carousel Ringの専用トークンとしての判定は誤検知**。実装はdirectory名carousel-ringだけでなく、CSSの最初のクラス`.k-ring`から`ring`を自動で追加し、全グローバルトークンを`startswith("--k-ring-")`で調べる。そのため共有の`--k-ring-danger`がヒットする。

`tokens.css`の`--k-ring-danger`はdanger色のフォーカスshadowで、Inputの`.input.errb:focus`とTextareaの`[data-invalid="true"]:focus`が使っている。Carousel Ringはこれを参照していない。`.k-ring`という部品クラスと「focus ring」という共有役割が衝突している。

修正案: 所有namespaceは完全な部品名を原則にし、button→btnやcombobox→comboの短縮namespaceは明示した設定またはメタデータで所有を宣言する。任意の先頭クラスから短いnamespaceを自動推測しない。共有トークンの用途・複数部品での利用も監査し、danger focusのような実共有を特定する。該当1件だけを理由なくallowlistへ足す方式にはしない。共有名を装った専用値もあるため、単に複数使用箇所があれば無条件合格とはしない。

この誤検知1所見だけを除いた試算はshared-token-scope 3→2所見、該当対象2→1。Carousel Ringにはtoken-valuesが3件残るため、全体の合格数は20/164のまま。このPRでは検査を変更していない。

### 今回の検証と制限

最新mainで実際にcheck.pyを実行し、上記の件数・失敗組み合わせ・JS試算を同じJSONから算出。単一宣言の検出実験も現行inspect()を一時ディレクトリで呼び出して確認。部品コード・検査器・共有トークンは未変更。調査後に再実行したJSONの完全一致を確認する。将来の強化案の実装・ブラウザー/スクリーンリーダー・見た目の検証は今回行わない。

## 現在の検査結果

実行: `python3 check.py --json /tmp/token-migration-check.json`（終了1＝既存違反）。全体20/164合格・144不合格・警告34件。`token-values`は433所見、139対象。1所見は1個のCSS宣言の失敗で、1宣言内の色・長さ・秒を重複計上しない。同じ値が複数の例にあれば例ごとに数える。

現検査はradius/shadow/duration/colorとborder等のshorthandを対象にする。**spacingとfont-sizeは検査対象外**なので、後半に別の追加棚卸しとして示す。「433件」の内訳に混ぜない。JS文字列内のスタイル、動的に生成する値、style外のSVG属性、定義済みローカル変数の中身はこの集計に含めない。

## UI / Lab の分類

`build.py:lab_page()` と同じくmeta.categoryがMotionまたはKATAYABURIのcomponentをLab、残りをUIとする。blocks/templatesはUI。見た目の印象で例外を足さない。Fireworks/Confetti Cannon等が0件でも「安全」という意味ではなく、この検査が該当宣言を検出していないという意味。

| 分類 | 対象数 | token-valuesあり | 所見数 |
|---|---:|---:|---:|
|UI|121|98|295|
|Lab|43|41|138|
|合計|164|139|433|

### 検査433件の種類別集計

| 種類 | UI | Lab | 合計 |
|---|---:|---:|---:|
|radius|168|63|231|
|duration|47|42|89|
|shadow|36|10|46|
|color / paint|19|16|35|
|border|25|7|32|

## 置換表の使い方

各種類の表は「宣言の値そのもの」でまとめ、使用回数降順。propertyを併記するので同じ値でも異なる用途を混ぜない。候補は未採用であり、このPRで新しいトークンは追加しない。`var(--k-mscale, 1)`はFoundryの既存倍率。radiusの近似は明示し、見た目を確認する別PRに分ける。

追加案は全て共通名（種類＋連番）で、部品名由来の名前は提案しない。連番は今回の候補の識別用で、全候補を無条件にtokens.cssへ追加する方針ではない。利用箇所/意味が共有できる候補だけを採用し、Lab固有の幾何や単発の演出色は部品ルートのローカル変数が適切かも別途判断する。これは共有名の案を提示する集計であり、一部品の検査を通すためのグローバル変数増設を承認するものではない。

既存値の出どころはtokens.cssの:root。system/tokens.jsonにradius xl=16等があっても、CSS変数として未公開なら既存トークンとは数えない。未公開値を追加案として扱う。`--k-toast-*`は専用名なので置換候補に使わない。

### radius（231所見 / 23値）

| property | 生の値 | 回数 | UI / Lab | 置換候補 | 条件・理由 |
|---|---|---:|---|---|---|
|`border-radius`|`14px`|70|45 / 25|`var(--k-radius-step-01)`|同値。形状・計算結果を維持して置換候補にできる|
|`border-radius`|`8px`|23|22 / 1|`var(--k-radius)`|同値。形状・計算結果を維持して置換候補にできる|
|`border-radius`|`99px`|22|11 / 11|`var(--k-radius-full)`|同値。形状・計算結果を維持して置換候補にできる|
|`border-radius`|`16px`|14|12 / 2|`var(--k-radius-step-02)`|同値。形状・計算結果を維持して置換候補にできる|
|`border-radius`|`12px`|13|12 / 1|`var(--k-radius-lg)`|同値。形状・計算結果を維持して置換候補にできる|
|`border-radius`|`7px`|13|12 / 1|`var(--k-radius-sm)`|7px→6pxは近似、前後画像と判断が必要|
|`border-radius`|`11px`|12|8 / 4|`var(--k-radius-lg)`|11px→12pxは近似、前後画像と判断が必要|
|`border-radius`|`13px`|12|6 / 6|`var(--k-radius-lg)`|13px→12pxは近似、前後画像と判断が必要|
|`border-radius`|`10px`|11|8 / 3|`var(--k-radius-step-03)`|同値。形状・計算結果を維持して置換候補にできる|
|`border-radius`|`9px`|7|7 / 0|`var(--k-radius)`|9px→8pxは近似、前後画像と判断が必要|
|`border-radius`|`6px`|6|5 / 1|`var(--k-radius-sm)`|同値。形状・計算結果を維持して置換候補にできる|
|`border-radius`|`2px`|5|2 / 3|`var(--k-radius-step-04)`|同値。形状・計算結果を維持して置換候補にできる|
|`border-radius`|`3px`|5|5 / 0|`var(--k-radius-step-05)`|同値。形状・計算結果を維持して置換候補にできる|
|`border-radius`|`5px`|4|4 / 0|`var(--k-radius-sm)`|5px→6pxは近似、前後画像と判断が必要|
|`border-radius`|`18px`|3|2 / 1|`var(--k-radius-step-06)`|同値。形状・計算結果を維持して置換候補にできる|
|`border-radius`|`2.5px`|3|3 / 0|`var(--k-radius-step-07)`|同値。形状・計算結果を維持して置換候補にできる|
|`border-radius`|`4px`|2|1 / 1|`var(--k-radius-step-08)`|同値。形状・計算結果を維持して置換候補にできる|
|`border-radius`|`10px 10px 0 0`|1|1 / 0|`var(--k-radius-step-03) var(--k-radius-step-03) 0 0`|同値。形状・計算結果を維持して置換候補にできる|
|`border-radius`|`12.5px`|1|0 / 1|`var(--k-radius-lg)`|12.5px→12pxは近似、前後画像と判断が必要|
|`border-radius`|`20px`|1|0 / 1|`var(--k-radius-step-09)`|同値。形状・計算結果を維持して置換候補にできる|
|`border-radius`|`5px 5px 0 0`|1|1 / 0|`var(--k-radius-sm) var(--k-radius-sm) 0 0`|5px→6pxは近似、前後画像と判断が必要 / 5px→6pxは近似、前後画像と判断が必要|
|`border-radius`|`9.5px`|1|0 / 1|`var(--k-radius-step-10)`|同値。形状・計算結果を維持して置換候補にできる|
|`border-radius`|`9px 11px 10px 12px`|1|1 / 0|`var(--k-radius) var(--k-radius-lg) var(--k-radius-step-03) var(--k-radius-lg)`|9px→8pxは近似、前後画像と判断が必要 / 11px→12pxは近似、前後画像と判断が必要|

### duration（89所見 / 78値）

| property | 生の値 | 回数 | UI / Lab | 置換候補 | 条件・理由 |
|---|---|---:|---|---|---|
|`transition`|`transform .18s`|4|4 / 0|`transform calc(var(--k-dur-2) * var(--k-mscale, 1))`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`transition`|`opacity .15s,transform .15s`|3|2 / 1|`opacity calc(var(--k-duration-01) * var(--k-mscale, 1)),transform calc(var(--k-duration-01) * var(--k-mscale, 1))`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`animation`|`k-ga-spin 3.6s linear infinite`|2|0 / 2|`k-ga-spin calc(var(--k-duration-02) * var(--k-mscale, 1)) linear infinite`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`animation-duration`|`16s`|2|0 / 2|`calc(var(--k-duration-03) * var(--k-mscale, 1))`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`animation-duration`|`26s`|2|0 / 2|`calc(var(--k-duration-04) * var(--k-mscale, 1))`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`transition`|`background .13s`|2|2 / 0|`background calc(var(--k-dur-1) * var(--k-mscale, 1))`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`transition`|`border-color .13s, box-shadow .13s`|2|2 / 0|`border-color calc(var(--k-dur-1) * var(--k-mscale, 1)), box-shadow calc(var(--k-dur-1) * var(--k-mscale, 1))`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`transition`|`border-color .15s`|2|2 / 0|`border-color calc(var(--k-duration-01) * var(--k-mscale, 1))`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`animation`|`k-aur-a 9s var(--k-ease) infinite alternate`|1|0 / 1|`k-aur-a calc(var(--k-duration-05) * var(--k-mscale, 1)) var(--k-ease) infinite alternate`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`animation`|`k-aur-b 12s var(--k-ease) infinite alternate`|1|0 / 1|`k-aur-b calc(var(--k-duration-06) * var(--k-mscale, 1)) var(--k-ease) infinite alternate`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`animation`|`k-aur-c 11s var(--k-ease) infinite alternate`|1|0 / 1|`k-aur-c calc(var(--k-duration-07) * var(--k-mscale, 1)) var(--k-ease) infinite alternate`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`animation`|`k-aur-pat 26s linear infinite alternate`|1|0 / 1|`k-aur-pat calc(var(--k-duration-04) * var(--k-mscale, 1)) linear infinite alternate`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`animation`|`k-beam-spin 4.5s linear infinite`|1|0 / 1|`k-beam-spin calc(var(--k-duration-08) * var(--k-mscale, 1)) linear infinite`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`animation`|`k-blur-in .7s cubic-bezier(.2,.6,.2,1) forwards`|1|0 / 1|`k-blur-in calc(var(--k-duration-09) * var(--k-mscale, 1)) cubic-bezier(.2,.6,.2,1) forwards`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認。独自イージングは別途判断し、標準曲線へ機械置換しない|
|`animation`|`k-conv-pulse 3.4s var(--k-ease) infinite alternate`|1|0 / 1|`k-conv-pulse calc(var(--k-duration-10) * var(--k-mscale, 1)) var(--k-ease) infinite alternate`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`animation`|`k-conv-tw 2.2s ease-in-out infinite alternate`|1|0 / 1|`k-conv-tw calc(var(--k-duration-11) * var(--k-mscale, 1)) ease-in-out infinite alternate`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`animation`|`k-cr-l 2.4s ease-in-out infinite`|1|0 / 1|`k-cr-l calc(var(--k-duration-12) * var(--k-mscale, 1)) ease-in-out infinite`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`animation`|`k-cr-r 2.4s ease-in-out infinite`|1|0 / 1|`k-cr-r calc(var(--k-duration-12) * var(--k-mscale, 1)) ease-in-out infinite`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`animation`|`k-jelly-wob .55s cubic-bezier(.3,2.2,.45,1)`|1|0 / 1|`k-jelly-wob calc(var(--k-duration-13) * var(--k-mscale, 1)) cubic-bezier(.3,2.2,.45,1)`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認。独自イージングは別途判断し、標準曲線へ機械置換しない|
|`animation`|`k-marquee 30s linear infinite`|1|0 / 1|`k-marquee calc(var(--k-duration-14) * var(--k-mscale, 1)) linear infinite`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`animation`|`k-nor-sway 5.2s ease-in-out infinite alternate`|1|1 / 0|`k-nor-sway calc(var(--k-duration-15) * var(--k-mscale, 1)) ease-in-out infinite alternate`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`animation`|`k-nor-sway 5.8s ease-in-out infinite alternate`|1|1 / 0|`k-nor-sway calc(var(--k-duration-16) * var(--k-mscale, 1)) ease-in-out infinite alternate`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`animation`|`k-nor-sway 6.4s ease-in-out infinite alternate-reverse`|1|1 / 0|`k-nor-sway calc(var(--k-duration-17) * var(--k-mscale, 1)) ease-in-out infinite alternate-reverse`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`animation`|`k-ring-spin 26s linear infinite`|1|0 / 1|`k-ring-spin calc(var(--k-duration-04) * var(--k-mscale, 1)) linear infinite`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`animation`|`k-seal-in .5s cubic-bezier(.2,1.6,.4,1)`|1|1 / 0|`k-seal-in calc(var(--k-duration-18) * var(--k-mscale, 1)) cubic-bezier(.2,1.6,.4,1)`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認。独自イージングは別途判断し、標準曲線へ機械置換しない|
|`animation`|`k-seal-ring .55s ease-out`|1|1 / 0|`k-seal-ring calc(var(--k-duration-13) * var(--k-mscale, 1)) ease-out`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`animation`|`k-shimmer 1.4s ease-in-out infinite`|1|1 / 0|`k-shimmer calc(var(--k-duration-19) * var(--k-mscale, 1)) ease-in-out infinite`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`animation`|`k-shine-move 3.4s linear infinite`|1|0 / 1|`k-shine-move calc(var(--k-duration-10) * var(--k-mscale, 1)) linear infinite`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`animation`|`k-spin .7s linear infinite`|1|1 / 0|`k-spin calc(var(--k-duration-09) * var(--k-mscale, 1)) linear infinite`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`animation`|`k-tate-in 1s cubic-bezier(.2,.7,.2,1) both`|1|1 / 0|`k-tate-in calc(var(--k-duration-20) * var(--k-mscale, 1)) cubic-bezier(.2,.7,.2,1) both`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認。独自イージングは別途判断し、標準曲線へ機械置換しない|
|`animation`|`k-tin .3s cubic-bezier(.3,1.2,.4,1)`|1|1 / 0|`k-tin calc(var(--k-duration-21) * var(--k-mscale, 1)) cubic-bezier(.3,1.2,.4,1)`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認。独自イージングは別途判断し、標準曲線へ機械置換しない|
|`animation`|`k-type-blink 1.05s steps(1) infinite`|1|0 / 1|`k-type-blink calc(var(--k-duration-22) * var(--k-mscale, 1)) steps(1) infinite`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`animation`|`k-uc-in .45s var(--k-ease)`|1|1 / 0|`k-uc-in calc(var(--k-duration-23) * var(--k-mscale, 1)) var(--k-ease)`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`animation`|`k-warp-fly 5s linear infinite`|1|0 / 1|`k-warp-fly calc(var(--k-duration-24) * var(--k-mscale, 1)) linear infinite`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`animation-duration`|`1.6s`|1|1 / 0|`calc(var(--k-duration-25) * var(--k-mscale, 1))`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`transition`|`background .13s,border-color .13s`|1|1 / 0|`background calc(var(--k-dur-1) * var(--k-mscale, 1)),border-color calc(var(--k-dur-1) * var(--k-mscale, 1))`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`transition`|`background .13s,border-color .13s,color .13s`|1|1 / 0|`background calc(var(--k-dur-1) * var(--k-mscale, 1)),border-color calc(var(--k-dur-1) * var(--k-mscale, 1)),color calc(var(--k-dur-1) * var(--k-mscale, 1))`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`transition`|`background .15s`|1|1 / 0|`background calc(var(--k-duration-01) * var(--k-mscale, 1))`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`transition`|`background .15s,color .15s`|1|1 / 0|`background calc(var(--k-duration-01) * var(--k-mscale, 1)),color calc(var(--k-duration-01) * var(--k-mscale, 1))`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`transition`|`background .18s`|1|1 / 0|`background calc(var(--k-dur-2) * var(--k-mscale, 1))`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`transition`|`background .3s, box-shadow .3s`|1|0 / 1|`background calc(var(--k-duration-21) * var(--k-mscale, 1)), box-shadow calc(var(--k-duration-21) * var(--k-mscale, 1))`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`transition`|`border-color .14s`|1|1 / 0|`border-color calc(var(--k-duration-26) * var(--k-mscale, 1))`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`transition`|`border-color .15s,background .15s`|1|1 / 0|`border-color calc(var(--k-duration-01) * var(--k-mscale, 1)),background calc(var(--k-duration-01) * var(--k-mscale, 1))`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`transition`|`border-color .15s,box-shadow .15s`|1|1 / 0|`border-color calc(var(--k-duration-01) * var(--k-mscale, 1)),box-shadow calc(var(--k-duration-01) * var(--k-mscale, 1))`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`transition`|`box-shadow .3s`|1|0 / 1|`box-shadow calc(var(--k-duration-21) * var(--k-mscale, 1))`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`transition`|`color .25s`|1|0 / 1|`color calc(var(--k-duration-27) * var(--k-mscale, 1))`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`transition`|`color .4s`|1|0 / 1|`color calc(var(--k-duration-28) * var(--k-mscale, 1))`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`transition`|`fill .12s`|1|1 / 0|`fill calc(var(--k-duration-29) * var(--k-mscale, 1))`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`transition`|`flex .55s cubic-bezier(.6,0,.2,1)`|1|0 / 1|`flex calc(var(--k-duration-13) * var(--k-mscale, 1)) cubic-bezier(.6,0,.2,1)`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認。独自イージングは別途判断し、標準曲線へ機械置換しない|
|`transition`|`left .22s cubic-bezier(.3,.7,.3,1),width .22s cubic-bezier(.3,.7,.3,1)`|1|1 / 0|`left calc(var(--k-dur-3) * var(--k-mscale, 1)) var(--k-ease),width calc(var(--k-dur-3) * var(--k-mscale, 1)) var(--k-ease)`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`transition`|`left .45s cubic-bezier(.6,-0.1,.2,1.25), width .45s cubic-bezier(.6,-0.1,.2,1.25), transform .3s`|1|0 / 1|`left calc(var(--k-duration-23) * var(--k-mscale, 1)) cubic-bezier(.6,-0.1,.2,1.25), width calc(var(--k-duration-23) * var(--k-mscale, 1)) cubic-bezier(.6,-0.1,.2,1.25), transform calc(var(--k-duration-21) * var(--k-mscale, 1))`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認。独自イージングは別途判断し、標準曲線へ機械置換しない|
|`transition`|`opacity .15s`|1|1 / 0|`opacity calc(var(--k-duration-01) * var(--k-mscale, 1))`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`transition`|`opacity .16s var(--k-ease),transform .16s var(--k-ease)`|1|1 / 0|`opacity calc(var(--k-duration-30) * var(--k-mscale, 1)) var(--k-ease),transform calc(var(--k-duration-30) * var(--k-mscale, 1)) var(--k-ease)`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`transition`|`opacity .18s,transform .18s`|1|1 / 0|`opacity calc(var(--k-dur-2) * var(--k-mscale, 1)),transform calc(var(--k-dur-2) * var(--k-mscale, 1))`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`transition`|`opacity .25s`|1|0 / 1|`opacity calc(var(--k-duration-27) * var(--k-mscale, 1))`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`transition`|`opacity .3s .18s`|1|0 / 1|`opacity calc(var(--k-duration-21) * var(--k-mscale, 1)) calc(var(--k-dur-2) * var(--k-mscale, 1))`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`transition`|`transform .08s linear`|1|0 / 1|`transform calc(var(--k-duration-31) * var(--k-mscale, 1)) linear`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`transition`|`transform .12s`|1|0 / 1|`transform calc(var(--k-duration-29) * var(--k-mscale, 1))`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`transition`|`transform .12s ease-out`|1|0 / 1|`transform calc(var(--k-duration-29) * var(--k-mscale, 1)) ease-out`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`transition`|`transform .12s var(--k-ease)`|1|1 / 0|`transform calc(var(--k-duration-29) * var(--k-mscale, 1)) var(--k-ease)`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`transition`|`transform .13s`|1|1 / 0|`transform calc(var(--k-dur-1) * var(--k-mscale, 1))`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`transition`|`transform .14s ease-out`|1|0 / 1|`transform calc(var(--k-duration-26) * var(--k-mscale, 1)) ease-out`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`transition`|`transform .15s cubic-bezier(.3,.7,.3,1)`|1|1 / 0|`transform calc(var(--k-duration-01) * var(--k-mscale, 1)) var(--k-ease)`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`transition`|`transform .15s var(--k-ease)`|1|1 / 0|`transform calc(var(--k-duration-01) * var(--k-mscale, 1)) var(--k-ease)`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`transition`|`transform .15s var(--k-ease),opacity .15s`|1|1 / 0|`transform calc(var(--k-duration-01) * var(--k-mscale, 1)) var(--k-ease),opacity calc(var(--k-duration-01) * var(--k-mscale, 1))`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`transition`|`transform .18s cubic-bezier(.3,.7,.3,1)`|1|1 / 0|`transform calc(var(--k-dur-2) * var(--k-mscale, 1)) var(--k-ease)`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`transition`|`transform .28s cubic-bezier(.3,2.4,.45,1)`|1|0 / 1|`transform calc(var(--k-duration-32) * var(--k-mscale, 1)) cubic-bezier(.3,2.4,.45,1)`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認。独自イージングは別途判断し、標準曲線へ機械置換しない|
|`transition`|`transform .2s`|1|1 / 0|`transform calc(var(--k-duration-33) * var(--k-mscale, 1))`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`transition`|`transform .2s var(--k-ease)`|1|1 / 0|`transform calc(var(--k-duration-33) * var(--k-mscale, 1)) var(--k-ease)`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`transition`|`transform .34s cubic-bezier(.3,2.3,.4,1)`|1|0 / 1|`transform calc(var(--k-duration-34) * var(--k-mscale, 1)) cubic-bezier(.3,2.3,.4,1)`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認。独自イージングは別途判断し、標準曲線へ機械置換しない|
|`transition`|`transform .35s cubic-bezier(.2,.8,.25,1.2)`|1|0 / 1|`transform calc(var(--k-duration-35) * var(--k-mscale, 1)) cubic-bezier(.2,.8,.25,1.2)`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認。独自イージングは別途判断し、標準曲線へ機械置換しない|
|`transition`|`transform .3s ease-out`|1|0 / 1|`transform calc(var(--k-duration-21) * var(--k-mscale, 1)) ease-out`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`transition`|`transform .55s cubic-bezier(.65,0,.2,1)`|1|0 / 1|`transform calc(var(--k-duration-13) * var(--k-mscale, 1)) cubic-bezier(.65,0,.2,1)`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認。独自イージングは別途判断し、標準曲線へ機械置換しない|
|`transition`|`transform .5s cubic-bezier(.4,0,.2,1)`|1|1 / 0|`transform calc(var(--k-duration-18) * var(--k-mscale, 1)) cubic-bezier(.4,0,.2,1)`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認。独自イージングは別途判断し、標準曲線へ機械置換しない|
|`transition`|`transform .65s cubic-bezier(.5,0,.2,1)`|1|0 / 1|`transform calc(var(--k-duration-36) * var(--k-mscale, 1)) cubic-bezier(.5,0,.2,1)`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認。独自イージングは別途判断し、標準曲線へ機械置換しない|
|`transition`|`transform .7s cubic-bezier(.3,.7,.3,1)`|1|0 / 1|`transform calc(var(--k-duration-09) * var(--k-mscale, 1)) var(--k-ease)`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`transition`|`width .18s var(--k-ease),background .18s`|1|1 / 0|`width calc(var(--k-dur-2) * var(--k-mscale, 1)) var(--k-ease),background calc(var(--k-dur-2) * var(--k-mscale, 1))`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|
|`transition`|`width .3s cubic-bezier(.3,.7,.3,1)`|1|1 / 0|`width calc(var(--k-duration-21) * var(--k-mscale, 1)) var(--k-ease)`|時間・delayを同値で変数化。既存keyframe名、linear/ease等を保持。倍率1以外は挙動が変わるため要確認|

### shadow（46所見 / 39値）

| property | 生の値 | 回数 | UI / Lab | 置換候補 | 条件・理由 |
|---|---|---:|---|---|---|
|`box-shadow`|`0 20px 44px -14px rgba(16,24,40,.22)`|4|4 / 0|`var(--k-shadow-level-01)`|新規の共通候補。光源・色・多重リング・darkの役割を確認し、同じ用途だけで共有。近い影への自動置換はしない|
|`box-shadow`|`0 0 0 3px var(--k-accent-bg)`|2|2 / 0|`var(--k-shadow-level-02)`|新規の共通候補。光源・色・多重リング・darkの役割を確認し、同じ用途だけで共有。近い影への自動置換はしない|
|`box-shadow`|`0 1px 2px rgba(16,24,40,.18)`|2|2 / 0|`var(--k-shadow-level-03)`|新規の共通候補。光源・色・多重リング・darkの役割を確認し、同じ用途だけで共有。近い影への自動置換はしない|
|`box-shadow`|`0 1px 4px rgba(16,24,40,.18)`|2|2 / 0|`var(--k-shadow-level-04)`|新規の共通候補。光源・色・多重リング・darkの役割を確認し、同じ用途だけで共有。近い影への自動置換はしない|
|`box-shadow`|`0 30px 80px -20px rgba(0,0,0,.4)`|2|2 / 0|`var(--k-shadow-level-05)`|新規の共通候補。光源・色・多重リング・darkの役割を確認し、同じ用途だけで共有。近い影への自動置換はしない|
|`box-shadow`|`-24px 0 60px -24px rgba(0,0,0,.35)`|1|1 / 0|`var(--k-shadow-level-06)`|新規の共通候補。光源・色・多重リング・darkの役割を確認し、同じ用途だけで共有。近い影への自動置換はしない|
|`box-shadow`|`0 0 0 1px rgba(24,24,27,.25)`|1|0 / 1|`var(--k-shadow-level-07)`|新規の共通候補。光源・色・多重リング・darkの役割を確認し、同じ用途だけで共有。近い影への自動置換はしない|
|`box-shadow`|`0 0 0 1px var(--k-line)`|1|1 / 0|`var(--k-shadow-level-08)`|新規の共通候補。光源・色・多重リング・darkの役割を確認し、同じ用途だけで共有。近い影への自動置換はしない|
|`box-shadow`|`0 0 0 2px var(--k-accent)`|1|1 / 0|`var(--k-shadow-level-09)`|新規の共通候補。光源・色・多重リング・darkの役割を確認し、同じ用途だけで共有。近い影への自動置換はしない|
|`box-shadow`|`0 0 0 2px var(--k-bg),0 0 0 4px var(--k-accent)`|1|1 / 0|`var(--k-shadow-level-10)`|新規の共通候補。光源・色・多重リング・darkの役割を確認し、同じ用途だけで共有。近い影への自動置換はしない|
|`box-shadow`|`0 0 0 2px var(--k-ink)`|1|1 / 0|`var(--k-shadow-level-11)`|新規の共通候補。光源・色・多重リング・darkの役割を確認し、同じ用途だけで共有。近い影への自動置換はしない|
|`box-shadow`|`0 0 0 4px var(--k-accent-bg)`|1|0 / 1|`var(--k-shadow-level-12)`|新規の共通候補。光源・色・多重リング・darkの役割を確認し、同じ用途だけで共有。近い影への自動置換はしない|
|`box-shadow`|`0 0 0 5px var(--k-accent-bg-strong)`|1|1 / 0|`var(--k-shadow-level-13)`|新規の共通候補。光源・色・多重リング・darkの役割を確認し、同じ用途だけで共有。近い影への自動置換はしない|
|`box-shadow`|`0 0 10px 2px rgba(255,255,255,.3)`|1|0 / 1|`var(--k-shadow-level-14)`|新規の共通候補。光源・色・多重リング・darkの役割を確認し、同じ用途だけで共有。近い影への自動置換はしない|
|`box-shadow`|`0 0 18px -4px var(--k-accent-bg)`|1|0 / 1|`var(--k-shadow-level-15)`|新規の共通候補。光源・色・多重リング・darkの役割を確認し、同じ用途だけで共有。近い影への自動置換はしない|
|`box-shadow`|`0 0 26px -6px var(--k-accent)`|1|0 / 1|`var(--k-shadow-level-16)`|新規の共通候補。光源・色・多重リング・darkの役割を確認し、同じ用途だけで共有。近い影への自動置換はしない|
|`box-shadow`|`0 0 46px color-mix(in srgb,var(--k-accent) 45%,transparent)`|1|0 / 1|`var(--k-shadow-level-17)`|新規の共通候補。光源・色・多重リング・darkの役割を確認し、同じ用途だけで共有。近い影への自動置換はしない|
|`box-shadow`|`0 12px 26px -10px rgba(16,24,40,.4)`|1|0 / 1|`var(--k-shadow-level-18)`|新規の共通候補。光源・色・多重リング・darkの役割を確認し、同じ用途だけで共有。近い影への自動置換はしない|
|`box-shadow`|`0 14px 28px -14px rgba(16,24,40,.28)`|1|1 / 0|`var(--k-shadow-level-19)`|新規の共通候補。光源・色・多重リング・darkの役割を確認し、同じ用途だけで共有。近い影への自動置換はしない|
|`box-shadow`|`0 14px 34px -12px rgba(16,24,40,.25)`|1|1 / 0|`var(--k-shadow-level-20)`|新規の共通候補。光源・色・多重リング・darkの役割を確認し、同じ用途だけで共有。近い影への自動置換はしない|
|`box-shadow`|`0 16px 40px -12px rgba(16,24,40,.18)`|1|1 / 0|`var(--k-shadow-level-21)`|新規の共通候補。光源・色・多重リング・darkの役割を確認し、同じ用途だけで共有。近い影への自動置換はしない|
|`box-shadow`|`0 16px 40px -14px rgba(16,24,40,.25)`|1|1 / 0|`var(--k-shadow-level-22)`|新規の共通候補。光源・色・多重リング・darkの役割を確認し、同じ用途だけで共有。近い影への自動置換はしない|
|`box-shadow`|`0 18px 40px -12px rgba(16,24,40,.25)`|1|1 / 0|`var(--k-shadow-level-23)`|新規の共通候補。光源・色・多重リング・darkの役割を確認し、同じ用途だけで共有。近い影への自動置換はしない|
|`box-shadow`|`0 18px 40px -18px rgba(0,0,0,.45)`|1|1 / 0|`var(--k-shadow-level-24)`|新規の共通候補。光源・色・多重リング・darkの役割を確認し、同じ用途だけで共有。近い影への自動置換はしない|
|`box-shadow`|`0 18px 44px -14px rgba(16,24,40,.28)`|1|1 / 0|`var(--k-shadow-overlay)`|既存の同値トークン|
|`box-shadow`|`0 1px 2px rgba(16,24,40,.04)`|1|1 / 0|`var(--k-shadow-level-25)`|新規の共通候補。光源・色・多重リング・darkの役割を確認し、同じ用途だけで共有。近い影への自動置換はしない|
|`box-shadow`|`0 1px 2px rgba(16,24,40,.05)`|1|1 / 0|`var(--k-shadow-level-26)`|新規の共通候補。光源・色・多重リング・darkの役割を確認し、同じ用途だけで共有。近い影への自動置換はしない|
|`box-shadow`|`0 1px 2px rgba(16,24,40,.09)`|1|1 / 0|`var(--k-shadow-level-27)`|新規の共通候補。光源・色・多重リング・darkの役割を確認し、同じ用途だけで共有。近い影への自動置換はしない|
|`box-shadow`|`0 1px 3px rgba(0,0,0,.3),inset 0 0 0 1px rgba(0,0,0,.08)`|1|1 / 0|`var(--k-shadow-level-28)`|新規の共通候補。光源・色・多重リング・darkの役割を確認し、同じ用途だけで共有。近い影への自動置換はしない|
|`box-shadow`|`0 1px 3px rgba(16,24,40,.14)`|1|1 / 0|`var(--k-shadow-level-29)`|新規の共通候補。光源・色・多重リング・darkの役割を確認し、同じ用途だけで共有。近い影への自動置換はしない|
|`box-shadow`|`0 20px 44px -12px rgba(16,24,40,.28)`|1|1 / 0|`var(--k-shadow-level-30)`|新規の共通候補。光源・色・多重リング・darkの役割を確認し、同じ用途だけで共有。近い影への自動置換はしない|
|`box-shadow`|`0 20px 44px -14px rgba(0,0,0,.45)`|1|1 / 0|`var(--k-shadow-level-31)`|新規の共通候補。光源・色・多重リング・darkの役割を確認し、同じ用途だけで共有。近い影への自動置換はしない|
|`box-shadow`|`0 2px 10px rgba(16,24,40,.3)`|1|0 / 1|`var(--k-shadow-level-32)`|新規の共通候補。光源・色・多重リング・darkの役割を確認し、同じ用途だけで共有。近い影への自動置換はしない|
|`box-shadow`|`0 2px 8px rgba(16,24,40,.08)`|1|1 / 0|`var(--k-shadow-level-33)`|新規の共通候補。光源・色・多重リング・darkの役割を確認し、同じ用途だけで共有。近い影への自動置換はしない|
|`box-shadow`|`0 2px 8px rgba(16,24,40,.1)`|1|1 / 0|`var(--k-shadow-level-34)`|新規の共通候補。光源・色・多重リング・darkの役割を確認し、同じ用途だけで共有。近い影への自動置換はしない|
|`box-shadow`|`0 30px 80px -20px rgba(0,0,0,.45)`|1|1 / 0|`var(--k-shadow-level-35)`|新規の共通候補。光源・色・多重リング・darkの役割を確認し、同じ用途だけで共有。近い影への自動置換はしない|
|`box-shadow`|`0 3px 7px rgba(16,24,40,.25)`|1|0 / 1|`var(--k-shadow-level-36)`|新規の共通候補。光源・色・多重リング・darkの役割を確認し、同じ用途だけで共有。近い影への自動置換はしない|
|`box-shadow`|`0 4px 12px rgba(16,24,40,.1)`|1|0 / 1|`var(--k-shadow-level-37)`|新規の共通候補。光源・色・多重リング・darkの役割を確認し、同じ用途だけで共有。近い影への自動置換はしない|
|`box-shadow`|`0 6px 18px rgba(16,24,40,.28)`|1|1 / 0|`var(--k-shadow-level-38)`|新規の共通候補。光源・色・多重リング・darkの役割を確認し、同じ用途だけで共有。近い影への自動置換はしない|

### color / paint（35所見 / 31値）

| property | 生の値 | 回数 | UI / Lab | 置換候補 | 条件・理由 |
|---|---|---:|---|---|---|
|`background`|`rgba(24,24,27,.45)`|4|4 / 0|`var(--k-paint-01)`|新規の共通paint候補（色/gradient全体を同値維持）。LabパレットとUIの意味色を混同しない。dark時の値・contrastを要確認|
|`background`|`radial-gradient(circle at center,var(--k-core) 0 2.5px,var(--k-knob) 3.2px)`|2|2 / 0|`var(--k-paint-02)`|新規の共通paint候補（色/gradient全体を同値維持）。LabパレットとUIの意味色を混同しない。dark時の値・contrastを要確認|
|`background`|`hsl(0 0% 11%)`|1|1 / 0|`var(--k-paint-03)`|新規の共通paint候補（色/gradient全体を同値維持）。LabパレットとUIの意味色を混同しない。dark時の値・contrastを要確認|
|`background`|`hsl(152 30% 52%)`|1|1 / 0|`var(--k-paint-04)`|新規の共通paint候補（色/gradient全体を同値維持）。LabパレットとUIの意味色を混同しない。dark時の値・contrastを要確認|
|`background`|`hsl(175 84% 32%)`|1|1 / 0|`var(--k-paint-05)`|新規の共通paint候補（色/gradient全体を同値維持）。LabパレットとUIの意味色を混同しない。dark時の値・contrastを要確認|
|`background`|`hsl(190 59% 46%)`|1|1 / 0|`var(--k-paint-06)`|新規の共通paint候補（色/gradient全体を同値維持）。LabパレットとUIの意味色を混同しない。dark時の値・contrastを要確認|
|`background`|`hsl(199 65% 60%)`|1|1 / 0|`var(--k-paint-07)`|新規の共通paint候補（色/gradient全体を同値維持）。LabパレットとUIの意味色を混同しない。dark時の値・contrastを要確認|
|`background`|`hsl(216 68% 38%)`|1|1 / 0|`var(--k-paint-08)`|新規の共通paint候補（色/gradient全体を同値維持）。LabパレットとUIの意味色を混同しない。dark時の値・contrastを要確認|
|`background`|`hsl(265 27% 46%)`|1|1 / 0|`var(--k-paint-09)`|新規の共通paint候補（色/gradient全体を同値維持）。LabパレットとUIの意味色を混同しない。dark時の値・contrastを要確認|
|`background`|`hsl(346 39% 38%)`|1|1 / 0|`var(--k-paint-10)`|新規の共通paint候補（色/gradient全体を同値維持）。LabパレットとUIの意味色を混同しない。dark時の値・contrastを要確認|
|`background`|`hsl(41 100% 55%)`|1|1 / 0|`var(--k-paint-11)`|新規の共通paint候補（色/gradient全体を同値維持）。LabパレットとUIの意味色を混同しない。dark時の値・contrastを要確認|
|`background`|`linear-gradient(to right, rgba(255,255,255,.75), transparent)`|1|0 / 1|`var(--k-paint-12)`|新規の共通paint候補（色/gradient全体を同値維持）。LabパレットとUIの意味色を混同しない。dark時の値・contrastを要確認|
|`background`|`radial-gradient(190px circle at var(--mx,50%) var(--my,50%), var(--k-accent), transparent 70%)`|1|0 / 1|`var(--k-paint-13)`|新規の共通paint候補（色/gradient全体を同値維持）。LabパレットとUIの意味色を混同しない。dark時の値・contrastを要確認|
|`background`|`radial-gradient(200px circle at var(--mx) var(--my),rgba(255,255,255,.17),rgba(255,255,255,.05) 55%,transparent 72%)`|1|0 / 1|`var(--k-paint-14)`|新規の共通paint候補（色/gradient全体を同値維持）。LabパレットとUIの意味色を混同しない。dark時の値・contrastを要確認|
|`background`|`radial-gradient(340px circle at var(--gx,50%) var(--gy,50%), rgba(255,255,255,.14), transparent 65%)`|1|0 / 1|`var(--k-paint-15)`|新規の共通paint候補（色/gradient全体を同値維持）。LabパレットとUIの意味色を混同しない。dark時の値・contrastを要確認|
|`background`|`radial-gradient(circle at 38% 32%,color-mix(in srgb,hsl(335 85% 68%) 34%,transparent),transparent 62%),radial-gradient(circle at 66% 70%,color-mix(in srgb,hsl(205 90% 63%) 30%,transparent),transparent 62%),radial-gradient(circle,color-mix(in srgb,var(--k-accent) 42%,transparent),transparent 68%)`|1|0 / 1|`var(--k-paint-16)`|新規の共通paint候補（色/gradient全体を同値維持）。LabパレットとUIの意味色を混同しない。dark時の値・contrastを要確認|
|`background`|`radial-gradient(circle at center,var(--k-core) 0 3px,var(--k-knob) 3.6px)`|1|1 / 0|`var(--k-paint-17)`|新規の共通paint候補（色/gradient全体を同値維持）。LabパレットとUIの意味色を混同しない。dark時の値・contrastを要確認|
|`background`|`repeating-linear-gradient(90deg, var(--k-ink) 0 2px, transparent 2px 5px, var(--k-ink) 5px 6px, transparent 6px 10px, var(--k-ink) 10px 13px, transparent 13px 16px)`|1|1 / 0|`var(--k-paint-18)`|新規の共通paint候補（色/gradient全体を同値維持）。LabパレットとUIの意味色を混同しない。dark時の値・contrastを要確認|
|`background`|`rgba(24,24,27,.72)`|1|0 / 1|`var(--k-paint-19)`|新規の共通paint候補（色/gradient全体を同値維持）。LabパレットとUIの意味色を混同しない。dark時の値・contrastを要確認|
|`background`|`rgba(255,255,255,.16)`|1|1 / 0|`var(--k-paint-20)`|新規の共通paint候補（色/gradient全体を同値維持）。LabパレットとUIの意味色を混同しない。dark時の値・contrastを要確認|
|`color`|`#fff`|1|1 / 0|`var(--k-on-color)`|白の文字色候補。背景・SVGマスクならこの意味では使わない|
|`color`|`hsl(205 90% 66%)`|1|0 / 1|`var(--k-paint-21)`|新規の共通paint候補（色/gradient全体を同値維持）。LabパレットとUIの意味色を混同しない。dark時の値・contrastを要確認|
|`color`|`hsl(32 95% 64%)`|1|0 / 1|`var(--k-paint-22)`|新規の共通paint候補（色/gradient全体を同値維持）。LabパレットとUIの意味色を混同しない。dark時の値・contrastを要確認|
|`color`|`hsl(335 85% 72%)`|1|0 / 1|`var(--k-paint-23)`|新規の共通paint候補（色/gradient全体を同値維持）。LabパレットとUIの意味色を混同しない。dark時の値・contrastを要確認|
|`color`|`rgba(255,255,255,.3)`|1|0 / 1|`var(--k-paint-24)`|新規の共通paint候補（色/gradient全体を同値維持）。LabパレットとUIの意味色を混同しない。dark時の値・contrastを要確認|
|`fill`|`hsl(205 90% 63%)`|1|0 / 1|`var(--k-paint-25)`|新規の共通paint候補（色/gradient全体を同値維持）。LabパレットとUIの意味色を混同しない。dark時の値・contrastを要確認|
|`fill`|`hsl(32 95% 60%)`|1|0 / 1|`var(--k-paint-26)`|新規の共通paint候補（色/gradient全体を同値維持）。LabパレットとUIの意味色を混同しない。dark時の値・contrastを要確認|
|`fill`|`hsl(335 85% 68%)`|1|0 / 1|`var(--k-paint-27)`|新規の共通paint候補（色/gradient全体を同値維持）。LabパレットとUIの意味色を混同しない。dark時の値・contrastを要確認|
|`stroke`|`hsl(205 90% 63%)`|1|0 / 1|`var(--k-paint-25)`|新規の共通paint候補（色/gradient全体を同値維持）。LabパレットとUIの意味色を混同しない。dark時の値・contrastを要確認|
|`stroke`|`hsl(32 95% 60%)`|1|0 / 1|`var(--k-paint-26)`|新規の共通paint候補（色/gradient全体を同値維持）。LabパレットとUIの意味色を混同しない。dark時の値・contrastを要確認|
|`stroke`|`hsl(335 85% 68%)`|1|0 / 1|`var(--k-paint-27)`|新規の共通paint候補（色/gradient全体を同値維持）。LabパレットとUIの意味色を混同しない。dark時の値・contrastを要確認|

### border（32所見 / 19値）

| property | 生の値 | 回数 | UI / Lab | 置換候補 | 条件・理由 |
|---|---|---:|---|---|---|
|`border`|`1.5px dashed var(--k-border-strong)`|5|4 / 1|`calc(var(--k-space-1) * 0.375) dashed var(--k-border-strong)`|幅は同値換算。1px dashedはAGENTSの1px境界許可と現検査のsolid限定の差があるため、機械的にsolidへ変えない|
|`border`|`1.5px solid var(--k-border-strong)`|4|4 / 0|`calc(var(--k-space-1) * 0.375) solid var(--k-border-strong)`|幅は同値換算。1px dashedはAGENTSの1px境界許可と現検査のsolid限定の差があるため、機械的にsolidへ変えない|
|`border`|`2px solid var(--k-bg)`|3|3 / 0|`calc(var(--k-space-1) * 0.5) solid var(--k-bg)`|幅は同値換算。1px dashedはAGENTSの1px境界許可と現検査のsolid限定の差があるため、機械的にsolidへ変えない|
|`border`|`1px dashed var(--k-zinc-300)`|2|1 / 1|`1px dashed var(--k-zinc-300)`|幅は同値換算。1px dashedはAGENTSの1px境界許可と現検査のsolid限定の差があるため、機械的にsolidへ変えない|
|`border`|`2.5px solid var(--k-ink)`|2|2 / 0|`calc(var(--k-space-1) * 0.625) solid var(--k-ink)`|幅は同値換算。1px dashedはAGENTSの1px境界許可と現検査のsolid限定の差があるため、機械的にsolidへ変えない|
|`border`|`2px solid var(--k-line)`|2|2 / 0|`calc(var(--k-space-1) * 0.5) solid var(--k-line)`|幅は同値換算。1px dashedはAGENTSの1px境界許可と現検査のsolid限定の差があるため、機械的にsolidへ変えない|
|`border`|`2px solid var(--k-zinc-400)`|2|2 / 0|`calc(var(--k-space-1) * 0.5) solid var(--k-zinc-400)`|幅は同値換算。1px dashedはAGENTSの1px境界許可と現検査のsolid限定の差があるため、機械的にsolidへ変えない|
|`border`|`1.5px solid var(--k-bg)`|1|1 / 0|`calc(var(--k-space-1) * 0.375) solid var(--k-bg)`|幅は同値換算。1px dashedはAGENTSの1px境界許可と現検査のsolid限定の差があるため、機械的にsolidへ変えない|
|`border`|`1.5px solid var(--k-ink)`|1|0 / 1|`calc(var(--k-space-1) * 0.375) solid var(--k-ink)`|幅は同値換算。1px dashedはAGENTSの1px境界許可と現検査のsolid限定の差があるため、機械的にsolidへ変えない|
|`border`|`1px solid color-mix(in srgb,var(--k-on-color) 18%,transparent)`|1|0 / 1|`var(--k-border-treatment-01)`|混色率を含むborder全体の共通候補。透過は背景に依存。役割を決めてから採用|
|`border`|`1px solid color-mix(in srgb,var(--k-on-color) 25%,transparent)`|1|0 / 1|`var(--k-border-treatment-02)`|混色率を含むborder全体の共通候補。透過は背景に依存。役割を決めてから採用|
|`border`|`1px solid color-mix(in srgb,var(--k-on-color) 28%,transparent)`|1|0 / 1|`var(--k-border-treatment-03)`|混色率を含むborder全体の共通候補。透過は背景に依存。役割を決めてから採用|
|`border`|`1px solid color-mix(in srgb,var(--k-on-color) 32%,transparent)`|1|1 / 0|`var(--k-border-treatment-04)`|混色率を含むborder全体の共通候補。透過は背景に依存。役割を決めてから採用|
|`border`|`2px solid var(--k-accent)`|1|1 / 0|`calc(var(--k-space-1) * 0.5) solid var(--k-accent)`|幅は同値換算。1px dashedはAGENTSの1px境界許可と現検査のsolid限定の差があるため、機械的にsolidへ変えない|
|`border`|`2px solid var(--k-border-strong)`|1|1 / 0|`calc(var(--k-space-1) * 0.5) solid var(--k-border-strong)`|幅は同値換算。1px dashedはAGENTSの1px境界許可と現検査のsolid限定の差があるため、機械的にsolidへ変えない|
|`border`|`2px solid var(--k-core)`|1|1 / 0|`calc(var(--k-space-1) * 0.5) solid var(--k-core)`|幅は同値換算。1px dashedはAGENTSの1px境界許可と現検査のsolid限定の差があるため、機械的にsolidへ変えない|
|`border`|`2px solid var(--k-ink)`|1|1 / 0|`calc(var(--k-space-1) * 0.5) solid var(--k-ink)`|幅は同値換算。1px dashedはAGENTSの1px境界許可と現検査のsolid限定の差があるため、機械的にsolidへ変えない|
|`border`|`2px solid var(--k-zinc-700)`|1|0 / 1|`calc(var(--k-space-1) * 0.5) solid var(--k-zinc-700)`|幅は同値換算。1px dashedはAGENTSの1px境界許可と現検査のsolid限定の差があるため、機械的にsolidへ変えない|
|`border`|`5px solid transparent`|1|1 / 0|`calc(var(--k-space-1) * 1.25) solid transparent`|幅は同値換算。1px dashedはAGENTSの1px境界許可と現検査のsolid限定の差があるため、機械的にsolidへ変えない|

## 検査対象外の追加棚卸し（433件には含めない）

同じ164対象の部品CSSと例HTMLのinline/styleブロックから、単位付きのfont-sizeとspacing宣言だけを数えた。1宣言=1件で数える。0・百分率・既存変数のみの宣言は数えない。ここでの「所見」はAGENTSに沿った移行候補で、check.pyが失敗したという意味ではない。dimensions（width/height）、transform、行高等は今回は別集計しない。

### spacing（947所見 / 335値）

| property | 生の値 | 回数 | UI / Lab | 置換候補 | 条件・理由 |
|---|---|---:|---|---|---|
|`gap`|`9px`|45|42 / 3|`var(--k-space-step-01)`|同値。形状・計算結果を維持して置換候補にできる|
|`gap`|`8px`|41|39 / 2|`var(--k-space-2)`|同値。形状・計算結果を維持して置換候補にできる|
|`gap`|`10px`|34|34 / 0|`calc(var(--k-space-1) * 2.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`gap`|`7px`|27|24 / 3|`var(--k-space-step-02)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin-top`|`9px`|23|12 / 11|`var(--k-space-step-01)`|同値。形状・計算結果を維持して置換候補にできる|
|`gap`|`12px`|22|22 / 0|`var(--k-space-3)`|同値。形状・計算結果を維持して置換候補にできる|
|`gap`|`14px`|22|22 / 0|`calc(var(--k-space-1) * 3.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`gap`|`16px`|18|16 / 2|`var(--k-space-4)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin-top`|`5px`|18|15 / 3|`var(--k-space-step-03)`|同値。形状・計算結果を維持して置換候補にできる|
|`gap`|`2px`|16|16 / 0|`calc(var(--k-space-1) * 0.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`gap`|`6px`|16|13 / 3|`calc(var(--k-space-1) * 1.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`gap`|`11px`|15|14 / 1|`var(--k-space-step-04)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin-top`|`16px`|14|13 / 1|`var(--k-space-4)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin-top`|`8px`|14|9 / 5|`var(--k-space-2)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`20px`|13|10 / 3|`calc(var(--k-space-1) * 5)`|同値。形状・計算結果を維持して置換候補にできる|
|`gap`|`13px`|12|9 / 3|`var(--k-space-step-05)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin-top`|`6px`|11|10 / 1|`calc(var(--k-space-1) * 1.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin-top`|`7px`|10|8 / 2|`var(--k-space-step-02)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin-top`|`14px`|9|9 / 0|`calc(var(--k-space-1) * 3.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin-top`|`18px`|9|9 / 0|`calc(var(--k-space-1) * 4.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin-top`|`4px`|9|9 / 0|`var(--k-space-1)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`16px`|9|8 / 1|`var(--k-space-4)`|同値。形状・計算結果を維持して置換候補にできる|
|`gap`|`26px`|7|6 / 1|`calc(var(--k-space-1) * 6.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin-bottom`|`12px`|7|7 / 0|`var(--k-space-3)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`14px`|7|5 / 2|`calc(var(--k-space-1) * 3.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`26px`|7|6 / 1|`calc(var(--k-space-1) * 6.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`7px 9px`|7|7 / 0|`var(--k-space-step-02) var(--k-space-step-01)`|同値。形状・計算結果を維持して置換候補にできる|
|`gap`|`20px`|6|4 / 2|`calc(var(--k-space-1) * 5)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin-bottom`|`18px`|6|6 / 0|`calc(var(--k-space-1) * 4.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin-top`|`10px`|6|3 / 3|`calc(var(--k-space-1) * 2.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin-top`|`12px`|6|5 / 1|`var(--k-space-3)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin-top`|`3px`|6|3 / 3|`var(--k-space-step-06)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`8px 0`|6|3 / 3|`var(--k-space-2) 0`|同値。形状・計算結果を維持して置換候補にできる|
|`gap`|`4px`|5|5 / 0|`var(--k-space-1)`|同値。形状・計算結果を維持して置換候補にできる|
|`gap`|`5px`|5|4 / 1|`var(--k-space-step-03)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin-bottom`|`5px`|5|4 / 1|`var(--k-space-step-03)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin-top`|`1px`|5|5 / 0|`var(--k-space-step-07)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`15px`|5|5 / 0|`var(--k-space-step-08)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`24px`|5|4 / 1|`var(--k-space-6)`|同値。形状・計算結果を維持して置換候補にできる|
|`top`|`calc(100% + 8px)`|5|5 / 0|`calc(100% + var(--k-space-2))`|同値。形状・計算結果を維持して置換候補にできる|
|`bottom`|`4px`|4|2 / 2|`var(--k-space-1)`|同値。形状・計算結果を維持して置換候補にできる|
|`gap`|`22px`|4|4 / 0|`calc(var(--k-space-1) * 5.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`gap`|`3px`|4|4 / 0|`var(--k-space-step-06)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin-bottom`|`9px`|4|4 / 0|`var(--k-space-step-01)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin-top`|`20px`|4|4 / 0|`calc(var(--k-space-1) * 5)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin-top`|`2px`|4|4 / 0|`calc(var(--k-space-1) * 0.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`12px`|4|3 / 1|`var(--k-space-3)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`12px 14px`|4|4 / 0|`var(--k-space-3) calc(var(--k-space-1) * 3.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`18px`|4|2 / 2|`calc(var(--k-space-1) * 4.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`22px`|4|2 / 2|`calc(var(--k-space-1) * 5.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`2px`|4|2 / 2|`calc(var(--k-space-1) * 0.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`5px`|4|4 / 0|`var(--k-space-step-03)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`8px 10px`|4|4 / 0|`var(--k-space-2) calc(var(--k-space-1) * 2.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`top`|`4px`|4|0 / 4|`var(--k-space-1)`|同値。形状・計算結果を維持して置換候補にできる|
|`bottom`|`12px`|3|0 / 3|`var(--k-space-3)`|同値。形状・計算結果を維持して置換候補にできる|
|`gap`|`18px`|3|3 / 0|`calc(var(--k-space-1) * 4.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`left`|`16px`|3|1 / 2|`var(--k-space-4)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin-bottom`|`10px`|3|3 / 0|`calc(var(--k-space-1) * 2.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin-bottom`|`11px`|3|2 / 1|`var(--k-space-step-04)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin-bottom`|`14px`|3|2 / 1|`calc(var(--k-space-1) * 3.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin-bottom`|`16px`|3|3 / 0|`var(--k-space-4)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin-top`|`11px`|3|3 / 0|`var(--k-space-step-04)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin-top`|`22px`|3|3 / 0|`calc(var(--k-space-1) * 5.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`0 12px`|3|2 / 1|`0 var(--k-space-3)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`0 6px`|3|3 / 0|`0 calc(var(--k-space-1) * 1.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`10px`|3|2 / 1|`calc(var(--k-space-1) * 2.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`10px 12px`|3|2 / 1|`calc(var(--k-space-1) * 2.5) var(--k-space-3)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`11px 14px`|3|3 / 0|`var(--k-space-step-04) calc(var(--k-space-1) * 3.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`14px 8px`|3|3 / 0|`calc(var(--k-space-1) * 3.5) var(--k-space-2)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`18px 20px`|3|3 / 0|`calc(var(--k-space-1) * 4.5) calc(var(--k-space-1) * 5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`3px`|3|3 / 0|`var(--k-space-step-06)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`9px 10px`|3|2 / 1|`var(--k-space-step-01) calc(var(--k-space-1) * 2.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`top`|`3px`|3|3 / 0|`var(--k-space-step-06)`|同値。形状・計算結果を維持して置換候補にできる|
|`bottom`|`14px`|2|2 / 0|`calc(var(--k-space-1) * 3.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`bottom`|`18px`|2|2 / 0|`calc(var(--k-space-1) * 4.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`gap`|`34px`|2|2 / 0|`calc(var(--k-space-1) * 8.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`left`|`10px`|2|1 / 1|`calc(var(--k-space-1) * 2.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`left`|`18px`|2|2 / 0|`calc(var(--k-space-1) * 4.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`left`|`7px`|2|0 / 2|`var(--k-space-step-02)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin`|`0 0 14px`|2|2 / 0|`0 0 calc(var(--k-space-1) * 3.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin`|`16px 10px 6px`|2|2 / 0|`var(--k-space-4) calc(var(--k-space-1) * 2.5) calc(var(--k-space-1) * 1.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin`|`18px 0`|2|2 / 0|`calc(var(--k-space-1) * 4.5) 0`|同値。形状・計算結果を維持して置換候補にできる|
|`margin`|`5px 4px`|2|2 / 0|`var(--k-space-step-03) var(--k-space-1)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin-bottom`|`20px`|2|1 / 1|`calc(var(--k-space-1) * 5)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin-bottom`|`22px`|2|2 / 0|`calc(var(--k-space-1) * 5.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin-bottom`|`3px`|2|2 / 0|`var(--k-space-step-06)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin-bottom`|`6px`|2|2 / 0|`calc(var(--k-space-1) * 1.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin-inline-end`|`5px`|2|2 / 0|`var(--k-space-step-03)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin-top`|`24px`|2|2 / 0|`var(--k-space-6)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`0 11px`|2|2 / 0|`0 var(--k-space-step-04)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`0 13px`|2|2 / 0|`0 var(--k-space-step-05)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`0 1px`|2|2 / 0|`0 var(--k-space-step-07)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`0 9px`|2|2 / 0|`0 var(--k-space-step-01)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`1.5px`|2|0 / 2|`var(--k-space-step-09)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`10px 0`|2|0 / 2|`calc(var(--k-space-1) * 2.5) 0`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`10px 14px`|2|2 / 0|`calc(var(--k-space-1) * 2.5) calc(var(--k-space-1) * 3.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`12px 0 2px`|2|2 / 0|`var(--k-space-3) 0 calc(var(--k-space-1) * 0.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`12px 8px 2px`|2|2 / 0|`var(--k-space-3) var(--k-space-2) calc(var(--k-space-1) * 0.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`13px 0`|2|2 / 0|`var(--k-space-step-05) 0`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`13px 18px`|2|2 / 0|`var(--k-space-step-05) calc(var(--k-space-1) * 4.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`13px 26px`|2|0 / 2|`var(--k-space-step-05) calc(var(--k-space-1) * 6.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`15px 17px`|2|2 / 0|`var(--k-space-step-08) var(--k-space-step-10)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`16px 12px`|2|2 / 0|`var(--k-space-4) var(--k-space-3)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`16px 18px`|2|2 / 0|`var(--k-space-4) calc(var(--k-space-1) * 4.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`17px`|2|2 / 0|`var(--k-space-step-10)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`1px 5px`|2|2 / 0|`var(--k-space-step-07) var(--k-space-step-03)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`20px 22px`|2|1 / 1|`calc(var(--k-space-1) * 5) calc(var(--k-space-1) * 5.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`26px 18px`|2|2 / 0|`calc(var(--k-space-1) * 6.5) calc(var(--k-space-1) * 4.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`2px 0 2px 16px`|2|2 / 0|`calc(var(--k-space-1) * 0.5) 0 calc(var(--k-space-1) * 0.5) var(--k-space-4)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`30px 26px`|2|1 / 1|`calc(var(--k-space-1) * 7.5) calc(var(--k-space-1) * 6.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`4px`|2|1 / 1|`var(--k-space-1)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`4px 9px`|2|0 / 2|`var(--k-space-1) var(--k-space-step-01)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`5px 8px`|2|2 / 0|`var(--k-space-step-03) var(--k-space-2)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`6px`|2|2 / 0|`calc(var(--k-space-1) * 1.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`6px 10px`|2|2 / 0|`calc(var(--k-space-1) * 1.5) calc(var(--k-space-1) * 2.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`8px 14px`|2|1 / 1|`var(--k-space-2) calc(var(--k-space-1) * 3.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`9px 0`|2|2 / 0|`var(--k-space-step-01) 0`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`9px 8px`|2|2 / 0|`var(--k-space-step-01) var(--k-space-2)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding-bottom`|`4px`|2|2 / 0|`var(--k-space-1)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding-bottom`|`8px`|2|2 / 0|`var(--k-space-2)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding-inline-end`|`6px`|2|1 / 1|`calc(var(--k-space-1) * 1.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding-inline-start`|`20px`|2|2 / 0|`calc(var(--k-space-1) * 5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding-right`|`42px`|2|2 / 0|`calc(var(--k-space-1) * 10.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding-top`|`11px`|2|2 / 0|`var(--k-space-step-04)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding-top`|`16px`|2|2 / 0|`var(--k-space-4)`|同値。形状・計算結果を維持して置換候補にできる|
|`right`|`10px`|2|1 / 1|`calc(var(--k-space-1) * 2.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`right`|`14px`|2|1 / 1|`calc(var(--k-space-1) * 3.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`right`|`6px`|2|2 / 0|`calc(var(--k-space-1) * 1.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`top`|`11px`|2|2 / 0|`var(--k-space-step-04)`|同値。形状・計算結果を維持して置換候補にできる|
|`top`|`14px`|2|2 / 0|`calc(var(--k-space-1) * 3.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`top`|`16px`|2|2 / 0|`var(--k-space-4)`|同値。形状・計算結果を維持して置換候補にできる|
|`top`|`78px`|2|2 / 0|`calc(var(--k-space-1) * 19.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`bottom`|`13px`|1|0 / 1|`var(--k-space-step-05)`|同値。形状・計算結果を維持して置換候補にできる|
|`bottom`|`2px`|1|1 / 0|`calc(var(--k-space-1) * 0.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`bottom`|`3px`|1|1 / 0|`var(--k-space-step-06)`|同値。形状・計算結果を維持して置換候補にできる|
|`bottom`|`calc(100% + 2px)`|1|1 / 0|`calc(100% + calc(var(--k-space-1) * 0.5))`|同値。形状・計算結果を維持して置換候補にできる|
|`bottom`|`calc(100% + 7px)`|1|1 / 0|`calc(100% + var(--k-space-step-02))`|同値。形状・計算結果を維持して置換候補にできる|
|`bottom`|`calc(100% + 9px)`|1|0 / 1|`calc(100% + var(--k-space-step-01))`|同値。形状・計算結果を維持して置換候補にできる|
|`gap`|`1px`|1|1 / 0|`var(--k-space-step-07)`|同値。形状・計算結果を維持して置換候補にできる|
|`gap`|`24px`|1|1 / 0|`var(--k-space-6)`|同値。形状・計算結果を維持して置換候補にできる|
|`gap`|`28px`|1|1 / 0|`calc(var(--k-space-1) * 7)`|同値。形状・計算結果を維持して置換候補にできる|
|`gap`|`44px`|1|0 / 1|`calc(var(--k-space-1) * 11)`|同値。形状・計算結果を維持して置換候補にできる|
|`inset`|`26px`|1|0 / 1|`calc(var(--k-space-1) * 6.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`inset-inline-end`|`10px`|1|1 / 0|`calc(var(--k-space-1) * 2.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`inset-inline-end`|`18px`|1|1 / 0|`calc(var(--k-space-1) * 4.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`inset-inline-start`|`3px`|1|1 / 0|`var(--k-space-step-06)`|同値。形状・計算結果を維持して置換候補にできる|
|`left`|`118px`|1|1 / 0|`calc(var(--k-space-1) * 29.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`left`|`120px`|1|1 / 0|`calc(var(--k-space-1) * 30)`|同値。形状・計算結果を維持して置換候補にできる|
|`left`|`13px`|1|0 / 1|`var(--k-space-step-05)`|同値。形状・計算結果を維持して置換候補にできる|
|`left`|`14px`|1|1 / 0|`calc(var(--k-space-1) * 3.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`left`|`15px`|1|0 / 1|`var(--k-space-step-08)`|同値。形状・計算結果を維持して置換候補にできる|
|`left`|`20px`|1|1 / 0|`calc(var(--k-space-1) * 5)`|同値。形状・計算結果を維持して置換候補にできる|
|`left`|`28px`|1|1 / 0|`calc(var(--k-space-1) * 7)`|同値。形状・計算結果を維持して置換候補にできる|
|`left`|`2px`|1|0 / 1|`calc(var(--k-space-1) * 0.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`left`|`3px`|1|0 / 1|`var(--k-space-step-06)`|同値。形状・計算結果を維持して置換候補にできる|
|`left`|`44px`|1|1 / 0|`calc(var(--k-space-1) * 11)`|同値。形状・計算結果を維持して置換候補にできる|
|`left`|`4px`|1|1 / 0|`var(--k-space-1)`|同値。形状・計算結果を維持して置換候補にできる|
|`left`|`96px`|1|1 / 0|`calc(var(--k-space-1) * 24)`|同値。形状・計算結果を維持して置換候補にできる|
|`left`|`calc(-50% + 16px)`|1|1 / 0|`calc(-50% + var(--k-space-4))`|同値。形状・計算結果を維持して置換候補にできる|
|`margin`|`0 0 10px`|1|1 / 0|`0 0 calc(var(--k-space-1) * 2.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin`|`0 0 15px`|1|1 / 0|`0 0 var(--k-space-step-08)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin`|`0 0 5px`|1|1 / 0|`0 0 var(--k-space-step-03)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin`|`0 0 8px`|1|1 / 0|`0 0 var(--k-space-2)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin`|`0 26px 0 2px`|1|1 / 0|`0 calc(var(--k-space-1) * 6.5) 0 calc(var(--k-space-1) * 0.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin`|`0 auto 15px`|1|1 / 0|`0 auto var(--k-space-step-08)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin`|`10px 0 0`|1|0 / 1|`calc(var(--k-space-1) * 2.5) 0 0`|同値。形状・計算結果を維持して置換候補にできる|
|`margin`|`10px auto 22px`|1|1 / 0|`calc(var(--k-space-1) * 2.5) auto calc(var(--k-space-1) * 5.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin`|`11px 0 0`|1|1 / 0|`var(--k-space-step-04) 0 0`|同値。形状・計算結果を維持して置換候補にできる|
|`margin`|`12px 0 0`|1|1 / 0|`var(--k-space-3) 0 0`|同値。形状・計算結果を維持して置換候補にできる|
|`margin`|`12px 0 10px`|1|1 / 0|`var(--k-space-3) 0 calc(var(--k-space-1) * 2.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin`|`12px 0 2px`|1|1 / 0|`var(--k-space-3) 0 calc(var(--k-space-1) * 0.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin`|`14px 0`|1|1 / 0|`calc(var(--k-space-1) * 3.5) 0`|同値。形状・計算結果を維持して置換候補にできる|
|`margin`|`14px 10px 6px`|1|1 / 0|`calc(var(--k-space-1) * 3.5) calc(var(--k-space-1) * 2.5) calc(var(--k-space-1) * 1.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin`|`15px 0 4px`|1|1 / 0|`var(--k-space-step-08) 0 var(--k-space-1)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin`|`15px 0 8px`|1|1 / 0|`var(--k-space-step-08) 0 var(--k-space-2)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin`|`18px 0 14px`|1|1 / 0|`calc(var(--k-space-1) * 4.5) 0 calc(var(--k-space-1) * 3.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin`|`18px 0 20px`|1|1 / 0|`calc(var(--k-space-1) * 4.5) 0 calc(var(--k-space-1) * 5)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin`|`20px 0`|1|1 / 0|`calc(var(--k-space-1) * 5) 0`|同値。形状・計算結果を維持して置換候補にできる|
|`margin`|`22px 0`|1|1 / 0|`calc(var(--k-space-1) * 5.5) 0`|同値。形状・計算結果を維持して置換候補にできる|
|`margin`|`22px 0 6px`|1|1 / 0|`calc(var(--k-space-1) * 5.5) 0 calc(var(--k-space-1) * 1.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin`|`24px 0`|1|1 / 0|`var(--k-space-6) 0`|同値。形状・計算結果を維持して置換候補にできる|
|`margin`|`26px 0 10px`|1|1 / 0|`calc(var(--k-space-1) * 6.5) 0 calc(var(--k-space-1) * 2.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin`|`2px 0 2px 25px`|1|1 / 0|`calc(var(--k-space-1) * 0.5) 0 calc(var(--k-space-1) * 0.5) var(--k-space-step-11)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin`|`30px 0 8px`|1|1 / 0|`calc(var(--k-space-1) * 7.5) 0 var(--k-space-2)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin`|`4px 0`|1|1 / 0|`var(--k-space-1) 0`|同値。形状・計算結果を維持して置換候補にできる|
|`margin`|`5px 8px`|1|1 / 0|`var(--k-space-step-03) var(--k-space-2)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin`|`6px 0 13px`|1|1 / 0|`calc(var(--k-space-1) * 1.5) 0 var(--k-space-step-05)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin`|`6px 0 5px`|1|1 / 0|`calc(var(--k-space-1) * 1.5) 0 var(--k-space-step-03)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin`|`6px auto`|1|0 / 1|`calc(var(--k-space-1) * 1.5) auto`|同値。形状・計算結果を維持して置換候補にできる|
|`margin`|`7px 0 14px`|1|0 / 1|`var(--k-space-step-02) 0 calc(var(--k-space-1) * 3.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin`|`8px 0 6px`|1|0 / 1|`var(--k-space-2) 0 calc(var(--k-space-1) * 1.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin`|`8px 0 7px`|1|1 / 0|`var(--k-space-2) 0 var(--k-space-step-02)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin`|`9px 0 7px`|1|1 / 0|`var(--k-space-step-01) 0 var(--k-space-step-02)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin`|`9px 10px 4px`|1|1 / 0|`var(--k-space-step-01) calc(var(--k-space-1) * 2.5) var(--k-space-1)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin-bottom`|`-.12em`|1|0 / 1|`var(--k-space-step-12)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin-bottom`|`13px`|1|1 / 0|`var(--k-space-step-05)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin-bottom`|`15px`|1|1 / 0|`var(--k-space-step-08)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin-bottom`|`1px`|1|1 / 0|`var(--k-space-step-07)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin-bottom`|`2px`|1|1 / 0|`calc(var(--k-space-1) * 0.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin-bottom`|`4px`|1|1 / 0|`var(--k-space-1)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin-bottom`|`8px`|1|1 / 0|`var(--k-space-2)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin-inline-end`|`8px`|1|1 / 0|`var(--k-space-2)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin-inline-end`|`9px`|1|1 / 0|`var(--k-space-step-01)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin-inline-start`|`2px`|1|0 / 1|`calc(var(--k-space-1) * 0.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin-inline-start`|`5px`|1|1 / 0|`var(--k-space-step-03)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin-inline-start`|`8px`|1|1 / 0|`var(--k-space-2)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin-left`|`8px`|1|1 / 0|`var(--k-space-2)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin-top`|`13px`|1|1 / 0|`var(--k-space-step-05)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin-top`|`15px`|1|1 / 0|`var(--k-space-step-08)`|同値。形状・計算結果を維持して置換候補にできる|
|`margin-top`|`26px`|1|1 / 0|`calc(var(--k-space-1) * 6.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`0 0 18px 22px`|1|1 / 0|`0 0 calc(var(--k-space-1) * 4.5) calc(var(--k-space-1) * 5.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`0 17px 17px 41px`|1|1 / 0|`0 var(--k-space-step-10) var(--k-space-step-10) var(--k-space-step-13)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`0 18px`|1|0 / 1|`0 calc(var(--k-space-1) * 4.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`0 26px`|1|0 / 1|`0 calc(var(--k-space-1) * 6.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`0 26px 22px`|1|1 / 0|`0 calc(var(--k-space-1) * 6.5) calc(var(--k-space-1) * 5.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`0 2px`|1|1 / 0|`0 calc(var(--k-space-1) * 0.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`0 32px 0 12px`|1|1 / 0|`0 var(--k-space-8) 0 var(--k-space-3)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`0 5px`|1|1 / 0|`0 var(--k-space-step-03)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`0 7px`|1|1 / 0|`0 var(--k-space-step-02)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`0 7px 0 12px`|1|1 / 0|`0 var(--k-space-step-02) 0 var(--k-space-3)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`10px 12px 150px`|1|1 / 0|`calc(var(--k-space-1) * 2.5) var(--k-space-3) calc(var(--k-space-1) * 37.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`10px 13px`|1|1 / 0|`calc(var(--k-space-1) * 2.5) var(--k-space-step-05)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`10px 18px 14px`|1|1 / 0|`calc(var(--k-space-1) * 2.5) calc(var(--k-space-1) * 4.5) calc(var(--k-space-1) * 3.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`10px 2px`|1|1 / 0|`calc(var(--k-space-1) * 2.5) calc(var(--k-space-1) * 0.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`10px 6px 2px`|1|1 / 0|`calc(var(--k-space-1) * 2.5) calc(var(--k-space-1) * 1.5) calc(var(--k-space-1) * 0.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`11px`|1|1 / 0|`var(--k-space-step-04)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`11px 0`|1|1 / 0|`var(--k-space-step-04) 0`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`11px 12px`|1|1 / 0|`var(--k-space-step-04) var(--k-space-3)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`11px 13px`|1|1 / 0|`var(--k-space-step-04) var(--k-space-step-05)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`12px 13px`|1|1 / 0|`var(--k-space-3) var(--k-space-step-05)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`12px 15px`|1|1 / 0|`var(--k-space-3) var(--k-space-step-08)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`12px 24px`|1|0 / 1|`var(--k-space-3) var(--k-space-6)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`12px 26px`|1|0 / 1|`var(--k-space-3) calc(var(--k-space-1) * 6.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`13px`|1|1 / 0|`var(--k-space-step-05)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`13px 14px`|1|1 / 0|`var(--k-space-step-05) calc(var(--k-space-1) * 3.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`13px 15px`|1|1 / 0|`var(--k-space-step-05) var(--k-space-step-08)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`13px 16px`|1|1 / 0|`var(--k-space-step-05) var(--k-space-4)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`13px 27px`|1|0 / 1|`var(--k-space-step-05) var(--k-space-step-14)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`14px 10px`|1|1 / 0|`calc(var(--k-space-1) * 3.5) calc(var(--k-space-1) * 2.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`14px 16px`|1|1 / 0|`calc(var(--k-space-1) * 3.5) var(--k-space-4)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`14px 18px 18px`|1|1 / 0|`calc(var(--k-space-1) * 3.5) calc(var(--k-space-1) * 4.5) calc(var(--k-space-1) * 4.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`14px 6px`|1|1 / 0|`calc(var(--k-space-1) * 3.5) calc(var(--k-space-1) * 1.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`16px 18px 0`|1|1 / 0|`var(--k-space-4) calc(var(--k-space-1) * 4.5) 0`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`16px 20px`|1|1 / 0|`var(--k-space-4) calc(var(--k-space-1) * 5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`16px 3px 2px`|1|0 / 1|`var(--k-space-4) var(--k-space-step-06) calc(var(--k-space-1) * 0.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`16px 6px`|1|0 / 1|`var(--k-space-4) calc(var(--k-space-1) * 1.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`18px 14px`|1|1 / 0|`calc(var(--k-space-1) * 4.5) calc(var(--k-space-1) * 3.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`18px 28px 4px`|1|1 / 0|`calc(var(--k-space-1) * 4.5) calc(var(--k-space-1) * 7) var(--k-space-1)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`19px 20px`|1|1 / 0|`var(--k-space-step-15) calc(var(--k-space-1) * 5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`1px 7px`|1|1 / 0|`var(--k-space-step-07) var(--k-space-step-02)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`1px 8px`|1|1 / 0|`var(--k-space-step-07) var(--k-space-2)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`20px 0 16px`|1|0 / 1|`calc(var(--k-space-1) * 5) 0 var(--k-space-4)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`22px 10px`|1|1 / 0|`calc(var(--k-space-1) * 5.5) calc(var(--k-space-1) * 2.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`22px 20px`|1|1 / 0|`calc(var(--k-space-1) * 5.5) calc(var(--k-space-1) * 5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`22px 24px`|1|1 / 0|`calc(var(--k-space-1) * 5.5) var(--k-space-6)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`22px 24px 26px`|1|1 / 0|`calc(var(--k-space-1) * 5.5) var(--k-space-6) calc(var(--k-space-1) * 6.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`22px 28px 4px`|1|1 / 0|`calc(var(--k-space-1) * 5.5) calc(var(--k-space-1) * 7) var(--k-space-1)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`24px 18px`|1|1 / 0|`var(--k-space-6) calc(var(--k-space-1) * 4.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`26px 20px`|1|1 / 0|`calc(var(--k-space-1) * 6.5) calc(var(--k-space-1) * 5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`26px 22px`|1|0 / 1|`calc(var(--k-space-1) * 6.5) calc(var(--k-space-1) * 5.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`28px`|1|0 / 1|`calc(var(--k-space-1) * 7)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`28px 22px`|1|0 / 1|`calc(var(--k-space-1) * 7) calc(var(--k-space-1) * 5.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`2px 0 12px`|1|1 / 0|`calc(var(--k-space-1) * 0.5) 0 var(--k-space-3)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`2px 15px 15px`|1|1 / 0|`calc(var(--k-space-1) * 0.5) var(--k-space-step-08) var(--k-space-step-08)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`2px 6px 14px`|1|1 / 0|`calc(var(--k-space-1) * 0.5) calc(var(--k-space-1) * 1.5) calc(var(--k-space-1) * 3.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`2px 8px`|1|1 / 0|`calc(var(--k-space-1) * 0.5) var(--k-space-2)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`2px 8px 12px`|1|1 / 0|`calc(var(--k-space-1) * 0.5) var(--k-space-2) var(--k-space-3)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`2px 8px 14px`|1|1 / 0|`calc(var(--k-space-1) * 0.5) var(--k-space-2) calc(var(--k-space-1) * 3.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`3.5px 0`|1|1 / 0|`var(--k-space-step-16) 0`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`30px 28px`|1|1 / 0|`calc(var(--k-space-1) * 7.5) calc(var(--k-space-1) * 7)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`34px 24px`|1|0 / 1|`calc(var(--k-space-1) * 8.5) var(--k-space-6)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`36px 22px`|1|1 / 0|`calc(var(--k-space-1) * 9) calc(var(--k-space-1) * 5.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`36px 28px`|1|1 / 0|`calc(var(--k-space-1) * 9) calc(var(--k-space-1) * 7)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`3px 0 5px`|1|1 / 0|`var(--k-space-step-06) 0 var(--k-space-step-03)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`3px 6px 10px`|1|1 / 0|`var(--k-space-step-06) calc(var(--k-space-1) * 1.5) calc(var(--k-space-1) * 2.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`3px 9px`|1|0 / 1|`var(--k-space-step-06) var(--k-space-step-01)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`4.5px 7px`|1|1 / 0|`var(--k-space-step-17) var(--k-space-step-02)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`46px 26px 42px`|1|1 / 0|`calc(var(--k-space-1) * 11.5) calc(var(--k-space-1) * 6.5) calc(var(--k-space-1) * 10.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`4px 0`|1|1 / 0|`var(--k-space-1) 0`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`4px 11px`|1|0 / 1|`var(--k-space-1) var(--k-space-step-04)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`5px 0`|1|1 / 0|`var(--k-space-step-03) 0`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`5px 0 5px 11px`|1|1 / 0|`var(--k-space-step-03) 0 var(--k-space-step-03) var(--k-space-step-04)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`5px 10px`|1|1 / 0|`var(--k-space-step-03) calc(var(--k-space-1) * 2.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`5px 9px`|1|0 / 1|`var(--k-space-step-03) var(--k-space-step-01)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`6px 0`|1|1 / 0|`calc(var(--k-space-1) * 1.5) 0`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`6px 10px 3px`|1|1 / 0|`calc(var(--k-space-1) * 1.5) calc(var(--k-space-1) * 2.5) var(--k-space-step-06)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`6px 11px`|1|1 / 0|`calc(var(--k-space-1) * 1.5) var(--k-space-step-04)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`6px 13px`|1|0 / 1|`calc(var(--k-space-1) * 1.5) var(--k-space-step-05)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`6px 14px`|1|0 / 1|`calc(var(--k-space-1) * 1.5) calc(var(--k-space-1) * 3.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`6px 16px`|1|1 / 0|`calc(var(--k-space-1) * 1.5) var(--k-space-4)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`6px 2px`|1|1 / 0|`calc(var(--k-space-1) * 1.5) calc(var(--k-space-1) * 0.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`6px 8px`|1|1 / 0|`calc(var(--k-space-1) * 1.5) var(--k-space-2)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`6px 8px calc(6px + env(safe-area-inset-bottom))`|1|1 / 0|`calc(var(--k-space-1) * 1.5) var(--k-space-2) calc(calc(var(--k-space-1) * 1.5) + env(safe-area-inset-bottom))`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`7px 0`|1|1 / 0|`var(--k-space-step-02) 0`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`7px 10px`|1|1 / 0|`var(--k-space-step-02) calc(var(--k-space-1) * 2.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`7px 13px`|1|1 / 0|`var(--k-space-step-02) var(--k-space-step-05)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`7px 15px`|1|1 / 0|`var(--k-space-step-02) var(--k-space-step-08)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`8px`|1|1 / 0|`var(--k-space-2)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`8px 12px`|1|1 / 0|`var(--k-space-2) var(--k-space-3)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`8px 16px`|1|0 / 1|`var(--k-space-2) var(--k-space-4)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`8px 2px 0`|1|1 / 0|`var(--k-space-2) calc(var(--k-space-1) * 0.5) 0`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`9px 12px`|1|1 / 0|`var(--k-space-step-01) var(--k-space-3)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`9px 2px`|1|1 / 0|`var(--k-space-step-01) calc(var(--k-space-1) * 0.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding`|`9px 8px 0`|1|1 / 0|`var(--k-space-step-01) var(--k-space-2) 0`|同値。形状・計算結果を維持して置換候補にできる|
|`padding-bottom`|`.12em`|1|0 / 1|`var(--k-space-step-18)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding-bottom`|`26px`|1|1 / 0|`calc(var(--k-space-1) * 6.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding-inline-end`|`2px`|1|1 / 0|`calc(var(--k-space-1) * 0.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding-inline-end`|`4px`|1|1 / 0|`var(--k-space-1)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding-inline-start`|`12px`|1|1 / 0|`var(--k-space-3)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding-inline-start`|`16px`|1|1 / 0|`var(--k-space-4)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding-inline-start`|`19px`|1|1 / 0|`var(--k-space-step-15)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding-inline-start`|`22px`|1|1 / 0|`calc(var(--k-space-1) * 5.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding-inline-start`|`24px`|1|1 / 0|`var(--k-space-6)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding-inline-start`|`34px`|1|1 / 0|`calc(var(--k-space-1) * 8.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding-right`|`44px`|1|0 / 1|`calc(var(--k-space-1) * 11)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding-top`|`104px`|1|0 / 1|`calc(var(--k-space-1) * 26)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding-top`|`106px`|1|0 / 1|`calc(var(--k-space-1) * 26.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding-top`|`1px`|1|1 / 0|`var(--k-space-step-07)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding-top`|`22px`|1|1 / 0|`calc(var(--k-space-1) * 5.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding-top`|`30px`|1|1 / 0|`calc(var(--k-space-1) * 7.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`padding-top`|`6px`|1|1 / 0|`calc(var(--k-space-1) * 1.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`right`|`12px`|1|1 / 0|`var(--k-space-3)`|同値。形状・計算結果を維持して置換候補にできる|
|`right`|`18px`|1|1 / 0|`calc(var(--k-space-1) * 4.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`right`|`calc(50% + 16px)`|1|1 / 0|`calc(50% + var(--k-space-4))`|同値。形状・計算結果を維持して置換候補にできる|
|`right`|`calc(50% - 14px)`|1|1 / 0|`calc(50% - calc(var(--k-space-1) * 3.5))`|同値。形状・計算結果を維持して置換候補にできる|
|`top`|`10px`|1|0 / 1|`calc(var(--k-space-1) * 2.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`top`|`13px`|1|1 / 0|`var(--k-space-step-05)`|同値。形状・計算結果を維持して置換候補にできる|
|`top`|`5px`|1|1 / 0|`var(--k-space-step-03)`|同値。形状・計算結果を維持して置換候補にできる|
|`top`|`6px`|1|1 / 0|`calc(var(--k-space-1) * 1.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`top`|`calc(100% + 10px)`|1|1 / 0|`calc(100% + calc(var(--k-space-1) * 2.5))`|同値。形状・計算結果を維持して置換候補にできる|
|`top`|`calc(100% + 2px)`|1|1 / 0|`calc(100% + calc(var(--k-space-1) * 0.5))`|同値。形状・計算結果を維持して置換候補にできる|
|`top`|`calc(100% + 4px)`|1|1 / 0|`calc(100% + var(--k-space-1))`|同値。形状・計算結果を維持して置換候補にできる|
|`top`|`calc(100% + 6px)`|1|1 / 0|`calc(100% + calc(var(--k-space-1) * 1.5))`|同値。形状・計算結果を維持して置換候補にできる|
|`top`|`calc(100% + 7px)`|1|1 / 0|`calc(100% + var(--k-space-step-02))`|同値。形状・計算結果を維持して置換候補にできる|
|`top`|`calc(6px + var(--i) * 11px)`|1|0 / 1|`calc(calc(var(--k-space-1) * 1.5) + var(--i) * var(--k-space-step-04))`|同値。形状・計算結果を維持して置換候補にできる|

### font-size（533所見 / 35値）

| property | 生の値 | 回数 | UI / Lab | 置換候補 | 条件・理由 |
|---|---|---:|---|---|---|
|`font-size`|`12.5px`|104|82 / 22|`var(--k-text-sm)`|同値。形状・計算結果を維持して置換候補にできる|
|`font-size`|`13px`|92|76 / 16|`var(--k-text-sm)`|13px→12.5pxは近似、前後画像と判断が必要|
|`font-size`|`13.5px`|71|65 / 6|`var(--k-text-base)`|同値。形状・計算結果を維持して置換候補にできる|
|`font-size`|`12px`|51|44 / 7|`var(--k-text-sm)`|12px→12.5pxは近似、前後画像と判断が必要|
|`font-size`|`11px`|40|32 / 8|`var(--k-text-xs)`|同値。形状・計算結果を維持して置換候補にできる|
|`font-size`|`11.5px`|27|24 / 3|`var(--k-text-xs)`|11.5px→11pxは近似、前後画像と判断が必要|
|`font-size`|`14px`|24|22 / 2|`var(--k-text-base)`|14px→13.5pxは近似、前後画像と判断が必要|
|`font-size`|`15px`|21|14 / 7|`var(--k-text-step-01)`|同値。形状・計算結果を維持して置換候補にできる|
|`font-size`|`14.5px`|19|10 / 9|`var(--k-text-base)`|14.5px→13.5pxは近似、前後画像と判断が必要|
|`font-size`|`16px`|9|9 / 0|`var(--k-text-lg)`|16px→16.5pxは近似、前後画像と判断が必要|
|`font-size`|`19px`|9|5 / 4|`var(--k-text-xl)`|同値。形状・計算結果を維持して置換候補にできる|
|`font-size`|`15.5px`|6|6 / 0|`var(--k-text-lg)`|15.5px→16.5pxは近似、前後画像と判断が必要|
|`font-size`|`16.5px`|6|4 / 2|`var(--k-text-lg)`|同値。形状・計算結果を維持して置換候補にできる|
|`font-size`|`24px`|6|4 / 2|`var(--k-text-2xl)`|同値。形状・計算結果を維持して置換候補にできる|
|`font-size`|`10.5px`|5|5 / 0|`var(--k-text-xs)`|10.5px→11pxは近似、前後画像と判断が必要|
|`font-size`|`17px`|5|4 / 1|`var(--k-text-lg)`|17px→16.5pxは近似、前後画像と判断が必要|
|`font-size`|`21px`|5|3 / 2|`var(--k-text-step-02)`|同値。形状・計算結果を維持して置換候補にできる|
|`font-size`|`29px`|5|4 / 1|`var(--k-text-3xl)`|29px→30pxは近似、前後画像と判断が必要|
|`font-size`|`20px`|4|2 / 2|`var(--k-text-xl)`|20px→19pxは近似、前後画像と判断が必要|
|`font-size`|`30px`|3|0 / 3|`var(--k-text-3xl)`|同値。形状・計算結果を維持して置換候補にできる|
|`font-size`|`.86em`|2|2 / 0|`var(--k-text-step-03)`|同値。形状・計算結果を維持して置換候補にできる|
|`font-size`|`18.5px`|2|2 / 0|`var(--k-text-xl)`|18.5px→19pxは近似、前後画像と判断が必要|
|`font-size`|`18px`|2|2 / 0|`var(--k-text-xl)`|18px→19pxは近似、前後画像と判断が必要|
|`font-size`|`23px`|2|1 / 1|`var(--k-text-2xl)`|23px→24pxは近似、前後画像と判断が必要|
|`font-size`|`25px`|2|2 / 0|`var(--k-text-2xl)`|25px→24pxは近似、前後画像と判断が必要|
|`font-size`|`31px`|2|1 / 1|`var(--k-text-3xl)`|31px→30pxは近似、前後画像と判断が必要|
|`font-size`|`10px`|1|1 / 0|`var(--k-text-xs)`|10px→11pxは近似、前後画像と判断が必要|
|`font-size`|`19.5px`|1|1 / 0|`var(--k-text-xl)`|19.5px→19pxは近似、前後画像と判断が必要|
|`font-size`|`26px`|1|1 / 0|`var(--k-text-step-04)`|同値。形状・計算結果を維持して置換候補にできる|
|`font-size`|`27px`|1|1 / 0|`var(--k-text-step-05)`|同値。形状・計算結果を維持して置換候補にできる|
|`font-size`|`32px`|1|1 / 0|`var(--k-text-step-06)`|同値。形状・計算結果を維持して置換候補にできる|
|`font-size`|`41px`|1|1 / 0|`var(--k-text-step-07)`|同値。形状・計算結果を維持して置換候補にできる|
|`font-size`|`44px`|1|1 / 0|`var(--k-text-step-08)`|同値。形状・計算結果を維持して置換候補にできる|
|`font-size`|`9.5px`|1|1 / 0|`var(--k-text-step-09)`|同値。形状・計算結果を維持して置換候補にできる|
|`font-size`|`clamp(22px,4vw,30px)`|1|0 / 1|`clamp(var(--k-text-step-10),4vw,var(--k-text-3xl))`|同値。形状・計算結果を維持して置換候補にできる|

## 原子値の頻度（宣言内の長さ・時間・色）

前の件数は宣言数。以下は複合値の中の同じリテラルも合算した使用頻度で、宣言数433とは一致しない。例えば`5px 5px 0 0`は5pxが2回、1宣言。時間はmsへ正規化して`.18s`と`180ms`をまとめる。shadowはblur等の長さを役割抜きにまとめず、上の完全値表を使う。spacing/font-sizeは検査外の追加棚卸し。

### 原子値: radius

| 生の値 | 出現回数 | 含む宣言数 | UI / Lab（出現数） | 置換候補 | 条件 |
|---|---:|---:|---|---|---|
|`14px`|70|70|45 / 25|`var(--k-radius-step-01)`|同値。形状・計算結果を維持して置換候補にできる|
|`8px`|23|23|22 / 1|`var(--k-radius)`|同値。形状・計算結果を維持して置換候補にできる|
|`99px`|22|22|11 / 11|`var(--k-radius-full)`|同値。形状・計算結果を維持して置換候補にできる|
|`10px`|14|13|11 / 3|`var(--k-radius-step-03)`|同値。形状・計算結果を維持して置換候補にできる|
|`12px`|14|14|13 / 1|`var(--k-radius-lg)`|同値。形状・計算結果を維持して置換候補にできる|
|`16px`|14|14|12 / 2|`var(--k-radius-step-02)`|同値。形状・計算結果を維持して置換候補にできる|
|`11px`|13|13|9 / 4|`var(--k-radius-lg)`|11px→12pxは近似、前後画像と判断が必要|
|`7px`|13|13|12 / 1|`var(--k-radius-sm)`|7px→6pxは近似、前後画像と判断が必要|
|`13px`|12|12|6 / 6|`var(--k-radius-lg)`|13px→12pxは近似、前後画像と判断が必要|
|`9px`|8|8|8 / 0|`var(--k-radius)`|9px→8pxは近似、前後画像と判断が必要|
|`5px`|6|5|6 / 0|`var(--k-radius-sm)`|5px→6pxは近似、前後画像と判断が必要|
|`6px`|6|6|5 / 1|`var(--k-radius-sm)`|同値。形状・計算結果を維持して置換候補にできる|
|`2px`|5|5|2 / 3|`var(--k-radius-step-04)`|同値。形状・計算結果を維持して置換候補にできる|
|`3px`|5|5|5 / 0|`var(--k-radius-step-05)`|同値。形状・計算結果を維持して置換候補にできる|
|`18px`|3|3|2 / 1|`var(--k-radius-step-06)`|同値。形状・計算結果を維持して置換候補にできる|
|`2.5px`|3|3|3 / 0|`var(--k-radius-step-07)`|同値。形状・計算結果を維持して置換候補にできる|
|`4px`|2|2|1 / 1|`var(--k-radius-step-08)`|同値。形状・計算結果を維持して置換候補にできる|
|`12.5px`|1|1|0 / 1|`var(--k-radius-lg)`|12.5px→12pxは近似、前後画像と判断が必要|
|`20px`|1|1|0 / 1|`var(--k-radius-step-09)`|同値。形状・計算結果を維持して置換候補にできる|
|`9.5px`|1|1|0 / 1|`var(--k-radius-step-10)`|同値。形状・計算結果を維持して置換候補にできる|

### 原子値: duration

| 生の値 | 出現回数 | 含む宣言数 | UI / Lab（出現数） | 置換候補 | 条件 |
|---|---:|---:|---|---|---|
|`150ms`|20|13|18 / 2|`var(--k-duration-01)`|Foundry倍率適用時はcalc(var(--k-duration-01) * var(--k-mscale, 1))。durationとdelayを区別する|
|`130ms`|12|7|12 / 0|`var(--k-dur-1)`|Foundry倍率適用時はcalc(var(--k-dur-1) * var(--k-mscale, 1))。durationとdelayを区別する|
|`180ms`|11|9|10 / 1|`var(--k-dur-2)`|Foundry倍率適用時はcalc(var(--k-dur-2) * var(--k-mscale, 1))。durationとdelayを区別する|
|`300ms`|8|7|2 / 6|`var(--k-duration-21)`|Foundry倍率適用時はcalc(var(--k-duration-21) * var(--k-mscale, 1))。durationとdelayを区別する|
|`120ms`|4|4|2 / 2|`var(--k-duration-29)`|Foundry倍率適用時はcalc(var(--k-duration-29) * var(--k-mscale, 1))。durationとdelayを区別する|
|`26000ms`|4|4|0 / 4|`var(--k-duration-04)`|Foundry倍率適用時はcalc(var(--k-duration-04) * var(--k-mscale, 1))。durationとdelayを区別する|
|`550ms`|4|4|1 / 3|`var(--k-duration-13)`|Foundry倍率適用時はcalc(var(--k-duration-13) * var(--k-mscale, 1))。durationとdelayを区別する|
|`450ms`|3|2|1 / 2|`var(--k-duration-23)`|Foundry倍率適用時はcalc(var(--k-duration-23) * var(--k-mscale, 1))。durationとdelayを区別する|
|`700ms`|3|3|1 / 2|`var(--k-duration-09)`|Foundry倍率適用時はcalc(var(--k-duration-09) * var(--k-mscale, 1))。durationとdelayを区別する|
|`140ms`|2|2|1 / 1|`var(--k-duration-26)`|Foundry倍率適用時はcalc(var(--k-duration-26) * var(--k-mscale, 1))。durationとdelayを区別する|
|`16000ms`|2|2|0 / 2|`var(--k-duration-03)`|Foundry倍率適用時はcalc(var(--k-duration-03) * var(--k-mscale, 1))。durationとdelayを区別する|
|`160ms`|2|1|2 / 0|`var(--k-duration-30)`|Foundry倍率適用時はcalc(var(--k-duration-30) * var(--k-mscale, 1))。durationとdelayを区別する|
|`200ms`|2|2|2 / 0|`var(--k-duration-33)`|Foundry倍率適用時はcalc(var(--k-duration-33) * var(--k-mscale, 1))。durationとdelayを区別する|
|`220ms`|2|1|2 / 0|`var(--k-dur-3)`|Foundry倍率適用時はcalc(var(--k-dur-3) * var(--k-mscale, 1))。durationとdelayを区別する|
|`2400ms`|2|2|0 / 2|`var(--k-duration-12)`|Foundry倍率適用時はcalc(var(--k-duration-12) * var(--k-mscale, 1))。durationとdelayを区別する|
|`250ms`|2|2|0 / 2|`var(--k-duration-27)`|Foundry倍率適用時はcalc(var(--k-duration-27) * var(--k-mscale, 1))。durationとdelayを区別する|
|`3400ms`|2|2|0 / 2|`var(--k-duration-10)`|Foundry倍率適用時はcalc(var(--k-duration-10) * var(--k-mscale, 1))。durationとdelayを区別する|
|`3600ms`|2|2|0 / 2|`var(--k-duration-02)`|Foundry倍率適用時はcalc(var(--k-duration-02) * var(--k-mscale, 1))。durationとdelayを区別する|
|`500ms`|2|2|2 / 0|`var(--k-duration-18)`|Foundry倍率適用時はcalc(var(--k-duration-18) * var(--k-mscale, 1))。durationとdelayを区別する|
|`1000ms`|1|1|1 / 0|`var(--k-duration-20)`|Foundry倍率適用時はcalc(var(--k-duration-20) * var(--k-mscale, 1))。durationとdelayを区別する|
|`1050ms`|1|1|0 / 1|`var(--k-duration-22)`|Foundry倍率適用時はcalc(var(--k-duration-22) * var(--k-mscale, 1))。durationとdelayを区別する|
|`11000ms`|1|1|0 / 1|`var(--k-duration-07)`|Foundry倍率適用時はcalc(var(--k-duration-07) * var(--k-mscale, 1))。durationとdelayを区別する|
|`12000ms`|1|1|0 / 1|`var(--k-duration-06)`|Foundry倍率適用時はcalc(var(--k-duration-06) * var(--k-mscale, 1))。durationとdelayを区別する|
|`1400ms`|1|1|1 / 0|`var(--k-duration-19)`|Foundry倍率適用時はcalc(var(--k-duration-19) * var(--k-mscale, 1))。durationとdelayを区別する|
|`1600ms`|1|1|1 / 0|`var(--k-duration-25)`|Foundry倍率適用時はcalc(var(--k-duration-25) * var(--k-mscale, 1))。durationとdelayを区別する|
|`2200ms`|1|1|0 / 1|`var(--k-duration-11)`|Foundry倍率適用時はcalc(var(--k-duration-11) * var(--k-mscale, 1))。durationとdelayを区別する|
|`280ms`|1|1|0 / 1|`var(--k-duration-32)`|Foundry倍率適用時はcalc(var(--k-duration-32) * var(--k-mscale, 1))。durationとdelayを区別する|
|`30000ms`|1|1|0 / 1|`var(--k-duration-14)`|Foundry倍率適用時はcalc(var(--k-duration-14) * var(--k-mscale, 1))。durationとdelayを区別する|
|`340ms`|1|1|0 / 1|`var(--k-duration-34)`|Foundry倍率適用時はcalc(var(--k-duration-34) * var(--k-mscale, 1))。durationとdelayを区別する|
|`350ms`|1|1|0 / 1|`var(--k-duration-35)`|Foundry倍率適用時はcalc(var(--k-duration-35) * var(--k-mscale, 1))。durationとdelayを区別する|
|`400ms`|1|1|0 / 1|`var(--k-duration-28)`|Foundry倍率適用時はcalc(var(--k-duration-28) * var(--k-mscale, 1))。durationとdelayを区別する|
|`4500ms`|1|1|0 / 1|`var(--k-duration-08)`|Foundry倍率適用時はcalc(var(--k-duration-08) * var(--k-mscale, 1))。durationとdelayを区別する|
|`5000ms`|1|1|0 / 1|`var(--k-duration-24)`|Foundry倍率適用時はcalc(var(--k-duration-24) * var(--k-mscale, 1))。durationとdelayを区別する|
|`5200ms`|1|1|1 / 0|`var(--k-duration-15)`|Foundry倍率適用時はcalc(var(--k-duration-15) * var(--k-mscale, 1))。durationとdelayを区別する|
|`5800ms`|1|1|1 / 0|`var(--k-duration-16)`|Foundry倍率適用時はcalc(var(--k-duration-16) * var(--k-mscale, 1))。durationとdelayを区別する|
|`6400ms`|1|1|1 / 0|`var(--k-duration-17)`|Foundry倍率適用時はcalc(var(--k-duration-17) * var(--k-mscale, 1))。durationとdelayを区別する|
|`650ms`|1|1|0 / 1|`var(--k-duration-36)`|Foundry倍率適用時はcalc(var(--k-duration-36) * var(--k-mscale, 1))。durationとdelayを区別する|
|`80ms`|1|1|0 / 1|`var(--k-duration-31)`|Foundry倍率適用時はcalc(var(--k-duration-31) * var(--k-mscale, 1))。durationとdelayを区別する|
|`9000ms`|1|1|0 / 1|`var(--k-duration-05)`|Foundry倍率適用時はcalc(var(--k-duration-05) * var(--k-mscale, 1))。durationとdelayを区別する|

### 原子値: color / paint

| 生の値 | 出現回数 | 含む宣言数 | UI / Lab（出現数） | 置換候補 | 条件 |
|---|---:|---:|---|---|---|
|`rgba(24,24,27,.45)`|4|4|4 / 0|`完全値表のpaint候補を参照`|色の役割を確認。gradient内の混色・位置を維持|
|`hsl(205 90% 63%)`|3|3|0 / 3|`完全値表のpaint候補を参照`|色の役割を確認。gradient内の混色・位置を維持|
|`hsl(335 85% 68%)`|3|3|0 / 3|`完全値表のpaint候補を参照`|色の役割を確認。gradient内の混色・位置を維持|
|`hsl(32 95% 60%)`|2|2|0 / 2|`完全値表のpaint候補を参照`|色の役割を確認。gradient内の混色・位置を維持|
|`#fff`|1|1|1 / 0|`完全値表のpaint候補を参照`|色の役割を確認。gradient内の混色・位置を維持|
|`hsl(0 0% 11%)`|1|1|1 / 0|`完全値表のpaint候補を参照`|色の役割を確認。gradient内の混色・位置を維持|
|`hsl(152 30% 52%)`|1|1|1 / 0|`完全値表のpaint候補を参照`|色の役割を確認。gradient内の混色・位置を維持|
|`hsl(175 84% 32%)`|1|1|1 / 0|`完全値表のpaint候補を参照`|色の役割を確認。gradient内の混色・位置を維持|
|`hsl(190 59% 46%)`|1|1|1 / 0|`完全値表のpaint候補を参照`|色の役割を確認。gradient内の混色・位置を維持|
|`hsl(199 65% 60%)`|1|1|1 / 0|`完全値表のpaint候補を参照`|色の役割を確認。gradient内の混色・位置を維持|
|`hsl(205 90% 66%)`|1|1|0 / 1|`完全値表のpaint候補を参照`|色の役割を確認。gradient内の混色・位置を維持|
|`hsl(216 68% 38%)`|1|1|1 / 0|`完全値表のpaint候補を参照`|色の役割を確認。gradient内の混色・位置を維持|
|`hsl(265 27% 46%)`|1|1|1 / 0|`完全値表のpaint候補を参照`|色の役割を確認。gradient内の混色・位置を維持|
|`hsl(32 95% 64%)`|1|1|0 / 1|`完全値表のpaint候補を参照`|色の役割を確認。gradient内の混色・位置を維持|
|`hsl(335 85% 72%)`|1|1|0 / 1|`完全値表のpaint候補を参照`|色の役割を確認。gradient内の混色・位置を維持|
|`hsl(346 39% 38%)`|1|1|1 / 0|`完全値表のpaint候補を参照`|色の役割を確認。gradient内の混色・位置を維持|
|`hsl(41 100% 55%)`|1|1|1 / 0|`完全値表のpaint候補を参照`|色の役割を確認。gradient内の混色・位置を維持|
|`rgba(24,24,27,.72)`|1|1|0 / 1|`完全値表のpaint候補を参照`|色の役割を確認。gradient内の混色・位置を維持|
|`rgba(255,255,255,.05)`|1|1|0 / 1|`完全値表のpaint候補を参照`|色の役割を確認。gradient内の混色・位置を維持|
|`rgba(255,255,255,.14)`|1|1|0 / 1|`完全値表のpaint候補を参照`|色の役割を確認。gradient内の混色・位置を維持|
|`rgba(255,255,255,.16)`|1|1|1 / 0|`完全値表のpaint候補を参照`|色の役割を確認。gradient内の混色・位置を維持|
|`rgba(255,255,255,.17)`|1|1|0 / 1|`完全値表のpaint候補を参照`|色の役割を確認。gradient内の混色・位置を維持|
|`rgba(255,255,255,.3)`|1|1|0 / 1|`完全値表のpaint候補を参照`|色の役割を確認。gradient内の混色・位置を維持|
|`rgba(255,255,255,.75)`|1|1|0 / 1|`完全値表のpaint候補を参照`|色の役割を確認。gradient内の混色・位置を維持|

### 原子値: border

| 生の値 | 出現回数 | 含む宣言数 | UI / Lab（出現数） | 置換候補 | 条件 |
|---|---:|---:|---|---|---|
|`2px`|12|12|11 / 1|`calc(var(--k-space-1) * 0.5)`|px幅の同値換算。境界の意味を確認|
|`1.5px`|11|11|9 / 2|`calc(var(--k-space-1) * 0.375)`|px幅の同値換算。境界の意味を確認|
|`1px`|6|6|2 / 4|`1px`|px幅の同値換算。境界の意味を確認|
|`2.5px`|2|2|2 / 0|`calc(var(--k-space-1) * 0.625)`|px幅の同値換算。境界の意味を確認|
|`5px`|1|1|1 / 0|`calc(var(--k-space-1) * 1.25)`|px幅の同値換算。境界の意味を確認|

### 原子値: spacing

| 生の値 | 出現回数 | 含む宣言数 | UI / Lab（出現数） | 置換候補 | 条件 |
|---|---:|---:|---|---|---|
|`8px`|104|104|91 / 13|`var(--k-space-2)`|同値。形状・計算結果を維持して置換候補にできる|
|`9px`|99|99|79 / 20|`var(--k-space-step-01)`|同値。形状・計算結果を維持して置換候補にできる|
|`10px`|89|89|77 / 12|`calc(var(--k-space-1) * 2.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`14px`|79|79|72 / 7|`calc(var(--k-space-1) * 3.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`12px`|75|75|66 / 9|`var(--k-space-3)`|同値。形状・計算結果を維持して置換候補にできる|
|`16px`|71|71|61 / 10|`var(--k-space-4)`|同値。形状・計算結果を維持して置換候補にできる|
|`6px`|67|66|56 / 11|`calc(var(--k-space-1) * 1.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`7px`|59|59|51 / 8|`var(--k-space-step-02)`|同値。形状・計算結果を維持して置換候補にできる|
|`2px`|56|53|51 / 5|`calc(var(--k-space-1) * 0.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`5px`|52|51|46 / 6|`var(--k-space-step-03)`|同値。形状・計算結果を維持して置換候補にできる|
|`18px`|50|49|47 / 3|`calc(var(--k-space-1) * 4.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`4px`|41|41|31 / 10|`var(--k-space-1)`|同値。形状・計算結果を維持して置換候補にできる|
|`20px`|40|40|32 / 8|`calc(var(--k-space-1) * 5)`|同値。形状・計算結果を維持して置換候補にできる|
|`11px`|39|39|35 / 4|`var(--k-space-step-04)`|同値。形状・計算結果を維持して置換候補にできる|
|`13px`|36|36|27 / 9|`var(--k-space-step-05)`|同値。形状・計算結果を維持して置換候補にできる|
|`26px`|32|32|23 / 9|`calc(var(--k-space-1) * 6.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`22px`|30|30|25 / 5|`calc(var(--k-space-1) * 5.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`3px`|26|26|20 / 6|`var(--k-space-step-06)`|同値。形状・計算結果を維持して置換候補にできる|
|`15px`|19|18|18 / 1|`var(--k-space-step-08)`|同値。形状・計算結果を維持して置換候補にできる|
|`24px`|15|15|12 / 3|`var(--k-space-6)`|同値。形状・計算結果を維持して置換候補にできる|
|`1px`|14|14|14 / 0|`var(--k-space-step-07)`|同値。形状・計算結果を維持して置換候補にできる|
|`28px`|8|8|6 / 2|`calc(var(--k-space-1) * 7)`|同値。形状・計算結果を維持して置換候補にできる|
|`17px`|6|5|6 / 0|`var(--k-space-step-10)`|同値。形状・計算結果を維持して置換候補にできる|
|`30px`|5|5|4 / 1|`calc(var(--k-space-1) * 7.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`34px`|4|4|3 / 1|`calc(var(--k-space-1) * 8.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`42px`|3|3|3 / 0|`calc(var(--k-space-1) * 10.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`44px`|3|3|1 / 2|`calc(var(--k-space-1) * 11)`|同値。形状・計算結果を維持して置換候補にできる|
|`1.5px`|2|2|0 / 2|`var(--k-space-step-09)`|同値。形状・計算結果を維持して置換候補にできる|
|`19px`|2|2|2 / 0|`var(--k-space-step-15)`|同値。形状・計算結果を維持して置換候補にできる|
|`36px`|2|2|2 / 0|`calc(var(--k-space-1) * 9)`|同値。形状・計算結果を維持して置換候補にできる|
|`78px`|2|2|2 / 0|`calc(var(--k-space-1) * 19.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`-.12em`|1|1|0 / 1|`var(--k-space-step-12)`|同値。形状・計算結果を維持して置換候補にできる|
|`.12em`|1|1|0 / 1|`var(--k-space-step-18)`|同値。形状・計算結果を維持して置換候補にできる|
|`104px`|1|1|0 / 1|`calc(var(--k-space-1) * 26)`|同値。形状・計算結果を維持して置換候補にできる|
|`106px`|1|1|0 / 1|`calc(var(--k-space-1) * 26.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`118px`|1|1|1 / 0|`calc(var(--k-space-1) * 29.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`120px`|1|1|1 / 0|`calc(var(--k-space-1) * 30)`|同値。形状・計算結果を維持して置換候補にできる|
|`150px`|1|1|1 / 0|`calc(var(--k-space-1) * 37.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`25px`|1|1|1 / 0|`var(--k-space-step-11)`|同値。形状・計算結果を維持して置換候補にできる|
|`27px`|1|1|0 / 1|`var(--k-space-step-14)`|同値。形状・計算結果を維持して置換候補にできる|
|`3.5px`|1|1|1 / 0|`var(--k-space-step-16)`|同値。形状・計算結果を維持して置換候補にできる|
|`32px`|1|1|1 / 0|`var(--k-space-8)`|同値。形状・計算結果を維持して置換候補にできる|
|`4.5px`|1|1|1 / 0|`var(--k-space-step-17)`|同値。形状・計算結果を維持して置換候補にできる|
|`41px`|1|1|1 / 0|`var(--k-space-step-13)`|同値。形状・計算結果を維持して置換候補にできる|
|`46px`|1|1|1 / 0|`calc(var(--k-space-1) * 11.5)`|同値。形状・計算結果を維持して置換候補にできる|
|`96px`|1|1|1 / 0|`calc(var(--k-space-1) * 24)`|同値。形状・計算結果を維持して置換候補にできる|

### 原子値: font-size

| 生の値 | 出現回数 | 含む宣言数 | UI / Lab（出現数） | 置換候補 | 条件 |
|---|---:|---:|---|---|---|
|`12.5px`|104|104|82 / 22|`var(--k-text-sm)`|同値。形状・計算結果を維持して置換候補にできる|
|`13px`|92|92|76 / 16|`var(--k-text-sm)`|13px→12.5pxは近似、前後画像と判断が必要|
|`13.5px`|71|71|65 / 6|`var(--k-text-base)`|同値。形状・計算結果を維持して置換候補にできる|
|`12px`|51|51|44 / 7|`var(--k-text-sm)`|12px→12.5pxは近似、前後画像と判断が必要|
|`11px`|40|40|32 / 8|`var(--k-text-xs)`|同値。形状・計算結果を維持して置換候補にできる|
|`11.5px`|27|27|24 / 3|`var(--k-text-xs)`|11.5px→11pxは近似、前後画像と判断が必要|
|`14px`|24|24|22 / 2|`var(--k-text-base)`|14px→13.5pxは近似、前後画像と判断が必要|
|`15px`|21|21|14 / 7|`var(--k-text-step-01)`|同値。形状・計算結果を維持して置換候補にできる|
|`14.5px`|19|19|10 / 9|`var(--k-text-base)`|14.5px→13.5pxは近似、前後画像と判断が必要|
|`16px`|9|9|9 / 0|`var(--k-text-lg)`|16px→16.5pxは近似、前後画像と判断が必要|
|`19px`|9|9|5 / 4|`var(--k-text-xl)`|同値。形状・計算結果を維持して置換候補にできる|
|`15.5px`|6|6|6 / 0|`var(--k-text-lg)`|15.5px→16.5pxは近似、前後画像と判断が必要|
|`16.5px`|6|6|4 / 2|`var(--k-text-lg)`|同値。形状・計算結果を維持して置換候補にできる|
|`24px`|6|6|4 / 2|`var(--k-text-2xl)`|同値。形状・計算結果を維持して置換候補にできる|
|`10.5px`|5|5|5 / 0|`var(--k-text-xs)`|10.5px→11pxは近似、前後画像と判断が必要|
|`17px`|5|5|4 / 1|`var(--k-text-lg)`|17px→16.5pxは近似、前後画像と判断が必要|
|`21px`|5|5|3 / 2|`var(--k-text-step-02)`|同値。形状・計算結果を維持して置換候補にできる|
|`29px`|5|5|4 / 1|`var(--k-text-3xl)`|29px→30pxは近似、前後画像と判断が必要|
|`20px`|4|4|2 / 2|`var(--k-text-xl)`|20px→19pxは近似、前後画像と判断が必要|
|`30px`|4|4|0 / 4|`var(--k-text-3xl)`|同値。形状・計算結果を維持して置換候補にできる|
|`.86em`|2|2|2 / 0|`var(--k-text-step-03)`|同値。形状・計算結果を維持して置換候補にできる|
|`18.5px`|2|2|2 / 0|`var(--k-text-xl)`|18.5px→19pxは近似、前後画像と判断が必要|
|`18px`|2|2|2 / 0|`var(--k-text-xl)`|18px→19pxは近似、前後画像と判断が必要|
|`23px`|2|2|1 / 1|`var(--k-text-2xl)`|23px→24pxは近似、前後画像と判断が必要|
|`25px`|2|2|2 / 0|`var(--k-text-2xl)`|25px→24pxは近似、前後画像と判断が必要|
|`31px`|2|2|1 / 1|`var(--k-text-3xl)`|31px→30pxは近似、前後画像と判断が必要|
|`10px`|1|1|1 / 0|`var(--k-text-xs)`|10px→11pxは近似、前後画像と判断が必要|
|`19.5px`|1|1|1 / 0|`var(--k-text-xl)`|19.5px→19pxは近似、前後画像と判断が必要|
|`22px`|1|1|0 / 1|`var(--k-text-step-10)`|同値。形状・計算結果を維持して置換候補にできる|
|`26px`|1|1|1 / 0|`var(--k-text-step-04)`|同値。形状・計算結果を維持して置換候補にできる|
|`27px`|1|1|1 / 0|`var(--k-text-step-05)`|同値。形状・計算結果を維持して置換候補にできる|
|`32px`|1|1|1 / 0|`var(--k-text-step-06)`|同値。形状・計算結果を維持して置換候補にできる|
|`41px`|1|1|1 / 0|`var(--k-text-step-07)`|同値。形状・計算結果を維持して置換候補にできる|
|`44px`|1|1|1 / 0|`var(--k-text-step-08)`|同値。形状・計算結果を維持して置換候補にできる|
|`9.5px`|1|1|1 / 0|`var(--k-text-step-09)`|同値。形状・計算結果を維持して置換候補にできる|

## 新しい共通トークンの追加案（未実装）

上の表から参照する候補の完全な定義。名前に部品名を使わず、現在の値を保持する案。単発値をすべて追加すると共通スケールが肥大化するため、採用前に下記の手順で共通性を判断する。

| 候補名 | 値 | 理由 |
|---|---|---|
|`--k-radius-step-01`|`14px`|既存の同値CSSトークンなし。値を維持する共通候補。|
|`--k-radius-step-02`|`16px`|既存の同値CSSトークンなし。値を維持する共通候補。|
|`--k-radius-step-03`|`10px`|既存の同値CSSトークンなし。値を維持する共通候補。|
|`--k-radius-step-04`|`2px`|既存の同値CSSトークンなし。値を維持する共通候補。|
|`--k-radius-step-05`|`3px`|既存の同値CSSトークンなし。値を維持する共通候補。|
|`--k-radius-step-06`|`18px`|既存の同値CSSトークンなし。値を維持する共通候補。|
|`--k-radius-step-07`|`2.5px`|既存の同値CSSトークンなし。値を維持する共通候補。|
|`--k-radius-step-08`|`4px`|既存の同値CSSトークンなし。値を維持する共通候補。|
|`--k-radius-step-09`|`20px`|既存の同値CSSトークンなし。値を維持する共通候補。|
|`--k-radius-step-10`|`9.5px`|既存の同値CSSトークンなし。値を維持する共通候補。|
|`--k-duration-01`|`150ms`|既存の同値CSSトークンなし。値を維持する共通候補。UIの短い反応とLabの長いループを別の用途として扱う。|
|`--k-duration-02`|`3600ms`|既存の同値CSSトークンなし。値を維持する共通候補。UIの短い反応とLabの長いループを別の用途として扱う。|
|`--k-duration-03`|`16000ms`|既存の同値CSSトークンなし。値を維持する共通候補。UIの短い反応とLabの長いループを別の用途として扱う。|
|`--k-duration-04`|`26000ms`|既存の同値CSSトークンなし。値を維持する共通候補。UIの短い反応とLabの長いループを別の用途として扱う。|
|`--k-duration-05`|`9000ms`|既存の同値CSSトークンなし。値を維持する共通候補。UIの短い反応とLabの長いループを別の用途として扱う。|
|`--k-duration-06`|`12000ms`|既存の同値CSSトークンなし。値を維持する共通候補。UIの短い反応とLabの長いループを別の用途として扱う。|
|`--k-duration-07`|`11000ms`|既存の同値CSSトークンなし。値を維持する共通候補。UIの短い反応とLabの長いループを別の用途として扱う。|
|`--k-duration-08`|`4500ms`|既存の同値CSSトークンなし。値を維持する共通候補。UIの短い反応とLabの長いループを別の用途として扱う。|
|`--k-duration-09`|`700ms`|既存の同値CSSトークンなし。値を維持する共通候補。UIの短い反応とLabの長いループを別の用途として扱う。|
|`--k-duration-10`|`3400ms`|既存の同値CSSトークンなし。値を維持する共通候補。UIの短い反応とLabの長いループを別の用途として扱う。|
|`--k-duration-11`|`2200ms`|既存の同値CSSトークンなし。値を維持する共通候補。UIの短い反応とLabの長いループを別の用途として扱う。|
|`--k-duration-12`|`2400ms`|既存の同値CSSトークンなし。値を維持する共通候補。UIの短い反応とLabの長いループを別の用途として扱う。|
|`--k-duration-13`|`550ms`|既存の同値CSSトークンなし。値を維持する共通候補。UIの短い反応とLabの長いループを別の用途として扱う。|
|`--k-duration-14`|`30000ms`|既存の同値CSSトークンなし。値を維持する共通候補。UIの短い反応とLabの長いループを別の用途として扱う。|
|`--k-duration-15`|`5200ms`|既存の同値CSSトークンなし。値を維持する共通候補。UIの短い反応とLabの長いループを別の用途として扱う。|
|`--k-duration-16`|`5800ms`|既存の同値CSSトークンなし。値を維持する共通候補。UIの短い反応とLabの長いループを別の用途として扱う。|
|`--k-duration-17`|`6400ms`|既存の同値CSSトークンなし。値を維持する共通候補。UIの短い反応とLabの長いループを別の用途として扱う。|
|`--k-duration-18`|`500ms`|既存の同値CSSトークンなし。値を維持する共通候補。UIの短い反応とLabの長いループを別の用途として扱う。|
|`--k-duration-19`|`1400ms`|既存の同値CSSトークンなし。値を維持する共通候補。UIの短い反応とLabの長いループを別の用途として扱う。|
|`--k-duration-20`|`1000ms`|既存の同値CSSトークンなし。値を維持する共通候補。UIの短い反応とLabの長いループを別の用途として扱う。|
|`--k-duration-21`|`300ms`|既存の同値CSSトークンなし。値を維持する共通候補。UIの短い反応とLabの長いループを別の用途として扱う。|
|`--k-duration-22`|`1050ms`|既存の同値CSSトークンなし。値を維持する共通候補。UIの短い反応とLabの長いループを別の用途として扱う。|
|`--k-duration-23`|`450ms`|既存の同値CSSトークンなし。値を維持する共通候補。UIの短い反応とLabの長いループを別の用途として扱う。|
|`--k-duration-24`|`5000ms`|既存の同値CSSトークンなし。値を維持する共通候補。UIの短い反応とLabの長いループを別の用途として扱う。|
|`--k-duration-25`|`1600ms`|既存の同値CSSトークンなし。値を維持する共通候補。UIの短い反応とLabの長いループを別の用途として扱う。|
|`--k-duration-26`|`140ms`|既存の同値CSSトークンなし。値を維持する共通候補。UIの短い反応とLabの長いループを別の用途として扱う。|
|`--k-duration-27`|`250ms`|既存の同値CSSトークンなし。値を維持する共通候補。UIの短い反応とLabの長いループを別の用途として扱う。|
|`--k-duration-28`|`400ms`|既存の同値CSSトークンなし。値を維持する共通候補。UIの短い反応とLabの長いループを別の用途として扱う。|
|`--k-duration-29`|`120ms`|既存の同値CSSトークンなし。値を維持する共通候補。UIの短い反応とLabの長いループを別の用途として扱う。|
|`--k-duration-30`|`160ms`|既存の同値CSSトークンなし。値を維持する共通候補。UIの短い反応とLabの長いループを別の用途として扱う。|
|`--k-duration-31`|`80ms`|既存の同値CSSトークンなし。値を維持する共通候補。UIの短い反応とLabの長いループを別の用途として扱う。|
|`--k-duration-32`|`280ms`|既存の同値CSSトークンなし。値を維持する共通候補。UIの短い反応とLabの長いループを別の用途として扱う。|
|`--k-duration-33`|`200ms`|既存の同値CSSトークンなし。値を維持する共通候補。UIの短い反応とLabの長いループを別の用途として扱う。|
|`--k-duration-34`|`340ms`|既存の同値CSSトークンなし。値を維持する共通候補。UIの短い反応とLabの長いループを別の用途として扱う。|
|`--k-duration-35`|`350ms`|既存の同値CSSトークンなし。値を維持する共通候補。UIの短い反応とLabの長いループを別の用途として扱う。|
|`--k-duration-36`|`650ms`|既存の同値CSSトークンなし。値を維持する共通候補。UIの短い反応とLabの長いループを別の用途として扱う。|
|`--k-shadow-level-01`|`0 20px 44px -14px rgba(16,24,40,.22)`|既存の同値CSSトークンなし。値を維持する共通候補。offset/blur/spread/alphaを丸めず保持。|
|`--k-shadow-level-02`|`0 0 0 3px var(--k-accent-bg)`|既存の同値CSSトークンなし。値を維持する共通候補。offset/blur/spread/alphaを丸めず保持。|
|`--k-shadow-level-03`|`0 1px 2px rgba(16,24,40,.18)`|既存の同値CSSトークンなし。値を維持する共通候補。offset/blur/spread/alphaを丸めず保持。|
|`--k-shadow-level-04`|`0 1px 4px rgba(16,24,40,.18)`|既存の同値CSSトークンなし。値を維持する共通候補。offset/blur/spread/alphaを丸めず保持。|
|`--k-shadow-level-05`|`0 30px 80px -20px rgba(0,0,0,.4)`|既存の同値CSSトークンなし。値を維持する共通候補。offset/blur/spread/alphaを丸めず保持。|
|`--k-shadow-level-06`|`-24px 0 60px -24px rgba(0,0,0,.35)`|既存の同値CSSトークンなし。値を維持する共通候補。offset/blur/spread/alphaを丸めず保持。|
|`--k-shadow-level-07`|`0 0 0 1px rgba(24,24,27,.25)`|既存の同値CSSトークンなし。値を維持する共通候補。offset/blur/spread/alphaを丸めず保持。|
|`--k-shadow-level-08`|`0 0 0 1px var(--k-line)`|既存の同値CSSトークンなし。値を維持する共通候補。offset/blur/spread/alphaを丸めず保持。|
|`--k-shadow-level-09`|`0 0 0 2px var(--k-accent)`|既存の同値CSSトークンなし。値を維持する共通候補。offset/blur/spread/alphaを丸めず保持。|
|`--k-shadow-level-10`|`0 0 0 2px var(--k-bg),0 0 0 4px var(--k-accent)`|既存の同値CSSトークンなし。値を維持する共通候補。offset/blur/spread/alphaを丸めず保持。|
|`--k-shadow-level-11`|`0 0 0 2px var(--k-ink)`|既存の同値CSSトークンなし。値を維持する共通候補。offset/blur/spread/alphaを丸めず保持。|
|`--k-shadow-level-12`|`0 0 0 4px var(--k-accent-bg)`|既存の同値CSSトークンなし。値を維持する共通候補。offset/blur/spread/alphaを丸めず保持。|
|`--k-shadow-level-13`|`0 0 0 5px var(--k-accent-bg-strong)`|既存の同値CSSトークンなし。値を維持する共通候補。offset/blur/spread/alphaを丸めず保持。|
|`--k-shadow-level-14`|`0 0 10px 2px rgba(255,255,255,.3)`|既存の同値CSSトークンなし。値を維持する共通候補。offset/blur/spread/alphaを丸めず保持。|
|`--k-shadow-level-15`|`0 0 18px -4px var(--k-accent-bg)`|既存の同値CSSトークンなし。値を維持する共通候補。offset/blur/spread/alphaを丸めず保持。|
|`--k-shadow-level-16`|`0 0 26px -6px var(--k-accent)`|既存の同値CSSトークンなし。値を維持する共通候補。offset/blur/spread/alphaを丸めず保持。|
|`--k-shadow-level-17`|`0 0 46px color-mix(in srgb,var(--k-accent) 45%,transparent)`|既存の同値CSSトークンなし。値を維持する共通候補。offset/blur/spread/alphaを丸めず保持。|
|`--k-shadow-level-18`|`0 12px 26px -10px rgba(16,24,40,.4)`|既存の同値CSSトークンなし。値を維持する共通候補。offset/blur/spread/alphaを丸めず保持。|
|`--k-shadow-level-19`|`0 14px 28px -14px rgba(16,24,40,.28)`|既存の同値CSSトークンなし。値を維持する共通候補。offset/blur/spread/alphaを丸めず保持。|
|`--k-shadow-level-20`|`0 14px 34px -12px rgba(16,24,40,.25)`|既存の同値CSSトークンなし。値を維持する共通候補。offset/blur/spread/alphaを丸めず保持。|
|`--k-shadow-level-21`|`0 16px 40px -12px rgba(16,24,40,.18)`|既存の同値CSSトークンなし。値を維持する共通候補。offset/blur/spread/alphaを丸めず保持。|
|`--k-shadow-level-22`|`0 16px 40px -14px rgba(16,24,40,.25)`|既存の同値CSSトークンなし。値を維持する共通候補。offset/blur/spread/alphaを丸めず保持。|
|`--k-shadow-level-23`|`0 18px 40px -12px rgba(16,24,40,.25)`|既存の同値CSSトークンなし。値を維持する共通候補。offset/blur/spread/alphaを丸めず保持。|
|`--k-shadow-level-24`|`0 18px 40px -18px rgba(0,0,0,.45)`|既存の同値CSSトークンなし。値を維持する共通候補。offset/blur/spread/alphaを丸めず保持。|
|`--k-shadow-level-25`|`0 1px 2px rgba(16,24,40,.04)`|既存の同値CSSトークンなし。値を維持する共通候補。offset/blur/spread/alphaを丸めず保持。|
|`--k-shadow-level-26`|`0 1px 2px rgba(16,24,40,.05)`|既存の同値CSSトークンなし。値を維持する共通候補。offset/blur/spread/alphaを丸めず保持。|
|`--k-shadow-level-27`|`0 1px 2px rgba(16,24,40,.09)`|既存の同値CSSトークンなし。値を維持する共通候補。offset/blur/spread/alphaを丸めず保持。|
|`--k-shadow-level-28`|`0 1px 3px rgba(0,0,0,.3),inset 0 0 0 1px rgba(0,0,0,.08)`|既存の同値CSSトークンなし。値を維持する共通候補。offset/blur/spread/alphaを丸めず保持。|
|`--k-shadow-level-29`|`0 1px 3px rgba(16,24,40,.14)`|既存の同値CSSトークンなし。値を維持する共通候補。offset/blur/spread/alphaを丸めず保持。|
|`--k-shadow-level-30`|`0 20px 44px -12px rgba(16,24,40,.28)`|既存の同値CSSトークンなし。値を維持する共通候補。offset/blur/spread/alphaを丸めず保持。|
|`--k-shadow-level-31`|`0 20px 44px -14px rgba(0,0,0,.45)`|既存の同値CSSトークンなし。値を維持する共通候補。offset/blur/spread/alphaを丸めず保持。|
|`--k-shadow-level-32`|`0 2px 10px rgba(16,24,40,.3)`|既存の同値CSSトークンなし。値を維持する共通候補。offset/blur/spread/alphaを丸めず保持。|
|`--k-shadow-level-33`|`0 2px 8px rgba(16,24,40,.08)`|既存の同値CSSトークンなし。値を維持する共通候補。offset/blur/spread/alphaを丸めず保持。|
|`--k-shadow-level-34`|`0 2px 8px rgba(16,24,40,.1)`|既存の同値CSSトークンなし。値を維持する共通候補。offset/blur/spread/alphaを丸めず保持。|
|`--k-shadow-level-35`|`0 30px 80px -20px rgba(0,0,0,.45)`|既存の同値CSSトークンなし。値を維持する共通候補。offset/blur/spread/alphaを丸めず保持。|
|`--k-shadow-level-36`|`0 3px 7px rgba(16,24,40,.25)`|既存の同値CSSトークンなし。値を維持する共通候補。offset/blur/spread/alphaを丸めず保持。|
|`--k-shadow-level-37`|`0 4px 12px rgba(16,24,40,.1)`|既存の同値CSSトークンなし。値を維持する共通候補。offset/blur/spread/alphaを丸めず保持。|
|`--k-shadow-level-38`|`0 6px 18px rgba(16,24,40,.28)`|既存の同値CSSトークンなし。値を維持する共通候補。offset/blur/spread/alphaを丸めず保持。|
|`--k-paint-01`|`rgba(24,24,27,.45)`|既存の同値CSSトークンなし。値を維持する共通候補。背景に対するcontrastとdarkの再設計が必要。|
|`--k-paint-02`|`radial-gradient(circle at center,var(--k-core) 0 2.5px,var(--k-knob) 3.2px)`|既存の同値CSSトークンなし。値を維持する共通候補。背景に対するcontrastとdarkの再設計が必要。|
|`--k-paint-03`|`hsl(0 0% 11%)`|既存の同値CSSトークンなし。値を維持する共通候補。背景に対するcontrastとdarkの再設計が必要。|
|`--k-paint-04`|`hsl(152 30% 52%)`|既存の同値CSSトークンなし。値を維持する共通候補。背景に対するcontrastとdarkの再設計が必要。|
|`--k-paint-05`|`hsl(175 84% 32%)`|既存の同値CSSトークンなし。値を維持する共通候補。背景に対するcontrastとdarkの再設計が必要。|
|`--k-paint-06`|`hsl(190 59% 46%)`|既存の同値CSSトークンなし。値を維持する共通候補。背景に対するcontrastとdarkの再設計が必要。|
|`--k-paint-07`|`hsl(199 65% 60%)`|既存の同値CSSトークンなし。値を維持する共通候補。背景に対するcontrastとdarkの再設計が必要。|
|`--k-paint-08`|`hsl(216 68% 38%)`|既存の同値CSSトークンなし。値を維持する共通候補。背景に対するcontrastとdarkの再設計が必要。|
|`--k-paint-09`|`hsl(265 27% 46%)`|既存の同値CSSトークンなし。値を維持する共通候補。背景に対するcontrastとdarkの再設計が必要。|
|`--k-paint-10`|`hsl(346 39% 38%)`|既存の同値CSSトークンなし。値を維持する共通候補。背景に対するcontrastとdarkの再設計が必要。|
|`--k-paint-11`|`hsl(41 100% 55%)`|既存の同値CSSトークンなし。値を維持する共通候補。背景に対するcontrastとdarkの再設計が必要。|
|`--k-paint-12`|`linear-gradient(to right, rgba(255,255,255,.75), transparent)`|既存の同値CSSトークンなし。値を維持する共通候補。背景に対するcontrastとdarkの再設計が必要。|
|`--k-paint-13`|`radial-gradient(190px circle at var(--mx,50%) var(--my,50%), var(--k-accent), transparent 70%)`|既存の同値CSSトークンなし。値を維持する共通候補。背景に対するcontrastとdarkの再設計が必要。|
|`--k-paint-14`|`radial-gradient(200px circle at var(--mx) var(--my),rgba(255,255,255,.17),rgba(255,255,255,.05) 55%,transparent 72%)`|既存の同値CSSトークンなし。値を維持する共通候補。背景に対するcontrastとdarkの再設計が必要。|
|`--k-paint-15`|`radial-gradient(340px circle at var(--gx,50%) var(--gy,50%), rgba(255,255,255,.14), transparent 65%)`|既存の同値CSSトークンなし。値を維持する共通候補。背景に対するcontrastとdarkの再設計が必要。|
|`--k-paint-16`|`radial-gradient(circle at 38% 32%,color-mix(in srgb,hsl(335 85% 68%) 34%,transparent),transparent 62%),radial-gradient(circle at 66% 70%,color-mix(in srgb,hsl(205 90% 63%) 30%,transparent),transparent 62%),radial-gradient(circle,color-mix(in srgb,var(--k-accent) 42%,transparent),transparent 68%)`|既存の同値CSSトークンなし。値を維持する共通候補。背景に対するcontrastとdarkの再設計が必要。|
|`--k-paint-17`|`radial-gradient(circle at center,var(--k-core) 0 3px,var(--k-knob) 3.6px)`|既存の同値CSSトークンなし。値を維持する共通候補。背景に対するcontrastとdarkの再設計が必要。|
|`--k-paint-18`|`repeating-linear-gradient(90deg, var(--k-ink) 0 2px, transparent 2px 5px, var(--k-ink) 5px 6px, transparent 6px 10px, var(--k-ink) 10px 13px, transparent 13px 16px)`|既存の同値CSSトークンなし。値を維持する共通候補。背景に対するcontrastとdarkの再設計が必要。|
|`--k-paint-19`|`rgba(24,24,27,.72)`|既存の同値CSSトークンなし。値を維持する共通候補。背景に対するcontrastとdarkの再設計が必要。|
|`--k-paint-20`|`rgba(255,255,255,.16)`|既存の同値CSSトークンなし。値を維持する共通候補。背景に対するcontrastとdarkの再設計が必要。|
|`--k-paint-21`|`hsl(205 90% 66%)`|既存の同値CSSトークンなし。値を維持する共通候補。背景に対するcontrastとdarkの再設計が必要。|
|`--k-paint-22`|`hsl(32 95% 64%)`|既存の同値CSSトークンなし。値を維持する共通候補。背景に対するcontrastとdarkの再設計が必要。|
|`--k-paint-23`|`hsl(335 85% 72%)`|既存の同値CSSトークンなし。値を維持する共通候補。背景に対するcontrastとdarkの再設計が必要。|
|`--k-paint-24`|`rgba(255,255,255,.3)`|既存の同値CSSトークンなし。値を維持する共通候補。背景に対するcontrastとdarkの再設計が必要。|
|`--k-paint-25`|`hsl(205 90% 63%)`|既存の同値CSSトークンなし。値を維持する共通候補。背景に対するcontrastとdarkの再設計が必要。|
|`--k-paint-26`|`hsl(32 95% 60%)`|既存の同値CSSトークンなし。値を維持する共通候補。背景に対するcontrastとdarkの再設計が必要。|
|`--k-paint-27`|`hsl(335 85% 68%)`|既存の同値CSSトークンなし。値を維持する共通候補。背景に対するcontrastとdarkの再設計が必要。|
|`--k-border-treatment-01`|`1px solid color-mix(in srgb,var(--k-on-color) 18%,transparent)`|既存の同値CSSトークンなし。値を維持する共通候補。|
|`--k-border-treatment-02`|`1px solid color-mix(in srgb,var(--k-on-color) 25%,transparent)`|既存の同値CSSトークンなし。値を維持する共通候補。|
|`--k-border-treatment-03`|`1px solid color-mix(in srgb,var(--k-on-color) 28%,transparent)`|既存の同値CSSトークンなし。値を維持する共通候補。|
|`--k-border-treatment-04`|`1px solid color-mix(in srgb,var(--k-on-color) 32%,transparent)`|既存の同値CSSトークンなし。値を維持する共通候補。|
|`--k-space-step-01`|`9px`|既存の同値CSSトークンなし。値を維持する共通候補。|
|`--k-space-step-02`|`7px`|既存の同値CSSトークンなし。値を維持する共通候補。|
|`--k-space-step-03`|`5px`|既存の同値CSSトークンなし。値を維持する共通候補。|
|`--k-space-step-04`|`11px`|既存の同値CSSトークンなし。値を維持する共通候補。|
|`--k-space-step-05`|`13px`|既存の同値CSSトークンなし。値を維持する共通候補。|
|`--k-space-step-06`|`3px`|既存の同値CSSトークンなし。値を維持する共通候補。|
|`--k-space-step-07`|`1px`|既存の同値CSSトークンなし。値を維持する共通候補。|
|`--k-space-step-08`|`15px`|既存の同値CSSトークンなし。値を維持する共通候補。|
|`--k-space-step-09`|`1.5px`|既存の同値CSSトークンなし。値を維持する共通候補。|
|`--k-space-step-10`|`17px`|既存の同値CSSトークンなし。値を維持する共通候補。|
|`--k-space-step-11`|`25px`|既存の同値CSSトークンなし。値を維持する共通候補。|
|`--k-space-step-12`|`-.12em`|既存の同値CSSトークンなし。値を維持する共通候補。|
|`--k-space-step-13`|`41px`|既存の同値CSSトークンなし。値を維持する共通候補。|
|`--k-space-step-14`|`27px`|既存の同値CSSトークンなし。値を維持する共通候補。|
|`--k-space-step-15`|`19px`|既存の同値CSSトークンなし。値を維持する共通候補。|
|`--k-space-step-16`|`3.5px`|既存の同値CSSトークンなし。値を維持する共通候補。|
|`--k-space-step-17`|`4.5px`|既存の同値CSSトークンなし。値を維持する共通候補。|
|`--k-space-step-18`|`.12em`|既存の同値CSSトークンなし。値を維持する共通候補。|
|`--k-text-step-01`|`15px`|既存の同値CSSトークンなし。値を維持する共通候補。|
|`--k-text-step-02`|`21px`|既存の同値CSSトークンなし。値を維持する共通候補。|
|`--k-text-step-03`|`.86em`|既存の同値CSSトークンなし。値を維持する共通候補。|
|`--k-text-step-04`|`26px`|既存の同値CSSトークンなし。値を維持する共通候補。|
|`--k-text-step-05`|`27px`|既存の同値CSSトークンなし。値を維持する共通候補。|
|`--k-text-step-06`|`32px`|既存の同値CSSトークンなし。値を維持する共通候補。|
|`--k-text-step-07`|`41px`|既存の同値CSSトークンなし。値を維持する共通候補。|
|`--k-text-step-08`|`44px`|既存の同値CSSトークンなし。値を維持する共通候補。|
|`--k-text-step-09`|`9.5px`|既存の同値CSSトークンなし。値を維持する共通候補。|
|`--k-text-step-10`|`22px`|既存の同値CSSトークンなし。値を維持する共通候補。|

## 全対象の分類と所見件数

| 対象 | meta.category | 分類 | token-values所見 |
|---|---|---|---:|
|`blocks/app-shell`|Block|UI|2|
|`blocks/cookie-consent`|Block|UI|4|
|`blocks/cta-band`|Block|UI|2|
|`blocks/faq`|Block|UI|0|
|`blocks/filter-toolbar`|Block|UI|1|
|`blocks/integrations`|Block|UI|3|
|`blocks/invoice`|Block|UI|1|
|`blocks/kanban`|Block|UI|4|
|`blocks/login`|Block|UI|1|
|`blocks/logo-cloud`|Block|UI|0|
|`blocks/order-confirmation`|Block|UI|2|
|`blocks/plan-compare`|Block|UI|1|
|`blocks/pricing`|Block|UI|1|
|`blocks/roadmap`|Block|UI|2|
|`blocks/settings`|Block|UI|1|
|`blocks/site-footer`|Block|UI|5|
|`blocks/site-header`|Block|UI|5|
|`blocks/stat-cards`|Block|UI|1|
|`blocks/team`|Block|UI|1|
|`blocks/testimonials`|Block|UI|0|
|`blocks/use-cases`|Block|UI|5|
|`components/accordion`|Layout & Navigation|UI|1|
|`components/accordion-gallery`|Motion|Lab|3|
|`components/alert`|Feedback & Status|UI|0|
|`components/alert-dialog`|Overlays & Dialogs|UI|3|
|`components/aspect-ratio`|Display & Media|UI|1|
|`components/aurora`|Motion|Lab|5|
|`components/avatar`|Display & Media|UI|2|
|`components/badge`|Feedback & Status|UI|1|
|`components/bar-chart`|Display & Media|UI|1|
|`components/beam-border`|Motion|Lab|3|
|`components/blur-in`|Motion|Lab|1|
|`components/bottom-navigation`|Layout & Navigation|UI|4|
|`components/bounce-letters`|KATAYABURI|Lab|1|
|`components/breadcrumbs`|Layout & Navigation|UI|0|
|`components/burst-button`|Motion|Lab|2|
|`components/button`|Form & Input|UI|0|
|`components/button-group`|Form & Input|UI|0|
|`components/calendar`|Form & Input|UI|2|
|`components/candlestick-chart`|Display & Media|UI|0|
|`components/card`|Display & Media|UI|1|
|`components/carousel`|Display & Media|UI|3|
|`components/carousel-ring`|KATAYABURI|Lab|3|
|`components/cascader`|Form & Input|UI|3|
|`components/checkbox`|Form & Input|UI|4|
|`components/chip`|Display & Media|UI|2|
|`components/collapsible`|Layout & Navigation|UI|1|
|`components/color-picker`|Form & Input|UI|16|
|`components/combobox`|Form & Input|UI|0|
|`components/command`|Overlays & Dialogs|UI|4|
|`components/comparison-slider`|Motion|Lab|4|
|`components/confetti-cannon`|KATAYABURI|Lab|2|
|`components/context-menu`|Overlays & Dialogs|UI|5|
|`components/converge`|Motion|Lab|17|
|`components/copy-field`|Form & Input|UI|1|
|`components/counter`|Motion|Lab|0|
|`components/data-table`|Display & Media|UI|2|
|`components/date-picker`|Form & Input|UI|5|
|`components/descriptions`|Display & Media|UI|0|
|`components/dock`|Motion|Lab|6|
|`components/donut-chart`|Display & Media|UI|1|
|`components/drawer`|Overlays & Dialogs|UI|2|
|`components/dropdown`|Overlays & Dialogs|UI|4|
|`components/dual-range`|Form & Input|UI|7|
|`components/empty-state`|Feedback & Status|UI|1|
|`components/field`|Form & Input|UI|0|
|`components/file-upload`|Form & Input|UI|5|
|`components/fireworks`|KATAYABURI|Lab|1|
|`components/follow-frame`|Motion|Lab|4|
|`components/funnel-chart`|Display & Media|UI|1|
|`components/gauge`|Display & Media|UI|0|
|`components/glass-panel`|Display & Media|UI|3|
|`components/glow-button`|Motion|Lab|10|
|`components/glow-cards`|Motion|Lab|4|
|`components/goo-cursor`|KATAYABURI|Lab|1|
|`components/goo-tabs`|Motion|Lab|5|
|`components/gravity-playground`|KATAYABURI|Lab|2|
|`components/hanko`|Japan|UI|6|
|`components/heatmap`|Display & Media|UI|2|
|`components/horizontal-reel`|Motion|Lab|2|
|`components/hover-card`|Overlays & Dialogs|UI|3|
|`components/input`|Form & Input|UI|1|
|`components/input-group`|Form & Input|UI|0|
|`components/input-otp`|Form & Input|UI|4|
|`components/jelly-buttons`|KATAYABURI|Lab|3|
|`components/kaleidoscope`|KATAYABURI|Lab|3|
|`components/kata-rain`|KATAYABURI|Lab|1|
|`components/kbd`|Display & Media|UI|1|
|`components/kintsugi-card`|Japan|UI|1|
|`components/line-chart`|Display & Media|UI|0|
|`components/liquid-button`|Motion|Lab|4|
|`components/list`|Display & Media|UI|1|
|`components/magnet`|Motion|Lab|4|
|`components/marquee`|Motion|Lab|1|
|`components/menubar`|Layout & Navigation|UI|5|
|`components/meteors`|Motion|Lab|4|
|`components/meter`|Feedback & Status|UI|0|
|`components/modal`|Overlays & Dialogs|UI|3|
|`components/navigation-menu`|Layout & Navigation|UI|7|
|`components/newtons-cradle`|KATAYABURI|Lab|5|
|`components/noren`|Japan|UI|6|
|`components/orbit`|Motion|Lab|9|
|`components/pagination`|Layout & Navigation|UI|1|
|`components/particle-net`|Motion|Lab|1|
|`components/particle-word`|KATAYABURI|Lab|2|
|`components/popover`|Overlays & Dialogs|UI|0|
|`components/progress`|Feedback & Status|UI|1|
|`components/qr-code`|Display & Media|UI|1|
|`components/radar-chart`|Display & Media|UI|0|
|`components/radio`|Form & Input|UI|3|
|`components/rating`|Form & Input|UI|2|
|`components/reorder`|Motion|Lab|4|
|`components/result`|Feedback & Status|UI|0|
|`components/scatter-chart`|Display & Media|UI|0|
|`components/scramble`|Motion|Lab|0|
|`components/scroll-area`|Layout & Navigation|UI|2|
|`components/scrollspy`|Layout & Navigation|UI|2|
|`components/segmented`|Form & Input|UI|4|
|`components/select`|Form & Input|UI|1|
|`components/separator`|Layout & Navigation|UI|0|
|`components/shine-text`|Motion|Lab|2|
|`components/sidebar`|Layout & Navigation|UI|8|
|`components/skeleton`|Feedback & Status|UI|1|
|`components/slider`|Form & Input|UI|6|
|`components/sparkles`|Motion|Lab|2|
|`components/sparkline`|Display & Media|UI|0|
|`components/speed-dial`|Layout & Navigation|UI|7|
|`components/spinner`|Feedback & Status|UI|3|
|`components/split-panel`|Layout & Navigation|UI|2|
|`components/spotlight`|Motion|Lab|2|
|`components/stacking-cards`|Motion|Lab|2|
|`components/stat`|Display & Media|UI|0|
|`components/stepper`|Form & Input|UI|1|
|`components/steps`|Layout & Navigation|UI|2|
|`components/switch`|Form & Input|UI|5|
|`components/table`|Display & Media|UI|0|
|`components/tabs`|Layout & Navigation|UI|6|
|`components/tag-input`|Form & Input|UI|2|
|`components/tategaki`|Japan|UI|2|
|`components/text-reveal`|Motion|Lab|1|
|`components/textarea`|Form & Input|UI|1|
|`components/tilt-card`|Motion|Lab|4|
|`components/time-picker`|Form & Input|UI|4|
|`components/timeline`|Display & Media|UI|1|
|`components/toast`|Feedback & Status|UI|3|
|`components/toggle`|Form & Input|UI|3|
|`components/tooltip`|Overlays & Dialogs|UI|4|
|`components/torn-ticket`|Display & Media|UI|3|
|`components/tour`|Overlays & Dialogs|UI|7|
|`components/tracing-beam`|Motion|Lab|3|
|`components/transfer`|Form & Input|UI|1|
|`components/tree`|Layout & Navigation|UI|3|
|`components/typeset`|Display & Media|UI|1|
|`components/typewriter`|Motion|Lab|1|
|`components/wagara`|Japan|UI|4|
|`components/warp-tunnel`|KATAYABURI|Lab|3|
|`components/word-rotate`|Motion|Lab|1|
|`templates/blog-article`|Template|UI|6|
|`templates/checkout`|Template|UI|3|
|`templates/dashboard`|Template|UI|6|
|`templates/inbox`|Template|UI|2|
|`templates/landing`|Template|UI|1|
|`templates/product-page`|Template|UI|9|
|`templates/settings-page`|Template|UI|3|

## ソース対応（検査433件と追加棚卸しを値ごとに辿る）

表の値が現れるファイルと回数。同一ファイルに同一宣言が複数あれば回数を付ける。行番号は後続修正でずれるため、propertyと元の値を検索キーにする。

| 種類 | property | 元の値 | ファイル:回数 |
|---|---|---|---|
|radius|`border-radius`|`14px`|[blocks/app-shell/app-shell.css](../blocks/app-shell/app-shell.css):1<br>[blocks/cookie-consent/cookie-consent.css](../blocks/cookie-consent/cookie-consent.css):1<br>[blocks/invoice/invoice.css](../blocks/invoice/invoice.css):1<br>[blocks/kanban/kanban.css](../blocks/kanban/kanban.css):1<br>[blocks/order-confirmation/order-confirmation.css](../blocks/order-confirmation/order-confirmation.css):1<br>[blocks/pricing/pricing.css](../blocks/pricing/pricing.css):1<br>[blocks/roadmap/roadmap.css](../blocks/roadmap/roadmap.css):1<br>[blocks/settings/settings.css](../blocks/settings/settings.css):1<br>[blocks/site-footer/site-footer.css](../blocks/site-footer/site-footer.css):1<br>[blocks/site-header/site-header.css](../blocks/site-header/site-header.css):1<br>[blocks/team/team.css](../blocks/team/team.css):1<br>[blocks/use-cases/use-cases.css](../blocks/use-cases/use-cases.css):3<br>[components/aurora/aurora.css](../components/aurora/aurora.css):1<br>[components/beam-border/beam-border.css](../components/beam-border/beam-border.css):1<br>[components/card/card.css](../components/card/card.css):1<br>[components/carousel-ring/carousel-ring.css](../components/carousel-ring/carousel-ring.css):1<br>[components/carousel/carousel.css](../components/carousel/carousel.css):1<br>[components/cascader/cascader.css](../components/cascader/cascader.css):1<br>[components/command/command.css](../components/command/command.css):1<br>[components/confetti-cannon/confetti-cannon.css](../components/confetti-cannon/confetti-cannon.css):1<br>[components/context-menu/context-menu.css](../components/context-menu/context-menu.css):1<br>[components/converge/converge.css](../components/converge/converge.css):1<br>[components/data-table/data-table.css](../components/data-table/data-table.css):1<br>[components/date-picker/date-picker.css](../components/date-picker/date-picker.css):1<br>[components/dock/preview.html](../components/dock/preview.html):1<br>[components/file-upload/file-upload.css](../components/file-upload/file-upload.css):1<br>[components/fireworks/fireworks.css](../components/fireworks/fireworks.css):1<br>[components/follow-frame/follow-frame.css](../components/follow-frame/follow-frame.css):1<br>[components/glass-panel/glass-panel.css](../components/glass-panel/glass-panel.css):1<br>[components/glow-cards/glow-cards.css](../components/glow-cards/glow-cards.css):1<br>[components/goo-cursor/goo-cursor.css](../components/goo-cursor/goo-cursor.css):1<br>[components/gravity-playground/gravity-playground.css](../components/gravity-playground/gravity-playground.css):1<br>[components/hanko/hanko.css](../components/hanko/hanko.css):1<br>[components/horizontal-reel/horizontal-reel.css](../components/horizontal-reel/horizontal-reel.css):1<br>[components/hover-card/hover-card.css](../components/hover-card/hover-card.css):1<br>[components/jelly-buttons/jelly-buttons.css](../components/jelly-buttons/jelly-buttons.css):1<br>[components/kaleidoscope/kaleidoscope.css](../components/kaleidoscope/kaleidoscope.css):1<br>[components/kata-rain/kata-rain.css](../components/kata-rain/kata-rain.css):1<br>[components/kintsugi-card/kintsugi-card.css](../components/kintsugi-card/kintsugi-card.css):1<br>[components/list/list.css](../components/list/list.css):1<br>[components/magnet/preview.html](../components/magnet/preview.html):1<br>[components/menubar/preview.html](../components/menubar/preview.html):1<br>[components/meteors/meteors.css](../components/meteors/meteors.css):1<br>[components/navigation-menu/navigation-menu.css](../components/navigation-menu/navigation-menu.css):1<br>[components/navigation-menu/preview.html](../components/navigation-menu/preview.html):1<br>[components/newtons-cradle/newtons-cradle.css](../components/newtons-cradle/newtons-cradle.css):1<br>[components/noren/noren.css](../components/noren/noren.css):1<br>[components/particle-net/particle-net.css](../components/particle-net/particle-net.css):1<br>[components/particle-word/particle-word.css](../components/particle-word/particle-word.css):1<br>[components/qr-code/examples.html](../components/qr-code/examples.html):1<br>[components/shine-text/examples.html](../components/shine-text/examples.html):1<br>[components/sidebar/examples.html](../components/sidebar/examples.html):2<br>[components/sidebar/preview.html](../components/sidebar/preview.html):1<br>[components/sparkles/examples.html](../components/sparkles/examples.html):1<br>[components/sparkles/preview.html](../components/sparkles/preview.html):1<br>[components/speed-dial/preview.html](../components/speed-dial/preview.html):1<br>[components/split-panel/split-panel.css](../components/split-panel/split-panel.css):1<br>[components/stacking-cards/stacking-cards.css](../components/stacking-cards/stacking-cards.css):1<br>[components/tategaki/tategaki.css](../components/tategaki/tategaki.css):1<br>[components/time-picker/time-picker.css](../components/time-picker/time-picker.css):1<br>[components/tour/tour.css](../components/tour/tour.css):2<br>[components/wagara/wagara.css](../components/wagara/wagara.css):1<br>[components/warp-tunnel/warp-tunnel.css](../components/warp-tunnel/warp-tunnel.css):1<br>[templates/checkout/checkout.css](../templates/checkout/checkout.css):2<br>[templates/product-page/product-page.css](../templates/product-page/product-page.css):1|
|radius|`border-radius`|`8px`|[blocks/app-shell/app-shell.css](../blocks/app-shell/app-shell.css):1<br>[blocks/site-footer/site-footer.css](../blocks/site-footer/site-footer.css):1<br>[components/calendar/calendar.css](../components/calendar/calendar.css):2<br>[components/cascader/cascader.css](../components/cascader/cascader.css):1<br>[components/command/command.css](../components/command/command.css):1<br>[components/context-menu/context-menu.css](../components/context-menu/context-menu.css):1<br>[components/date-picker/date-picker.css](../components/date-picker/date-picker.css):1<br>[components/kaleidoscope/kaleidoscope.css](../components/kaleidoscope/kaleidoscope.css):1<br>[components/navigation-menu/navigation-menu.css](../components/navigation-menu/navigation-menu.css):2<br>[components/segmented/segmented.css](../components/segmented/segmented.css):1<br>[components/sidebar/sidebar.css](../components/sidebar/sidebar.css):1<br>[components/speed-dial/speed-dial.css](../components/speed-dial/speed-dial.css):1<br>[components/split-panel/split-panel.css](../components/split-panel/split-panel.css):1<br>[components/tabs/tabs.css](../components/tabs/tabs.css):2<br>[components/time-picker/time-picker.css](../components/time-picker/time-picker.css):1<br>[components/transfer/transfer.css](../components/transfer/transfer.css):1<br>[components/tree/tree.css](../components/tree/tree.css):1<br>[templates/dashboard/dashboard.css](../templates/dashboard/dashboard.css):1<br>[templates/inbox/inbox.css](../templates/inbox/inbox.css):1<br>[templates/settings-page/settings-page.css](../templates/settings-page/settings-page.css):1|
|radius|`border-radius`|`99px`|[blocks/kanban/kanban.css](../blocks/kanban/kanban.css):1<br>[components/badge/badge.css](../components/badge/badge.css):1<br>[components/carousel/carousel.css](../components/carousel/carousel.css):1<br>[components/chip/chip.css](../components/chip/chip.css):1<br>[components/comparison-slider/comparison-slider.css](../components/comparison-slider/comparison-slider.css):1<br>[components/confetti-cannon/confetti-cannon.css](../components/confetti-cannon/confetti-cannon.css):1<br>[components/follow-frame/follow-frame.css](../components/follow-frame/follow-frame.css):1<br>[components/goo-tabs/goo-tabs.css](../components/goo-tabs/goo-tabs.css):3<br>[components/gravity-playground/gravity-playground.css](../components/gravity-playground/gravity-playground.css):1<br>[components/kaleidoscope/kaleidoscope.css](../components/kaleidoscope/kaleidoscope.css):1<br>[components/magnet/preview.html](../components/magnet/preview.html):1<br>[components/particle-word/particle-word.css](../components/particle-word/particle-word.css):1<br>[components/reorder/reorder.css](../components/reorder/reorder.css):1<br>[components/scroll-area/scroll-area.css](../components/scroll-area/scroll-area.css):1<br>[components/sidebar/sidebar.css](../components/sidebar/sidebar.css):1<br>[components/switch/switch.css](../components/switch/switch.css):1<br>[components/tour/tour.css](../components/tour/tour.css):1<br>[components/wagara/wagara.css](../components/wagara/wagara.css):3|
|radius|`border-radius`|`16px`|[blocks/cta-band/cta-band.css](../blocks/cta-band/cta-band.css):2<br>[blocks/login/login.css](../blocks/login/login.css):1<br>[components/alert-dialog/alert-dialog.css](../components/alert-dialog/alert-dialog.css):1<br>[components/converge/converge.css](../components/converge/converge.css):1<br>[components/modal/modal.css](../components/modal/modal.css):1<br>[components/tilt-card/tilt-card.css](../components/tilt-card/tilt-card.css):1<br>[templates/blog-article/blog-article.css](../templates/blog-article/blog-article.css):1<br>[templates/checkout/checkout.css](../templates/checkout/checkout.css):1<br>[templates/dashboard/dashboard.css](../templates/dashboard/dashboard.css):1<br>[templates/inbox/inbox.css](../templates/inbox/inbox.css):1<br>[templates/landing/landing.css](../templates/landing/landing.css):1<br>[templates/product-page/product-page.css](../templates/product-page/product-page.css):1<br>[templates/settings-page/settings-page.css](../templates/settings-page/settings-page.css):1|
|radius|`border-radius`|`12px`|[blocks/stat-cards/stat-cards.css](../blocks/stat-cards/stat-cards.css):1<br>[components/aspect-ratio/aspect-ratio.css](../components/aspect-ratio/aspect-ratio.css):1<br>[components/context-menu/context-menu.css](../components/context-menu/context-menu.css):1<br>[components/hanko/hanko.css](../components/hanko/hanko.css):1<br>[components/orbit/orbit.css](../components/orbit/orbit.css):1<br>[components/scrollspy/scrollspy.css](../components/scrollspy/scrollspy.css):1<br>[components/sidebar/examples.html](../components/sidebar/examples.html):1<br>[components/toast/toast.css](../components/toast/toast.css):1<br>[components/toggle/toggle.css](../components/toggle/toggle.css):1<br>[templates/blog-article/blog-article.css](../templates/blog-article/blog-article.css):1<br>[templates/dashboard/dashboard.css](../templates/dashboard/dashboard.css):1<br>[templates/product-page/product-page.css](../templates/product-page/product-page.css):1<br>[templates/settings-page/settings-page.css](../templates/settings-page/settings-page.css):1|
|radius|`border-radius`|`7px`|[blocks/site-footer/site-footer.css](../blocks/site-footer/site-footer.css):1<br>[blocks/site-header/site-header.css](../blocks/site-header/site-header.css):1<br>[components/converge/converge.css](../components/converge/converge.css):1<br>[components/date-picker/date-picker.css](../components/date-picker/date-picker.css):1<br>[components/dropdown/dropdown.css](../components/dropdown/dropdown.css):1<br>[components/file-upload/file-upload.css](../components/file-upload/file-upload.css):1<br>[components/funnel-chart/funnel-chart.css](../components/funnel-chart/funnel-chart.css):1<br>[components/menubar/menubar.css](../components/menubar/menubar.css):2<br>[components/scrollspy/scrollspy.css](../components/scrollspy/scrollspy.css):1<br>[components/sidebar/sidebar.css](../components/sidebar/sidebar.css):1<br>[components/time-picker/time-picker.css](../components/time-picker/time-picker.css):1<br>[templates/dashboard/dashboard.css](../templates/dashboard/dashboard.css):1|
|radius|`border-radius`|`11px`|[blocks/kanban/kanban.css](../blocks/kanban/kanban.css):1<br>[blocks/order-confirmation/order-confirmation.css](../blocks/order-confirmation/order-confirmation.css):1<br>[blocks/roadmap/roadmap.css](../blocks/roadmap/roadmap.css):1<br>[components/burst-button/burst-button.css](../components/burst-button/burst-button.css):1<br>[components/dropdown/dropdown.css](../components/dropdown/dropdown.css):1<br>[components/file-upload/file-upload.css](../components/file-upload/file-upload.css):1<br>[components/glow-button/glow-button.css](../components/glow-button/glow-button.css):2<br>[components/liquid-button/liquid-button.css](../components/liquid-button/liquid-button.css):1<br>[components/menubar/menubar.css](../components/menubar/menubar.css):1<br>[components/segmented/segmented.css](../components/segmented/segmented.css):1<br>[templates/blog-article/blog-article.css](../templates/blog-article/blog-article.css):1|
|radius|`border-radius`|`13px`|[blocks/cookie-consent/cookie-consent.css](../blocks/cookie-consent/cookie-consent.css):1<br>[blocks/filter-toolbar/filter-toolbar.css](../blocks/filter-toolbar/filter-toolbar.css):1<br>[blocks/integrations/integrations.css](../blocks/integrations/integrations.css):1<br>[components/accordion-gallery/accordion-gallery.css](../components/accordion-gallery/accordion-gallery.css):1<br>[components/carousel-ring/carousel-ring.css](../components/carousel-ring/carousel-ring.css):1<br>[components/dock/dock.css](../components/dock/dock.css):1<br>[components/glow-button/glow-button.css](../components/glow-button/glow-button.css):1<br>[components/horizontal-reel/horizontal-reel.css](../components/horizontal-reel/horizontal-reel.css):1<br>[components/stacking-cards/stacking-cards.css](../components/stacking-cards/stacking-cards.css):1<br>[components/torn-ticket/torn-ticket.css](../components/torn-ticket/torn-ticket.css):1<br>[templates/blog-article/blog-article.css](../templates/blog-article/blog-article.css):2|
|radius|`border-radius`|`10px`|[blocks/integrations/integrations.css](../blocks/integrations/integrations.css):1<br>[components/color-picker/color-picker.css](../components/color-picker/color-picker.css):2<br>[components/follow-frame/follow-frame.css](../components/follow-frame/follow-frame.css):1<br>[components/glow-cards/glow-cards.css](../components/glow-cards/glow-cards.css):1<br>[components/input-otp/input-otp.css](../components/input-otp/input-otp.css):1<br>[components/reorder/reorder.css](../components/reorder/reorder.css):1<br>[components/tabs/tabs.css](../components/tabs/tabs.css):2<br>[components/tour/tour.css](../components/tour/tour.css):1<br>[templates/product-page/product-page.css](../templates/product-page/product-page.css):1|
|radius|`border-radius`|`9px`|[blocks/site-header/site-header.css](../blocks/site-header/site-header.css):1<br>[components/bottom-navigation/bottom-navigation.css](../components/bottom-navigation/bottom-navigation.css):1<br>[components/date-picker/date-picker.css](../components/date-picker/date-picker.css):1<br>[components/navigation-menu/navigation-menu.css](../components/navigation-menu/navigation-menu.css):1<br>[components/scroll-area/scroll-area.css](../components/scroll-area/scroll-area.css):1<br>[components/toggle/toggle.css](../components/toggle/toggle.css):1<br>[templates/product-page/product-page.css](../templates/product-page/product-page.css):1|
|radius|`border-radius`|`6px`|[components/color-picker/color-picker.css](../components/color-picker/color-picker.css):1<br>[components/dock/dock.css](../components/dock/dock.css):1<br>[components/dual-range/dual-range.css](../components/dual-range/dual-range.css):1<br>[components/kbd/kbd.css](../components/kbd/kbd.css):1<br>[components/rating/rating.css](../components/rating/rating.css):1<br>[components/tooltip/tooltip.css](../components/tooltip/tooltip.css):1|
|radius|`border-radius`|`2px`|[components/input-otp/input-otp.css](../components/input-otp/input-otp.css):1<br>[components/meteors/meteors.css](../components/meteors/meteors.css):1<br>[components/steps/steps.css](../components/steps/steps.css):1<br>[components/tracing-beam/tracing-beam.css](../components/tracing-beam/tracing-beam.css):2|
|radius|`border-radius`|`3px`|[components/donut-chart/donut-chart.css](../components/donut-chart/donut-chart.css):1<br>[components/dual-range/dual-range.css](../components/dual-range/dual-range.css):2<br>[components/heatmap/heatmap.css](../components/heatmap/heatmap.css):2|
|radius|`border-radius`|`5px`|[components/checkbox/checkbox.css](../components/checkbox/checkbox.css):1<br>[components/tree/tree.css](../components/tree/tree.css):1<br>[components/typeset/typeset.css](../components/typeset/typeset.css):1<br>[templates/blog-article/blog-article.css](../templates/blog-article/blog-article.css):1|
|radius|`border-radius`|`18px`|[components/bottom-navigation/examples.html](../components/bottom-navigation/examples.html):1<br>[components/bottom-navigation/preview.html](../components/bottom-navigation/preview.html):1<br>[components/orbit/orbit.css](../components/orbit/orbit.css):1|
|radius|`border-radius`|`2.5px`|[blocks/site-footer/site-footer.css](../blocks/site-footer/site-footer.css):1<br>[blocks/site-header/site-header.css](../blocks/site-header/site-header.css):1<br>[templates/dashboard/dashboard.css](../templates/dashboard/dashboard.css):1|
|radius|`border-radius`|`4px`|[components/newtons-cradle/newtons-cradle.css](../components/newtons-cradle/newtons-cradle.css):1<br>[components/noren/noren.css](../components/noren/noren.css):1|
|radius|`border-radius`|`10px 10px 0 0`|[blocks/plan-compare/plan-compare.css](../blocks/plan-compare/plan-compare.css):1|
|radius|`border-radius`|`12.5px`|[components/beam-border/beam-border.css](../components/beam-border/beam-border.css):1|
|radius|`border-radius`|`20px`|[components/dock/dock.css](../components/dock/dock.css):1|
|radius|`border-radius`|`5px 5px 0 0`|[components/bar-chart/bar-chart.css](../components/bar-chart/bar-chart.css):1|
|radius|`border-radius`|`9.5px`|[components/glow-button/glow-button.css](../components/glow-button/glow-button.css):1|
|radius|`border-radius`|`9px 11px 10px 12px`|[components/hanko/hanko.css](../components/hanko/hanko.css):1|
|duration|`transition`|`transform .18s`|[components/collapsible/collapsible.css](../components/collapsible/collapsible.css):1<br>[components/navigation-menu/navigation-menu.css](../components/navigation-menu/navigation-menu.css):1<br>[components/sidebar/sidebar.css](../components/sidebar/sidebar.css):1<br>[components/switch/switch.css](../components/switch/switch.css):1|
|duration|`transition`|`opacity .15s,transform .15s`|[components/dock/dock.css](../components/dock/dock.css):1<br>[components/dropdown/dropdown.css](../components/dropdown/dropdown.css):1<br>[components/tooltip/tooltip.css](../components/tooltip/tooltip.css):1|
|duration|`animation`|`k-ga-spin 3.6s linear infinite`|[components/glow-button/glow-button.css](../components/glow-button/glow-button.css):2|
|duration|`animation-duration`|`16s`|[components/orbit/orbit.css](../components/orbit/orbit.css):2|
|duration|`animation-duration`|`26s`|[components/orbit/orbit.css](../components/orbit/orbit.css):2|
|duration|`transition`|`background .13s`|[components/pagination/pagination.css](../components/pagination/pagination.css):1<br>[components/stepper/stepper.css](../components/stepper/stepper.css):1|
|duration|`transition`|`border-color .13s, box-shadow .13s`|[components/input-otp/input-otp.css](../components/input-otp/input-otp.css):1<br>[components/tag-input/tag-input.css](../components/tag-input/tag-input.css):1|
|duration|`transition`|`border-color .15s`|[components/radio/radio.css](../components/radio/radio.css):1<br>[components/select/select.css](../components/select/select.css):1|
|duration|`animation`|`k-aur-a 9s var(--k-ease) infinite alternate`|[components/aurora/aurora.css](../components/aurora/aurora.css):1|
|duration|`animation`|`k-aur-b 12s var(--k-ease) infinite alternate`|[components/aurora/aurora.css](../components/aurora/aurora.css):1|
|duration|`animation`|`k-aur-c 11s var(--k-ease) infinite alternate`|[components/aurora/aurora.css](../components/aurora/aurora.css):1|
|duration|`animation`|`k-aur-pat 26s linear infinite alternate`|[components/aurora/aurora.css](../components/aurora/aurora.css):1|
|duration|`animation`|`k-beam-spin 4.5s linear infinite`|[components/beam-border/beam-border.css](../components/beam-border/beam-border.css):1|
|duration|`animation`|`k-blur-in .7s cubic-bezier(.2,.6,.2,1) forwards`|[components/blur-in/blur-in.css](../components/blur-in/blur-in.css):1|
|duration|`animation`|`k-conv-pulse 3.4s var(--k-ease) infinite alternate`|[components/converge/converge.css](../components/converge/converge.css):1|
|duration|`animation`|`k-conv-tw 2.2s ease-in-out infinite alternate`|[components/converge/converge.css](../components/converge/converge.css):1|
|duration|`animation`|`k-cr-l 2.4s ease-in-out infinite`|[components/newtons-cradle/newtons-cradle.css](../components/newtons-cradle/newtons-cradle.css):1|
|duration|`animation`|`k-cr-r 2.4s ease-in-out infinite`|[components/newtons-cradle/newtons-cradle.css](../components/newtons-cradle/newtons-cradle.css):1|
|duration|`animation`|`k-jelly-wob .55s cubic-bezier(.3,2.2,.45,1)`|[components/jelly-buttons/jelly-buttons.css](../components/jelly-buttons/jelly-buttons.css):1|
|duration|`animation`|`k-marquee 30s linear infinite`|[components/marquee/marquee.css](../components/marquee/marquee.css):1|
|duration|`animation`|`k-nor-sway 5.2s ease-in-out infinite alternate`|[components/noren/noren.css](../components/noren/noren.css):1|
|duration|`animation`|`k-nor-sway 5.8s ease-in-out infinite alternate`|[components/noren/noren.css](../components/noren/noren.css):1|
|duration|`animation`|`k-nor-sway 6.4s ease-in-out infinite alternate-reverse`|[components/noren/noren.css](../components/noren/noren.css):1|
|duration|`animation`|`k-ring-spin 26s linear infinite`|[components/carousel-ring/carousel-ring.css](../components/carousel-ring/carousel-ring.css):1|
|duration|`animation`|`k-seal-in .5s cubic-bezier(.2,1.6,.4,1)`|[components/hanko/hanko.css](../components/hanko/hanko.css):1|
|duration|`animation`|`k-seal-ring .55s ease-out`|[components/hanko/hanko.css](../components/hanko/hanko.css):1|
|duration|`animation`|`k-shimmer 1.4s ease-in-out infinite`|[components/skeleton/skeleton.css](../components/skeleton/skeleton.css):1|
|duration|`animation`|`k-shine-move 3.4s linear infinite`|[components/shine-text/shine-text.css](../components/shine-text/shine-text.css):1|
|duration|`animation`|`k-spin .7s linear infinite`|[components/spinner/spinner.css](../components/spinner/spinner.css):1|
|duration|`animation`|`k-tate-in 1s cubic-bezier(.2,.7,.2,1) both`|[components/tategaki/tategaki.css](../components/tategaki/tategaki.css):1|
|duration|`animation`|`k-tin .3s cubic-bezier(.3,1.2,.4,1)`|[components/toast/toast.css](../components/toast/toast.css):1|
|duration|`animation`|`k-type-blink 1.05s steps(1) infinite`|[components/typewriter/typewriter.css](../components/typewriter/typewriter.css):1|
|duration|`animation`|`k-uc-in .45s var(--k-ease)`|[blocks/use-cases/use-cases.css](../blocks/use-cases/use-cases.css):1|
|duration|`animation`|`k-warp-fly 5s linear infinite`|[components/warp-tunnel/warp-tunnel.css](../components/warp-tunnel/warp-tunnel.css):1|
|duration|`animation-duration`|`1.6s`|[components/spinner/spinner.css](../components/spinner/spinner.css):1|
|duration|`transition`|`background .13s,border-color .13s`|[components/checkbox/checkbox.css](../components/checkbox/checkbox.css):1|
|duration|`transition`|`background .13s,border-color .13s,color .13s`|[components/toggle/toggle.css](../components/toggle/toggle.css):1|
|duration|`transition`|`background .15s`|[components/copy-field/copy-field.css](../components/copy-field/copy-field.css):1|
|duration|`transition`|`background .15s,color .15s`|[components/segmented/segmented.css](../components/segmented/segmented.css):1|
|duration|`transition`|`background .18s`|[components/switch/switch.css](../components/switch/switch.css):1|
|duration|`transition`|`background .3s, box-shadow .3s`|[components/glow-button/glow-button.css](../components/glow-button/glow-button.css):1|
|duration|`transition`|`border-color .14s`|[blocks/integrations/integrations.css](../blocks/integrations/integrations.css):1|
|duration|`transition`|`border-color .15s,background .15s`|[components/file-upload/file-upload.css](../components/file-upload/file-upload.css):1|
|duration|`transition`|`border-color .15s,box-shadow .15s`|[components/textarea/textarea.css](../components/textarea/textarea.css):1|
|duration|`transition`|`box-shadow .3s`|[components/glow-button/glow-button.css](../components/glow-button/glow-button.css):1|
|duration|`transition`|`color .25s`|[components/goo-tabs/goo-tabs.css](../components/goo-tabs/goo-tabs.css):1|
|duration|`transition`|`color .4s`|[components/liquid-button/liquid-button.css](../components/liquid-button/liquid-button.css):1|
|duration|`transition`|`fill .12s`|[components/rating/rating.css](../components/rating/rating.css):1|
|duration|`transition`|`flex .55s cubic-bezier(.6,0,.2,1)`|[components/accordion-gallery/accordion-gallery.css](../components/accordion-gallery/accordion-gallery.css):1|
|duration|`transition`|`left .22s cubic-bezier(.3,.7,.3,1),width .22s cubic-bezier(.3,.7,.3,1)`|[components/tabs/tabs.css](../components/tabs/tabs.css):1|
|duration|`transition`|`left .45s cubic-bezier(.6,-0.1,.2,1.25), width .45s cubic-bezier(.6,-0.1,.2,1.25), transform .3s`|[components/goo-tabs/goo-tabs.css](../components/goo-tabs/goo-tabs.css):1|
|duration|`transition`|`opacity .15s`|[components/tooltip/tooltip.css](../components/tooltip/tooltip.css):1|
|duration|`transition`|`opacity .16s var(--k-ease),transform .16s var(--k-ease)`|[components/hover-card/hover-card.css](../components/hover-card/hover-card.css):1|
|duration|`transition`|`opacity .18s,transform .18s`|[components/speed-dial/speed-dial.css](../components/speed-dial/speed-dial.css):1|
|duration|`transition`|`opacity .25s`|[components/glow-cards/glow-cards.css](../components/glow-cards/glow-cards.css):1|
|duration|`transition`|`opacity .3s .18s`|[components/accordion-gallery/accordion-gallery.css](../components/accordion-gallery/accordion-gallery.css):1|
|duration|`transition`|`transform .08s linear`|[components/tilt-card/tilt-card.css](../components/tilt-card/tilt-card.css):1|
|duration|`transition`|`transform .12s`|[components/burst-button/burst-button.css](../components/burst-button/burst-button.css):1|
|duration|`transition`|`transform .12s ease-out`|[components/magnet/magnet.css](../components/magnet/magnet.css):1|
|duration|`transition`|`transform .12s var(--k-ease)`|[components/color-picker/color-picker.css](../components/color-picker/color-picker.css):1|
|duration|`transition`|`transform .13s`|[components/checkbox/checkbox.css](../components/checkbox/checkbox.css):1|
|duration|`transition`|`transform .14s ease-out`|[components/dock/dock.css](../components/dock/dock.css):1|
|duration|`transition`|`transform .15s cubic-bezier(.3,.7,.3,1)`|[components/radio/radio.css](../components/radio/radio.css):1|
|duration|`transition`|`transform .15s var(--k-ease)`|[components/tree/tree.css](../components/tree/tree.css):1|
|duration|`transition`|`transform .15s var(--k-ease),opacity .15s`|[components/data-table/data-table.css](../components/data-table/data-table.css):1|
|duration|`transition`|`transform .18s cubic-bezier(.3,.7,.3,1)`|[components/accordion/accordion.css](../components/accordion/accordion.css):1|
|duration|`transition`|`transform .28s cubic-bezier(.3,2.4,.45,1)`|[components/jelly-buttons/jelly-buttons.css](../components/jelly-buttons/jelly-buttons.css):1|
|duration|`transition`|`transform .2s`|[components/speed-dial/speed-dial.css](../components/speed-dial/speed-dial.css):1|
|duration|`transition`|`transform .2s var(--k-ease)`|[blocks/use-cases/use-cases.css](../blocks/use-cases/use-cases.css):1|
|duration|`transition`|`transform .34s cubic-bezier(.3,2.3,.4,1)`|[components/bounce-letters/bounce-letters.css](../components/bounce-letters/bounce-letters.css):1|
|duration|`transition`|`transform .35s cubic-bezier(.2,.8,.25,1.2)`|[components/magnet/magnet.css](../components/magnet/magnet.css):1|
|duration|`transition`|`transform .3s ease-out`|[components/tilt-card/tilt-card.css](../components/tilt-card/tilt-card.css):1|
|duration|`transition`|`transform .55s cubic-bezier(.65,0,.2,1)`|[components/word-rotate/word-rotate.css](../components/word-rotate/word-rotate.css):1|
|duration|`transition`|`transform .5s cubic-bezier(.4,0,.2,1)`|[components/noren/noren.css](../components/noren/noren.css):1|
|duration|`transition`|`transform .65s cubic-bezier(.5,0,.2,1)`|[components/liquid-button/liquid-button.css](../components/liquid-button/liquid-button.css):1|
|duration|`transition`|`transform .7s cubic-bezier(.3,.7,.3,1)`|[components/text-reveal/text-reveal.css](../components/text-reveal/text-reveal.css):1|
|duration|`transition`|`width .18s var(--k-ease),background .18s`|[components/carousel/carousel.css](../components/carousel/carousel.css):1|
|duration|`transition`|`width .3s cubic-bezier(.3,.7,.3,1)`|[components/progress/progress.css](../components/progress/progress.css):1|
|shadow|`box-shadow`|`0 20px 44px -14px rgba(16,24,40,.22)`|[components/cascader/cascader.css](../components/cascader/cascader.css):1<br>[components/date-picker/date-picker.css](../components/date-picker/date-picker.css):1<br>[components/navigation-menu/navigation-menu.css](../components/navigation-menu/navigation-menu.css):1<br>[components/time-picker/time-picker.css](../components/time-picker/time-picker.css):1|
|shadow|`box-shadow`|`0 0 0 3px var(--k-accent-bg)`|[components/input-otp/input-otp.css](../components/input-otp/input-otp.css):1<br>[components/tag-input/tag-input.css](../components/tag-input/tag-input.css):1|
|shadow|`box-shadow`|`0 1px 2px rgba(16,24,40,.18)`|[components/slider/slider.css](../components/slider/slider.css):2|
|shadow|`box-shadow`|`0 1px 4px rgba(16,24,40,.18)`|[components/dual-range/dual-range.css](../components/dual-range/dual-range.css):2|
|shadow|`box-shadow`|`0 30px 80px -20px rgba(0,0,0,.4)`|[components/alert-dialog/alert-dialog.css](../components/alert-dialog/alert-dialog.css):1<br>[components/modal/modal.css](../components/modal/modal.css):1|
|shadow|`box-shadow`|`-24px 0 60px -24px rgba(0,0,0,.35)`|[components/drawer/drawer.css](../components/drawer/drawer.css):1|
|shadow|`box-shadow`|`0 0 0 1px rgba(24,24,27,.25)`|[components/comparison-slider/comparison-slider.css](../components/comparison-slider/comparison-slider.css):1|
|shadow|`box-shadow`|`0 0 0 1px var(--k-line)`|[templates/product-page/product-page.css](../templates/product-page/product-page.css):1|
|shadow|`box-shadow`|`0 0 0 2px var(--k-accent)`|[templates/product-page/product-page.css](../templates/product-page/product-page.css):1|
|shadow|`box-shadow`|`0 0 0 2px var(--k-bg),0 0 0 4px var(--k-accent)`|[components/color-picker/color-picker.css](../components/color-picker/color-picker.css):1|
|shadow|`box-shadow`|`0 0 0 2px var(--k-ink)`|[templates/product-page/product-page.css](../templates/product-page/product-page.css):1|
|shadow|`box-shadow`|`0 0 0 4px var(--k-accent-bg)`|[components/tracing-beam/tracing-beam.css](../components/tracing-beam/tracing-beam.css):1|
|shadow|`box-shadow`|`0 0 0 5px var(--k-accent-bg-strong)`|[components/tour/tour.css](../components/tour/tour.css):1|
|shadow|`box-shadow`|`0 0 10px 2px rgba(255,255,255,.3)`|[components/meteors/meteors.css](../components/meteors/meteors.css):1|
|shadow|`box-shadow`|`0 0 18px -4px var(--k-accent-bg)`|[components/glow-button/glow-button.css](../components/glow-button/glow-button.css):1|
|shadow|`box-shadow`|`0 0 26px -6px var(--k-accent)`|[components/glow-button/glow-button.css](../components/glow-button/glow-button.css):1|
|shadow|`box-shadow`|`0 0 46px color-mix(in srgb,var(--k-accent) 45%,transparent)`|[components/converge/converge.css](../components/converge/converge.css):1|
|shadow|`box-shadow`|`0 12px 26px -10px rgba(16,24,40,.4)`|[components/orbit/orbit.css](../components/orbit/orbit.css):1|
|shadow|`box-shadow`|`0 14px 28px -14px rgba(16,24,40,.28)`|[components/torn-ticket/torn-ticket.css](../components/torn-ticket/torn-ticket.css):1|
|shadow|`box-shadow`|`0 14px 34px -12px rgba(16,24,40,.25)`|[blocks/cookie-consent/cookie-consent.css](../blocks/cookie-consent/cookie-consent.css):1|
|shadow|`box-shadow`|`0 16px 40px -12px rgba(16,24,40,.18)`|[components/hover-card/hover-card.css](../components/hover-card/hover-card.css):1|
|shadow|`box-shadow`|`0 16px 40px -14px rgba(16,24,40,.25)`|[components/dropdown/dropdown.css](../components/dropdown/dropdown.css):1|
|shadow|`box-shadow`|`0 18px 40px -12px rgba(16,24,40,.25)`|[components/menubar/menubar.css](../components/menubar/menubar.css):1|
|shadow|`box-shadow`|`0 18px 40px -18px rgba(0,0,0,.45)`|[components/glass-panel/glass-panel.css](../components/glass-panel/glass-panel.css):1|
|shadow|`box-shadow`|`0 18px 44px -14px rgba(16,24,40,.28)`|[components/tour/tour.css](../components/tour/tour.css):1|
|shadow|`box-shadow`|`0 1px 2px rgba(16,24,40,.04)`|[components/input/input.css](../components/input/input.css):1|
|shadow|`box-shadow`|`0 1px 2px rgba(16,24,40,.05)`|[blocks/kanban/kanban.css](../blocks/kanban/kanban.css):1|
|shadow|`box-shadow`|`0 1px 2px rgba(16,24,40,.09)`|[components/segmented/segmented.css](../components/segmented/segmented.css):1|
|shadow|`box-shadow`|`0 1px 3px rgba(0,0,0,.3),inset 0 0 0 1px rgba(0,0,0,.08)`|[components/switch/switch.css](../components/switch/switch.css):1|
|shadow|`box-shadow`|`0 1px 3px rgba(16,24,40,.14)`|[components/tabs/tabs.css](../components/tabs/tabs.css):1|
|shadow|`box-shadow`|`0 20px 44px -12px rgba(16,24,40,.28)`|[components/context-menu/context-menu.css](../components/context-menu/context-menu.css):1|
|shadow|`box-shadow`|`0 20px 44px -14px rgba(0,0,0,.45)`|[components/toast/toast.css](../components/toast/toast.css):1|
|shadow|`box-shadow`|`0 2px 10px rgba(16,24,40,.3)`|[components/comparison-slider/comparison-slider.css](../components/comparison-slider/comparison-slider.css):1|
|shadow|`box-shadow`|`0 2px 8px rgba(16,24,40,.08)`|[components/speed-dial/speed-dial.css](../components/speed-dial/speed-dial.css):1|
|shadow|`box-shadow`|`0 2px 8px rgba(16,24,40,.1)`|[components/speed-dial/speed-dial.css](../components/speed-dial/speed-dial.css):1|
|shadow|`box-shadow`|`0 30px 80px -20px rgba(0,0,0,.45)`|[components/command/command.css](../components/command/command.css):1|
|shadow|`box-shadow`|`0 3px 7px rgba(16,24,40,.25)`|[components/newtons-cradle/newtons-cradle.css](../components/newtons-cradle/newtons-cradle.css):1|
|shadow|`box-shadow`|`0 4px 12px rgba(16,24,40,.1)`|[components/orbit/orbit.css](../components/orbit/orbit.css):1|
|shadow|`box-shadow`|`0 6px 18px rgba(16,24,40,.28)`|[components/speed-dial/speed-dial.css](../components/speed-dial/speed-dial.css):1|
|color / paint|`background`|`rgba(24,24,27,.45)`|[components/alert-dialog/alert-dialog.css](../components/alert-dialog/alert-dialog.css):1<br>[components/command/command.css](../components/command/command.css):1<br>[components/drawer/drawer.css](../components/drawer/drawer.css):1<br>[components/modal/modal.css](../components/modal/modal.css):1|
|color / paint|`background`|`radial-gradient(circle at center,var(--k-core) 0 2.5px,var(--k-knob) 3.2px)`|[components/slider/slider.css](../components/slider/slider.css):2|
|color / paint|`background`|`hsl(0 0% 11%)`|[components/color-picker/preview.html](../components/color-picker/preview.html):1|
|color / paint|`background`|`hsl(152 30% 52%)`|[components/color-picker/preview.html](../components/color-picker/preview.html):1|
|color / paint|`background`|`hsl(175 84% 32%)`|[components/color-picker/preview.html](../components/color-picker/preview.html):1|
|color / paint|`background`|`hsl(190 59% 46%)`|[components/color-picker/preview.html](../components/color-picker/preview.html):1|
|color / paint|`background`|`hsl(199 65% 60%)`|[components/color-picker/preview.html](../components/color-picker/preview.html):1|
|color / paint|`background`|`hsl(216 68% 38%)`|[components/color-picker/preview.html](../components/color-picker/preview.html):1|
|color / paint|`background`|`hsl(265 27% 46%)`|[components/color-picker/preview.html](../components/color-picker/preview.html):1|
|color / paint|`background`|`hsl(346 39% 38%)`|[components/color-picker/preview.html](../components/color-picker/preview.html):1|
|color / paint|`background`|`hsl(41 100% 55%)`|[components/color-picker/preview.html](../components/color-picker/preview.html):1|
|color / paint|`background`|`linear-gradient(to right, rgba(255,255,255,.75), transparent)`|[components/meteors/meteors.css](../components/meteors/meteors.css):1|
|color / paint|`background`|`radial-gradient(190px circle at var(--mx,50%) var(--my,50%), var(--k-accent), transparent 70%)`|[components/glow-cards/glow-cards.css](../components/glow-cards/glow-cards.css):1|
|color / paint|`background`|`radial-gradient(200px circle at var(--mx) var(--my),rgba(255,255,255,.17),rgba(255,255,255,.05) 55%,transparent 72%)`|[components/spotlight/spotlight.css](../components/spotlight/spotlight.css):1|
|color / paint|`background`|`radial-gradient(340px circle at var(--gx,50%) var(--gy,50%), rgba(255,255,255,.14), transparent 65%)`|[components/tilt-card/tilt-card.css](../components/tilt-card/tilt-card.css):1|
|color / paint|`background`|`radial-gradient(circle at 38% 32%,color-mix(in srgb,hsl(335 85% 68%) 34%,transparent),transparent 62%),radial-gradient(circle at 66% 70%,color-mix(in srgb,hsl(205 90% 63%) 30%,transparent),transparent 62%),radial-gradient(circle,color-mix(in srgb,var(--k-accent) 42%,transparent),transparent 68%)`|[components/converge/converge.css](../components/converge/converge.css):1|
|color / paint|`background`|`radial-gradient(circle at center,var(--k-core) 0 3px,var(--k-knob) 3.6px)`|[components/switch/switch.css](../components/switch/switch.css):1|
|color / paint|`background`|`repeating-linear-gradient(90deg, var(--k-ink) 0 2px, transparent 2px 5px, var(--k-ink) 5px 6px, transparent 6px 10px, var(--k-ink) 10px 13px, transparent 13px 16px)`|[components/torn-ticket/torn-ticket.css](../components/torn-ticket/torn-ticket.css):1|
|color / paint|`background`|`rgba(24,24,27,.72)`|[components/comparison-slider/comparison-slider.css](../components/comparison-slider/comparison-slider.css):1|
|color / paint|`background`|`rgba(255,255,255,.16)`|[components/chip/chip.css](../components/chip/chip.css):1|
|color / paint|`color`|`#fff`|[components/color-picker/color-picker.css](../components/color-picker/color-picker.css):1|
|color / paint|`color`|`hsl(205 90% 66%)`|[components/converge/preview.html](../components/converge/preview.html):1|
|color / paint|`color`|`hsl(32 95% 64%)`|[components/converge/preview.html](../components/converge/preview.html):1|
|color / paint|`color`|`hsl(335 85% 72%)`|[components/converge/preview.html](../components/converge/preview.html):1|
|color / paint|`color`|`rgba(255,255,255,.3)`|[components/spotlight/spotlight.css](../components/spotlight/spotlight.css):1|
|color / paint|`fill`|`hsl(205 90% 63%)`|[components/converge/converge.css](../components/converge/converge.css):1|
|color / paint|`fill`|`hsl(32 95% 60%)`|[components/converge/converge.css](../components/converge/converge.css):1|
|color / paint|`fill`|`hsl(335 85% 68%)`|[components/converge/converge.css](../components/converge/converge.css):1|
|color / paint|`stroke`|`hsl(205 90% 63%)`|[components/converge/converge.css](../components/converge/converge.css):1|
|color / paint|`stroke`|`hsl(32 95% 60%)`|[components/converge/converge.css](../components/converge/converge.css):1|
|color / paint|`stroke`|`hsl(335 85% 68%)`|[components/converge/converge.css](../components/converge/converge.css):1|
|border|`border`|`1.5px dashed var(--k-border-strong)`|[components/color-picker/color-picker.css](../components/color-picker/color-picker.css):1<br>[components/context-menu/context-menu.css](../components/context-menu/context-menu.css):1<br>[components/empty-state/empty-state.css](../components/empty-state/empty-state.css):1<br>[components/file-upload/file-upload.css](../components/file-upload/file-upload.css):1<br>[components/follow-frame/follow-frame.css](../components/follow-frame/follow-frame.css):1|
|border|`border`|`1.5px solid var(--k-border-strong)`|[components/checkbox/checkbox.css](../components/checkbox/checkbox.css):1<br>[components/radio/radio.css](../components/radio/radio.css):1<br>[components/slider/slider.css](../components/slider/slider.css):2|
|border|`border`|`2px solid var(--k-bg)`|[components/avatar/avatar.css](../components/avatar/avatar.css):2<br>[templates/product-page/product-page.css](../templates/product-page/product-page.css):1|
|border|`border`|`1px dashed var(--k-zinc-300)`|[blocks/cookie-consent/cookie-consent.css](../blocks/cookie-consent/cookie-consent.css):1<br>[components/orbit/orbit.css](../components/orbit/orbit.css):1|
|border|`border`|`2.5px solid var(--k-ink)`|[blocks/site-footer/site-footer.css](../blocks/site-footer/site-footer.css):1<br>[blocks/site-header/site-header.css](../blocks/site-header/site-header.css):1|
|border|`border`|`2px solid var(--k-line)`|[components/spinner/spinner.css](../components/spinner/spinner.css):1<br>[components/steps/steps.css](../components/steps/steps.css):1|
|border|`border`|`2px solid var(--k-zinc-400)`|[components/dual-range/dual-range.css](../components/dual-range/dual-range.css):2|
|border|`border`|`1.5px solid var(--k-bg)`|[components/bottom-navigation/bottom-navigation.css](../components/bottom-navigation/bottom-navigation.css):1|
|border|`border`|`1.5px solid var(--k-ink)`|[components/liquid-button/liquid-button.css](../components/liquid-button/liquid-button.css):1|
|border|`border`|`1px solid color-mix(in srgb,var(--k-on-color) 18%,transparent)`|[components/reorder/reorder.css](../components/reorder/reorder.css):1|
|border|`border`|`1px solid color-mix(in srgb,var(--k-on-color) 25%,transparent)`|[components/reorder/reorder.css](../components/reorder/reorder.css):1|
|border|`border`|`1px solid color-mix(in srgb,var(--k-on-color) 28%,transparent)`|[components/converge/converge.css](../components/converge/converge.css):1|
|border|`border`|`1px solid color-mix(in srgb,var(--k-on-color) 32%,transparent)`|[components/glass-panel/glass-panel.css](../components/glass-panel/glass-panel.css):1|
|border|`border`|`2px solid var(--k-accent)`|[components/tour/tour.css](../components/tour/tour.css):1|
|border|`border`|`2px solid var(--k-border-strong)`|[components/timeline/timeline.css](../components/timeline/timeline.css):1|
|border|`border`|`2px solid var(--k-core)`|[components/hanko/hanko.css](../components/hanko/hanko.css):1|
|border|`border`|`2px solid var(--k-ink)`|[templates/dashboard/dashboard.css](../templates/dashboard/dashboard.css):1|
|border|`border`|`2px solid var(--k-zinc-700)`|[components/warp-tunnel/warp-tunnel.css](../components/warp-tunnel/warp-tunnel.css):1|
|border|`border`|`5px solid transparent`|[components/tooltip/tooltip.css](../components/tooltip/tooltip.css):1|
|spacing|`gap`|`9px`|[blocks/app-shell/app-shell.css](../blocks/app-shell/app-shell.css):3<br>[blocks/kanban/kanban.css](../blocks/kanban/kanban.css):1<br>[blocks/logo-cloud/logo-cloud.css](../blocks/logo-cloud/logo-cloud.css):1<br>[blocks/order-confirmation/order-confirmation.css](../blocks/order-confirmation/order-confirmation.css):1<br>[blocks/pricing/pricing.css](../blocks/pricing/pricing.css):2<br>[blocks/settings/settings.css](../blocks/settings/settings.css):1<br>[blocks/site-footer/site-footer.css](../blocks/site-footer/site-footer.css):1<br>[blocks/site-header/site-header.css](../blocks/site-header/site-header.css):2<br>[components/alert-dialog/alert-dialog.css](../components/alert-dialog/alert-dialog.css):1<br>[components/card/card.css](../components/card/card.css):2<br>[components/checkbox/checkbox.css](../components/checkbox/checkbox.css):1<br>[components/collapsible/collapsible.css](../components/collapsible/collapsible.css):1<br>[components/color-picker/color-picker.css](../components/color-picker/color-picker.css):1<br>[components/context-menu/context-menu.css](../components/context-menu/context-menu.css):1<br>[components/drawer/drawer.css](../components/drawer/drawer.css):1<br>[components/dropdown/dropdown.css](../components/dropdown/dropdown.css):1<br>[components/glow-button/glow-button.css](../components/glow-button/glow-button.css):2<br>[components/input/combos.html](../components/input/combos.html):1<br>[components/menubar/menubar.css](../components/menubar/menubar.css):1<br>[components/meteors/meteors.css](../components/meteors/meteors.css):1<br>[components/modal/modal.css](../components/modal/modal.css):1<br>[components/result/result.css](../components/result/result.css):1<br>[components/sidebar/sidebar.css](../components/sidebar/sidebar.css):3<br>[components/speed-dial/speed-dial.css](../components/speed-dial/speed-dial.css):2<br>[components/toast/combos.html](../components/toast/combos.html):1<br>[components/toast/toast.css](../components/toast/toast.css):1<br>[components/transfer/transfer.css](../components/transfer/transfer.css):1<br>[templates/dashboard/dashboard.css](../templates/dashboard/dashboard.css):4<br>[templates/inbox/inbox.css](../templates/inbox/inbox.css):2<br>[templates/product-page/product-page.css](../templates/product-page/product-page.css):2<br>[templates/settings-page/settings-page.css](../templates/settings-page/settings-page.css):1|
|spacing|`gap`|`8px`|[blocks/cookie-consent/cookie-consent.css](../blocks/cookie-consent/cookie-consent.css):1<br>[blocks/kanban/kanban.css](../blocks/kanban/kanban.css):2<br>[blocks/roadmap/roadmap.css](../blocks/roadmap/roadmap.css):2<br>[blocks/site-footer/site-footer.css](../blocks/site-footer/site-footer.css):1<br>[blocks/use-cases/use-cases.css](../blocks/use-cases/use-cases.css):1<br>[components/accordion-gallery/accordion-gallery.css](../components/accordion-gallery/accordion-gallery.css):1<br>[components/avatar/combos.html](../components/avatar/combos.html):2<br>[components/avatar/preview.html](../components/avatar/preview.html):1<br>[components/badge/examples.html](../components/badge/examples.html):2<br>[components/breadcrumbs/breadcrumbs.css](../components/breadcrumbs/breadcrumbs.css):2<br>[components/chip/chip.css](../components/chip/chip.css):1<br>[components/color-picker/color-picker.css](../components/color-picker/color-picker.css):1<br>[components/copy-field/copy-field.css](../components/copy-field/copy-field.css):1<br>[components/data-table/combos.html](../components/data-table/combos.html):3<br>[components/donut-chart/donut-chart.css](../components/donut-chart/donut-chart.css):2<br>[components/field/field.css](../components/field/field.css):1<br>[components/file-upload/file-upload.css](../components/file-upload/file-upload.css):1<br>[components/input-otp/input-otp.css](../components/input-otp/input-otp.css):1<br>[components/particle-word/particle-word.css](../components/particle-word/particle-word.css):1<br>[components/popover/popover.css](../components/popover/popover.css):1<br>[components/radio/radio.css](../components/radio/radio.css):1<br>[components/steps/steps.css](../components/steps/steps.css):1<br>[components/tour/examples.html](../components/tour/examples.html):2<br>[components/tour/preview.html](../components/tour/preview.html):1<br>[components/tour/tour.css](../components/tour/tour.css):1<br>[components/transfer/transfer.css](../components/transfer/transfer.css):2<br>[components/wagara/wagara.css](../components/wagara/wagara.css):2<br>[templates/inbox/inbox.css](../templates/inbox/inbox.css):3|
|spacing|`gap`|`10px`|[blocks/filter-toolbar/filter-toolbar.css](../blocks/filter-toolbar/filter-toolbar.css):1<br>[blocks/integrations/integrations.css](../blocks/integrations/integrations.css):2<br>[blocks/order-confirmation/order-confirmation.css](../blocks/order-confirmation/order-confirmation.css):1<br>[blocks/stat-cards/stat-cards.css](../blocks/stat-cards/stat-cards.css):1<br>[blocks/testimonials/testimonials.css](../blocks/testimonials/testimonials.css):1<br>[components/alert/alert.css](../components/alert/alert.css):1<br>[components/alert/preview.html](../components/alert/preview.html):1<br>[components/aspect-ratio/preview.html](../components/aspect-ratio/preview.html):1<br>[components/badge/examples.html](../components/badge/examples.html):4<br>[components/bar-chart/bar-chart.css](../components/bar-chart/bar-chart.css):2<br>[components/carousel/carousel.css](../components/carousel/carousel.css):1<br>[components/command/command.css](../components/command/command.css):1<br>[components/copy-field/preview.html](../components/copy-field/preview.html):1<br>[components/data-table/data-table.css](../components/data-table/data-table.css):1<br>[components/modal/combos.html](../components/modal/combos.html):1<br>[components/radio/preview.html](../components/radio/preview.html):1<br>[components/scatter-chart/scatter-chart.css](../components/scatter-chart/scatter-chart.css):1<br>[components/scroll-area/scroll-area.css](../components/scroll-area/scroll-area.css):1<br>[components/speed-dial/speed-dial.css](../components/speed-dial/speed-dial.css):1<br>[components/switch/combos.html](../components/switch/combos.html):3<br>[components/tooltip/preview.html](../components/tooltip/preview.html):1<br>[templates/checkout/checkout.css](../templates/checkout/checkout.css):1<br>[templates/inbox/inbox.css](../templates/inbox/inbox.css):2<br>[templates/landing/landing.css](../templates/landing/landing.css):1<br>[templates/product-page/product-page.css](../templates/product-page/product-page.css):2|
|spacing|`gap`|`7px`|[blocks/site-footer/site-footer.css](../blocks/site-footer/site-footer.css):1<br>[components/card/combos.html](../components/card/combos.html):2<br>[components/cascader/cascader.css](../components/cascader/cascader.css):1<br>[components/chip/chip.css](../components/chip/chip.css):1<br>[components/converge/converge.css](../components/converge/converge.css):1<br>[components/data-table/data-table.css](../components/data-table/data-table.css):1<br>[components/dock/dock.css](../components/dock/dock.css):1<br>[components/empty-state/empty-state.css](../components/empty-state/empty-state.css):1<br>[components/field/field.css](../components/field/field.css):1<br>[components/file-upload/file-upload.css](../components/file-upload/file-upload.css):1<br>[components/menubar/preview.html](../components/menubar/preview.html):1<br>[components/meter/preview.html](../components/meter/preview.html):3<br>[components/progress/preview.html](../components/progress/preview.html):2<br>[components/reorder/reorder.css](../components/reorder/reorder.css):1<br>[components/skeleton/preview.html](../components/skeleton/preview.html):1<br>[components/tag-input/tag-input.css](../components/tag-input/tag-input.css):1<br>[components/toggle/toggle.css](../components/toggle/toggle.css):1<br>[components/torn-ticket/torn-ticket.css](../components/torn-ticket/torn-ticket.css):1<br>[components/tree/tree.css](../components/tree/tree.css):1<br>[templates/dashboard/dashboard.css](../templates/dashboard/dashboard.css):1<br>[templates/inbox/inbox.css](../templates/inbox/inbox.css):2<br>[templates/product-page/product-page.css](../templates/product-page/product-page.css):1|
|spacing|`margin-top`|`9px`|[components/alert-dialog/alert-dialog.css](../components/alert-dialog/alert-dialog.css):1<br>[components/carousel-ring/preview.html](../components/carousel-ring/preview.html):1<br>[components/cascader/preview.html](../components/cascader/preview.html):1<br>[components/comparison-slider/preview.html](../components/comparison-slider/preview.html):1<br>[components/dock/preview.html](../components/dock/preview.html):1<br>[components/empty-state/empty-state.css](../components/empty-state/empty-state.css):1<br>[components/funnel-chart/funnel-chart.css](../components/funnel-chart/funnel-chart.css):1<br>[components/glow-cards/preview.html](../components/glow-cards/preview.html):1<br>[components/gravity-playground/preview.html](../components/gravity-playground/preview.html):1<br>[components/hanko/preview.html](../components/hanko/preview.html):1<br>[components/horizontal-reel/preview.html](../components/horizontal-reel/preview.html):1<br>[components/kaleidoscope/preview.html](../components/kaleidoscope/preview.html):1<br>[components/magnet/preview.html](../components/magnet/preview.html):1<br>[components/modal/modal.css](../components/modal/modal.css):1<br>[components/particle-word/preview.html](../components/particle-word/preview.html):1<br>[components/scatter-chart/scatter-chart.css](../components/scatter-chart/scatter-chart.css):1<br>[components/sparkles/preview.html](../components/sparkles/preview.html):1<br>[components/stacking-cards/preview.html](../components/stacking-cards/preview.html):1<br>[components/time-picker/preview.html](../components/time-picker/preview.html):1<br>[components/wagara/wagara.css](../components/wagara/wagara.css):3<br>[templates/product-page/product-page.css](../templates/product-page/product-page.css):1|
|spacing|`gap`|`12px`|[blocks/app-shell/app-shell.css](../blocks/app-shell/app-shell.css):2<br>[blocks/invoice/invoice.css](../blocks/invoice/invoice.css):1<br>[blocks/pricing/pricing.css](../blocks/pricing/pricing.css):1<br>[blocks/stat-cards/stat-cards.css](../blocks/stat-cards/stat-cards.css):1<br>[blocks/testimonials/testimonials.css](../blocks/testimonials/testimonials.css):1<br>[blocks/use-cases/use-cases.css](../blocks/use-cases/use-cases.css):1<br>[components/accordion/accordion.css](../components/accordion/accordion.css):1<br>[components/card/card.css](../components/card/card.css):1<br>[components/carousel/carousel.css](../components/carousel/carousel.css):1<br>[components/funnel-chart/funnel-chart.css](../components/funnel-chart/funnel-chart.css):1<br>[components/list/list.css](../components/list/list.css):1<br>[components/separator/preview.html](../components/separator/preview.html):1<br>[components/separator/separator.css](../components/separator/separator.css):1<br>[components/skeleton/preview.html](../components/skeleton/preview.html):2<br>[components/sparkline/sparkline.css](../components/sparkline/sparkline.css):1<br>[components/transfer/transfer.css](../components/transfer/transfer.css):1<br>[templates/blog-article/blog-article.css](../templates/blog-article/blog-article.css):1<br>[templates/checkout/checkout.css](../templates/checkout/checkout.css):2<br>[templates/inbox/inbox.css](../templates/inbox/inbox.css):1|
|spacing|`gap`|`14px`|[blocks/integrations/integrations.css](../blocks/integrations/integrations.css):1<br>[blocks/invoice/invoice.css](../blocks/invoice/invoice.css):2<br>[blocks/roadmap/roadmap.css](../blocks/roadmap/roadmap.css):1<br>[blocks/settings/settings.css](../blocks/settings/settings.css):2<br>[blocks/team/team.css](../blocks/team/team.css):1<br>[blocks/use-cases/use-cases.css](../blocks/use-cases/use-cases.css):1<br>[components/button-group/preview.html](../components/button-group/preview.html):1<br>[components/card/combos.html](../components/card/combos.html):1<br>[components/descriptions/descriptions.css](../components/descriptions/descriptions.css):1<br>[components/input-group/preview.html](../components/input-group/preview.html):1<br>[components/input/examples.html](../components/input/examples.html):2<br>[components/kbd/preview.html](../components/kbd/preview.html):1<br>[components/radar-chart/radar-chart.css](../components/radar-chart/radar-chart.css):1<br>[components/scatter-chart/scatter-chart.css](../components/scatter-chart/scatter-chart.css):1<br>[components/segmented/preview.html](../components/segmented/preview.html):1<br>[components/toggle/preview.html](../components/toggle/preview.html):1<br>[templates/dashboard/dashboard.css](../templates/dashboard/dashboard.css):1<br>[templates/inbox/inbox.css](../templates/inbox/inbox.css):1<br>[templates/settings-page/settings-page.css](../templates/settings-page/settings-page.css):1|
|spacing|`gap`|`16px`|[blocks/app-shell/app-shell.css](../blocks/app-shell/app-shell.css):1<br>[blocks/pricing/pricing.css](../blocks/pricing/pricing.css):1<br>[blocks/settings/settings.css](../blocks/settings/settings.css):1<br>[blocks/site-footer/site-footer.css](../blocks/site-footer/site-footer.css):1<br>[components/hanko/hanko.css](../components/hanko/hanko.css):1<br>[components/liquid-button/preview.html](../components/liquid-button/preview.html):1<br>[components/pagination/preview.html](../components/pagination/preview.html):1<br>[components/progress/preview.html](../components/progress/preview.html):1<br>[components/qr-code/examples.html](../components/qr-code/examples.html):1<br>[components/separator/preview.html](../components/separator/preview.html):1<br>[components/slider/preview.html](../components/slider/preview.html):1<br>[components/tracing-beam/tracing-beam.css](../components/tracing-beam/tracing-beam.css):1<br>[templates/dashboard/dashboard.css](../templates/dashboard/dashboard.css):2<br>[templates/landing/landing.css](../templates/landing/landing.css):1<br>[templates/settings-page/settings-page.css](../templates/settings-page/settings-page.css):3|
|spacing|`margin-top`|`5px`|[blocks/invoice/invoice.css](../blocks/invoice/invoice.css):1<br>[blocks/login/login.css](../blocks/login/login.css):1<br>[blocks/order-confirmation/order-confirmation.css](../blocks/order-confirmation/order-confirmation.css):1<br>[blocks/pricing/pricing.css](../blocks/pricing/pricing.css):1<br>[blocks/settings/settings.css](../blocks/settings/settings.css):1<br>[components/beam-border/preview.html](../components/beam-border/preview.html):1<br>[components/bottom-navigation/examples.html](../components/bottom-navigation/examples.html):1<br>[components/bottom-navigation/preview.html](../components/bottom-navigation/preview.html):1<br>[components/carousel/carousel.css](../components/carousel/carousel.css):1<br>[components/checkbox/combos.html](../components/checkbox/combos.html):1<br>[components/glow-cards/glow-cards.css](../components/glow-cards/glow-cards.css):1<br>[components/hanko/hanko.css](../components/hanko/hanko.css):1<br>[components/meter/meter.css](../components/meter/meter.css):1<br>[components/qr-code/preview.html](../components/qr-code/preview.html):1<br>[components/sparkles/examples.html](../components/sparkles/examples.html):1<br>[components/stat/stat.css](../components/stat/stat.css):1<br>[templates/settings-page/settings-page.css](../templates/settings-page/settings-page.css):2|
|spacing|`gap`|`2px`|[blocks/app-shell/app-shell.css](../blocks/app-shell/app-shell.css):1<br>[blocks/testimonials/testimonials.css](../blocks/testimonials/testimonials.css):1<br>[components/calendar/calendar.css](../components/calendar/calendar.css):1<br>[components/date-picker/date-picker.css](../components/date-picker/date-picker.css):1<br>[components/menubar/menubar.css](../components/menubar/menubar.css):1<br>[components/scrollspy/scrollspy.css](../components/scrollspy/scrollspy.css):1<br>[components/segmented/segmented.css](../components/segmented/segmented.css):1<br>[components/sidebar/sidebar.css](../components/sidebar/sidebar.css):2<br>[components/slider/preview.html](../components/slider/preview.html):2<br>[components/tabs/tabs.css](../components/tabs/tabs.css):1<br>[components/time-picker/time-picker.css](../components/time-picker/time-picker.css):1<br>[templates/dashboard/dashboard.css](../templates/dashboard/dashboard.css):1<br>[templates/inbox/inbox.css](../templates/inbox/inbox.css):1<br>[templates/settings-page/settings-page.css](../templates/settings-page/settings-page.css):1|
|spacing|`gap`|`6px`|[blocks/use-cases/use-cases.css](../blocks/use-cases/use-cases.css):1<br>[components/aspect-ratio/aspect-ratio.css](../components/aspect-ratio/aspect-ratio.css):1<br>[components/badge/badge.css](../components/badge/badge.css):1<br>[components/bar-chart/bar-chart.css](../components/bar-chart/bar-chart.css):1<br>[components/carousel-ring/carousel-ring.css](../components/carousel-ring/carousel-ring.css):1<br>[components/carousel/carousel.css](../components/carousel/carousel.css):1<br>[components/converge/converge.css](../components/converge/converge.css):1<br>[components/field/field.css](../components/field/field.css):1<br>[components/follow-frame/follow-frame.css](../components/follow-frame/follow-frame.css):1<br>[components/input/combos.html](../components/input/combos.html):1<br>[components/input/input.css](../components/input/input.css):1<br>[components/navigation-menu/navigation-menu.css](../components/navigation-menu/navigation-menu.css):1<br>[components/stepper/preview.html](../components/stepper/preview.html):2<br>[components/textarea/preview.html](../components/textarea/preview.html):1<br>[components/time-picker/time-picker.css](../components/time-picker/time-picker.css):1|
|spacing|`gap`|`11px`|[components/avatar/combos.html](../components/avatar/combos.html):1<br>[components/checkbox/combos.html](../components/checkbox/combos.html):1<br>[components/checkbox/examples.html](../components/checkbox/examples.html):3<br>[components/command/command.css](../components/command/command.css):1<br>[components/file-upload/file-upload.css](../components/file-upload/file-upload.css):1<br>[components/glass-panel/glass-panel.css](../components/glass-panel/glass-panel.css):1<br>[components/hover-card/preview.html](../components/hover-card/preview.html):1<br>[components/navigation-menu/navigation-menu.css](../components/navigation-menu/navigation-menu.css):1<br>[components/reorder/reorder.css](../components/reorder/reorder.css):1<br>[components/switch/switch.css](../components/switch/switch.css):1<br>[components/toast/toast.css](../components/toast/toast.css):1<br>[templates/blog-article/blog-article.css](../templates/blog-article/blog-article.css):1<br>[templates/inbox/inbox.css](../templates/inbox/inbox.css):1|
|spacing|`margin-top`|`16px`|[blocks/faq/faq.css](../blocks/faq/faq.css):1<br>[blocks/login/login.css](../blocks/login/login.css):2<br>[blocks/order-confirmation/order-confirmation.css](../blocks/order-confirmation/order-confirmation.css):1<br>[blocks/pricing/pricing.css](../blocks/pricing/pricing.css):1<br>[blocks/settings/settings.css](../blocks/settings/settings.css):3<br>[components/hanko/hanko.css](../components/hanko/hanko.css):1<br>[components/kintsugi-card/kintsugi-card.css](../components/kintsugi-card/kintsugi-card.css):1<br>[components/noren/noren.css](../components/noren/noren.css):1<br>[components/spotlight/preview.html](../components/spotlight/preview.html):1<br>[templates/blog-article/blog-article.css](../templates/blog-article/blog-article.css):1<br>[templates/settings-page/settings-page.css](../templates/settings-page/settings-page.css):1|
|spacing|`margin-top`|`8px`|[blocks/team/team.css](../blocks/team/team.css):1<br>[components/accordion/accordion.css](../components/accordion/accordion.css):1<br>[components/avatar/combos.html](../components/avatar/combos.html):1<br>[components/bounce-letters/preview.html](../components/bounce-letters/preview.html):1<br>[components/candlestick-chart/candlestick-chart.css](../components/candlestick-chart/candlestick-chart.css):1<br>[components/glass-panel/glass-panel.css](../components/glass-panel/glass-panel.css):1<br>[components/line-chart/line-chart.css](../components/line-chart/line-chart.css):1<br>[components/liquid-button/preview.html](../components/liquid-button/preview.html):1<br>[components/navigation-menu/preview.html](../components/navigation-menu/preview.html):1<br>[components/particle-net/particle-net.css](../components/particle-net/particle-net.css):1<br>[components/result/result.css](../components/result/result.css):1<br>[components/scramble/preview.html](../components/scramble/preview.html):1<br>[components/spotlight/preview.html](../components/spotlight/preview.html):1<br>[templates/settings-page/settings-page.css](../templates/settings-page/settings-page.css):1|
|spacing|`padding`|`20px`|[blocks/team/team.css](../blocks/team/team.css):1<br>[components/beam-border/beam-border.css](../components/beam-border/beam-border.css):1<br>[components/drawer/drawer.css](../components/drawer/drawer.css):1<br>[components/glass-panel/preview.html](../components/glass-panel/preview.html):1<br>[components/hanko/hanko.css](../components/hanko/hanko.css):1<br>[components/reorder/preview.html](../components/reorder/preview.html):1<br>[components/sidebar/examples.html](../components/sidebar/examples.html):2<br>[components/sidebar/preview.html](../components/sidebar/preview.html):1<br>[components/stacking-cards/stacking-cards.css](../components/stacking-cards/stacking-cards.css):1<br>[templates/checkout/checkout.css](../templates/checkout/checkout.css):2<br>[templates/product-page/product-page.css](../templates/product-page/product-page.css):1|
|spacing|`gap`|`13px`|[blocks/kanban/kanban.css](../blocks/kanban/kanban.css):1<br>[components/glow-cards/glow-cards.css](../components/glow-cards/glow-cards.css):1<br>[components/horizontal-reel/horizontal-reel.css](../components/horizontal-reel/horizontal-reel.css):1<br>[components/jelly-buttons/preview.html](../components/jelly-buttons/preview.html):1<br>[components/switch/combos.html](../components/switch/combos.html):1<br>[components/switch/examples.html](../components/switch/examples.html):3<br>[components/tabs/combos.html](../components/tabs/combos.html):1<br>[components/tategaki/tategaki.css](../components/tategaki/tategaki.css):1<br>[templates/blog-article/blog-article.css](../templates/blog-article/blog-article.css):1<br>[templates/product-page/product-page.css](../templates/product-page/product-page.css):1|
|spacing|`margin-top`|`6px`|[blocks/faq/faq.css](../blocks/faq/faq.css):1<br>[blocks/use-cases/use-cases.css](../blocks/use-cases/use-cases.css):1<br>[components/card/examples.html](../components/card/examples.html):2<br>[components/jelly-buttons/preview.html](../components/jelly-buttons/preview.html):1<br>[components/popover/popover.css](../components/popover/popover.css):1<br>[components/radar-chart/radar-chart.css](../components/radar-chart/radar-chart.css):1<br>[components/sidebar/examples.html](../components/sidebar/examples.html):2<br>[components/sidebar/preview.html](../components/sidebar/preview.html):1<br>[components/stat/stat.css](../components/stat/stat.css):1|
|spacing|`margin-top`|`7px`|[blocks/pricing/pricing.css](../blocks/pricing/pricing.css):1<br>[components/aurora/aurora.css](../components/aurora/aurora.css):1<br>[components/beam-border/preview.html](../components/beam-border/preview.html):1<br>[components/dual-range/dual-range.css](../components/dual-range/dual-range.css):1<br>[components/sparkline/examples.html](../components/sparkline/examples.html):3<br>[components/sparkline/preview.html](../components/sparkline/preview.html):2<br>[templates/checkout/checkout.css](../templates/checkout/checkout.css):1|
|spacing|`margin-top`|`14px`|[blocks/faq/faq.css](../blocks/faq/faq.css):1<br>[blocks/login/login.css](../blocks/login/login.css):2<br>[blocks/testimonials/testimonials.css](../blocks/testimonials/testimonials.css):1<br>[components/popover/popover.css](../components/popover/popover.css):1<br>[components/tabs/tabs.css](../components/tabs/tabs.css):1<br>[components/tour/tour.css](../components/tour/tour.css):1<br>[templates/product-page/product-page.css](../templates/product-page/product-page.css):1<br>[templates/settings-page/settings-page.css](../templates/settings-page/settings-page.css):1|
|spacing|`margin-top`|`18px`|[blocks/login/login.css](../blocks/login/login.css):2<br>[blocks/order-confirmation/order-confirmation.css](../blocks/order-confirmation/order-confirmation.css):2<br>[blocks/settings/settings.css](../blocks/settings/settings.css):1<br>[components/result/result.css](../components/result/result.css):1<br>[templates/settings-page/settings-page.css](../templates/settings-page/settings-page.css):3|
|spacing|`margin-top`|`4px`|[blocks/kanban/kanban.css](../blocks/kanban/kanban.css):1<br>[blocks/roadmap/roadmap.css](../blocks/roadmap/roadmap.css):1<br>[components/avatar/combos.html](../components/avatar/combos.html):1<br>[components/hover-card/hover-card.css](../components/hover-card/hover-card.css):1<br>[components/qr-code/examples.html](../components/qr-code/examples.html):2<br>[templates/blog-article/blog-article.css](../templates/blog-article/blog-article.css):1<br>[templates/landing/landing.css](../templates/landing/landing.css):1<br>[templates/settings-page/settings-page.css](../templates/settings-page/settings-page.css):1|
|spacing|`padding`|`16px`|[blocks/stat-cards/stat-cards.css](../blocks/stat-cards/stat-cards.css):1<br>[components/bottom-navigation/examples.html](../components/bottom-navigation/examples.html):1<br>[components/bottom-navigation/preview.html](../components/bottom-navigation/preview.html):1<br>[components/context-menu/context-menu.css](../components/context-menu/context-menu.css):1<br>[components/glass-panel/glass-panel.css](../components/glass-panel/glass-panel.css):1<br>[components/horizontal-reel/horizontal-reel.css](../components/horizontal-reel/horizontal-reel.css):1<br>[components/popover/popover.css](../components/popover/popover.css):1<br>[components/qr-code/examples.html](../components/qr-code/examples.html):1<br>[components/tour/tour.css](../components/tour/tour.css):1|
|spacing|`gap`|`26px`|[blocks/site-header/site-header.css](../blocks/site-header/site-header.css):1<br>[components/burst-button/preview.html](../components/burst-button/preview.html):1<br>[components/sparkline/examples.html](../components/sparkline/examples.html):3<br>[components/sparkline/preview.html](../components/sparkline/preview.html):1<br>[components/stepper/preview.html](../components/stepper/preview.html):1|
|spacing|`margin-bottom`|`12px`|[blocks/order-confirmation/order-confirmation.css](../blocks/order-confirmation/order-confirmation.css):1<br>[blocks/roadmap/roadmap.css](../blocks/roadmap/roadmap.css):1<br>[components/candlestick-chart/candlestick-chart.css](../components/candlestick-chart/candlestick-chart.css):1<br>[components/donut-chart/donut-chart.css](../components/donut-chart/donut-chart.css):1<br>[components/heatmap/heatmap.css](../components/heatmap/heatmap.css):1<br>[components/line-chart/line-chart.css](../components/line-chart/line-chart.css):1<br>[templates/inbox/inbox.css](../templates/inbox/inbox.css):1|
|spacing|`padding`|`14px`|[components/calendar/calendar.css](../components/calendar/calendar.css):1<br>[components/date-picker/date-picker.css](../components/date-picker/date-picker.css):1<br>[components/particle-word/particle-word.css](../components/particle-word/particle-word.css):1<br>[components/sidebar/examples.html](../components/sidebar/examples.html):1<br>[components/stacking-cards/stacking-cards.css](../components/stacking-cards/stacking-cards.css):1<br>[templates/blog-article/blog-article.css](../templates/blog-article/blog-article.css):1<br>[templates/product-page/product-page.css](../templates/product-page/product-page.css):1|
|spacing|`padding`|`26px`|[blocks/site-footer/site-footer.css](../blocks/site-footer/site-footer.css):1<br>[components/alert-dialog/alert-dialog.css](../components/alert-dialog/alert-dialog.css):1<br>[components/magnet/magnet.css](../components/magnet/magnet.css):1<br>[components/modal/modal.css](../components/modal/modal.css):1<br>[components/tategaki/tategaki.css](../components/tategaki/tategaki.css):1<br>[templates/checkout/checkout.css](../templates/checkout/checkout.css):1<br>[templates/product-page/product-page.css](../templates/product-page/product-page.css):1|
|spacing|`padding`|`7px 9px`|[components/cascader/cascader.css](../components/cascader/cascader.css):1<br>[components/menubar/menubar.css](../components/menubar/menubar.css):1<br>[components/split-panel/split-panel.css](../components/split-panel/split-panel.css):1<br>[components/tag-input/tag-input.css](../components/tag-input/tag-input.css):1<br>[components/transfer/transfer.css](../components/transfer/transfer.css):1<br>[templates/dashboard/dashboard.css](../templates/dashboard/dashboard.css):1<br>[templates/inbox/inbox.css](../templates/inbox/inbox.css):1|
|spacing|`gap`|`20px`|[blocks/site-header/site-header.css](../blocks/site-header/site-header.css):1<br>[components/counter/preview.html](../components/counter/preview.html):1<br>[components/donut-chart/donut-chart.css](../components/donut-chart/donut-chart.css):1<br>[components/glow-button/preview.html](../components/glow-button/preview.html):1<br>[components/spinner/preview.html](../components/spinner/preview.html):1<br>[components/stat/preview.html](../components/stat/preview.html):1|
|spacing|`margin-bottom`|`18px`|[blocks/invoice/invoice.css](../blocks/invoice/invoice.css):2<br>[blocks/logo-cloud/logo-cloud.css](../blocks/logo-cloud/logo-cloud.css):1<br>[components/typeset/typeset.css](../components/typeset/typeset.css):1<br>[templates/checkout/checkout.css](../templates/checkout/checkout.css):1<br>[templates/product-page/product-page.css](../templates/product-page/product-page.css):1|
|spacing|`margin-top`|`10px`|[blocks/kanban/kanban.css](../blocks/kanban/kanban.css):1<br>[blocks/pricing/pricing.css](../blocks/pricing/pricing.css):1<br>[blocks/site-footer/site-footer.css](../blocks/site-footer/site-footer.css):1<br>[components/kaleidoscope/kaleidoscope.css](../components/kaleidoscope/kaleidoscope.css):1<br>[components/particle-word/particle-word.css](../components/particle-word/particle-word.css):1<br>[components/spotlight/examples.html](../components/spotlight/examples.html):1|
|spacing|`margin-top`|`12px`|[blocks/invoice/invoice.css](../blocks/invoice/invoice.css):1<br>[blocks/use-cases/preview.html](../blocks/use-cases/preview.html):2<br>[components/carousel/carousel.css](../components/carousel/carousel.css):1<br>[components/menubar/preview.html](../components/menubar/preview.html):1<br>[components/spotlight/examples.html](../components/spotlight/examples.html):1|
|spacing|`margin-top`|`3px`|[blocks/invoice/invoice.css](../blocks/invoice/invoice.css):1<br>[components/card/card.css](../components/card/card.css):1<br>[components/counter/preview.html](../components/counter/preview.html):3<br>[templates/dashboard/dashboard.css](../templates/dashboard/dashboard.css):1|
|spacing|`padding`|`8px 0`|[blocks/order-confirmation/order-confirmation.css](../blocks/order-confirmation/order-confirmation.css):1<br>[blocks/site-header/site-header.css](../blocks/site-header/site-header.css):1<br>[components/jelly-buttons/preview.html](../components/jelly-buttons/preview.html):1<br>[components/liquid-button/preview.html](../components/liquid-button/preview.html):1<br>[components/tilt-card/tilt-card.css](../components/tilt-card/tilt-card.css):1<br>[templates/checkout/checkout.css](../templates/checkout/checkout.css):1|
|spacing|`gap`|`4px`|[components/heatmap/heatmap.css](../components/heatmap/heatmap.css):1<br>[components/navigation-menu/navigation-menu.css](../components/navigation-menu/navigation-menu.css):1<br>[components/pagination/pagination.css](../components/pagination/pagination.css):1<br>[templates/dashboard/dashboard.css](../templates/dashboard/dashboard.css):1<br>[templates/inbox/inbox.css](../templates/inbox/inbox.css):1|
|spacing|`gap`|`5px`|[components/data-table/data-table.css](../components/data-table/data-table.css):1<br>[components/horizontal-reel/horizontal-reel.css](../components/horizontal-reel/horizontal-reel.css):1<br>[components/noren/noren.css](../components/noren/noren.css):1<br>[components/toggle/toggle.css](../components/toggle/toggle.css):1<br>[components/tour/tour.css](../components/tour/tour.css):1|
|spacing|`margin-bottom`|`5px`|[blocks/invoice/invoice.css](../blocks/invoice/invoice.css):1<br>[components/date-picker/date-picker.css](../components/date-picker/date-picker.css):1<br>[components/scrollspy/scrollspy.css](../components/scrollspy/scrollspy.css):1<br>[components/tracing-beam/tracing-beam.css](../components/tracing-beam/tracing-beam.css):1<br>[templates/blog-article/blog-article.css](../templates/blog-article/blog-article.css):1|
|spacing|`margin-top`|`1px`|[blocks/integrations/integrations.css](../blocks/integrations/integrations.css):1<br>[components/alert/alert.css](../components/alert/alert.css):1<br>[components/gauge/gauge.css](../components/gauge/gauge.css):1<br>[components/list/list.css](../components/list/list.css):1<br>[templates/inbox/inbox.css](../templates/inbox/inbox.css):1|
|spacing|`padding`|`15px`|[blocks/integrations/integrations.css](../blocks/integrations/integrations.css):1<br>[blocks/roadmap/roadmap.css](../blocks/roadmap/roadmap.css):1<br>[components/hover-card/hover-card.css](../components/hover-card/hover-card.css):1<br>[components/split-panel/split-panel.css](../components/split-panel/split-panel.css):2|
|spacing|`padding`|`24px`|[blocks/invoice/invoice.css](../blocks/invoice/invoice.css):1<br>[blocks/order-confirmation/order-confirmation.css](../blocks/order-confirmation/order-confirmation.css):1<br>[blocks/settings/settings.css](../blocks/settings/settings.css):1<br>[components/shine-text/examples.html](../components/shine-text/examples.html):1<br>[templates/settings-page/settings-page.css](../templates/settings-page/settings-page.css):1|
|spacing|`top`|`calc(100% + 8px)`|[components/cascader/cascader.css](../components/cascader/cascader.css):1<br>[components/date-picker/date-picker.css](../components/date-picker/date-picker.css):1<br>[components/navigation-menu/navigation-menu.css](../components/navigation-menu/navigation-menu.css):1<br>[components/popover/popover.css](../components/popover/popover.css):1<br>[components/time-picker/time-picker.css](../components/time-picker/time-picker.css):1|
|spacing|`bottom`|`4px`|[components/calendar/calendar.css](../components/calendar/calendar.css):1<br>[components/date-picker/date-picker.css](../components/date-picker/date-picker.css):1<br>[components/goo-tabs/goo-tabs.css](../components/goo-tabs/goo-tabs.css):1<br>[components/tracing-beam/tracing-beam.css](../components/tracing-beam/tracing-beam.css):1|
|spacing|`gap`|`22px`|[components/avatar/preview.html](../components/avatar/preview.html):1<br>[components/kintsugi-card/kintsugi-card.css](../components/kintsugi-card/kintsugi-card.css):1<br>[components/scrollspy/scrollspy.css](../components/scrollspy/scrollspy.css):1<br>[templates/checkout/checkout.css](../templates/checkout/checkout.css):1|
|spacing|`gap`|`3px`|[components/bottom-navigation/bottom-navigation.css](../components/bottom-navigation/bottom-navigation.css):1<br>[components/heatmap/heatmap.css](../components/heatmap/heatmap.css):1<br>[components/rating/rating.css](../components/rating/rating.css):1<br>[components/stat/stat.css](../components/stat/stat.css):1|
|spacing|`margin-bottom`|`9px`|[blocks/roadmap/roadmap.css](../blocks/roadmap/roadmap.css):1<br>[components/rating/preview.html](../components/rating/preview.html):1<br>[components/split-panel/split-panel.css](../components/split-panel/split-panel.css):1<br>[templates/blog-article/blog-article.css](../templates/blog-article/blog-article.css):1|
|spacing|`margin-top`|`20px`|[blocks/invoice/invoice.css](../blocks/invoice/invoice.css):1<br>[blocks/pricing/pricing.css](../blocks/pricing/pricing.css):1<br>[templates/product-page/product-page.css](../templates/product-page/product-page.css):2|
|spacing|`margin-top`|`2px`|[blocks/settings/settings.css](../blocks/settings/settings.css):1<br>[components/toast/toast.css](../components/toast/toast.css):1<br>[templates/inbox/inbox.css](../templates/inbox/inbox.css):1<br>[templates/settings-page/settings-page.css](../templates/settings-page/settings-page.css):1|
|spacing|`padding`|`12px`|[blocks/filter-toolbar/filter-toolbar.css](../blocks/filter-toolbar/filter-toolbar.css):1<br>[components/kaleidoscope/kaleidoscope.css](../components/kaleidoscope/kaleidoscope.css):1<br>[components/qr-code/qr-code.css](../components/qr-code/qr-code.css):1<br>[templates/inbox/inbox.css](../templates/inbox/inbox.css):1|
|spacing|`padding`|`12px 14px`|[blocks/order-confirmation/order-confirmation.css](../blocks/order-confirmation/order-confirmation.css):1<br>[components/alert/alert.css](../components/alert/alert.css):1<br>[components/data-table/data-table.css](../components/data-table/data-table.css):1<br>[components/table/table.css](../components/table/table.css):1|
|spacing|`padding`|`18px`|[components/carousel/carousel.css](../components/carousel/carousel.css):1<br>[components/dock/preview.html](../components/dock/preview.html):1<br>[components/glow-cards/glow-cards.css](../components/glow-cards/glow-cards.css):1<br>[components/tour/tour.css](../components/tour/tour.css):1|
|spacing|`padding`|`22px`|[blocks/use-cases/use-cases.css](../blocks/use-cases/use-cases.css):1<br>[components/kintsugi-card/kintsugi-card.css](../components/kintsugi-card/kintsugi-card.css):1<br>[components/spotlight/spotlight.css](../components/spotlight/spotlight.css):1<br>[components/tilt-card/tilt-card.css](../components/tilt-card/tilt-card.css):1|
|spacing|`padding`|`2px`|[components/cascader/cascader.css](../components/cascader/cascader.css):1<br>[components/glow-button/glow-button.css](../components/glow-button/glow-button.css):2<br>[components/rating/rating.css](../components/rating/rating.css):1|
|spacing|`padding`|`5px`|[components/context-menu/context-menu.css](../components/context-menu/context-menu.css):1<br>[components/dropdown/dropdown.css](../components/dropdown/dropdown.css):1<br>[components/menubar/menubar.css](../components/menubar/menubar.css):1<br>[components/transfer/transfer.css](../components/transfer/transfer.css):1|
|spacing|`padding`|`8px 10px`|[blocks/app-shell/app-shell.css](../blocks/app-shell/app-shell.css):1<br>[components/context-menu/context-menu.css](../components/context-menu/context-menu.css):1<br>[components/dropdown/dropdown.css](../components/dropdown/dropdown.css):1<br>[components/sidebar/sidebar.css](../components/sidebar/sidebar.css):1|
|spacing|`top`|`4px`|[components/goo-tabs/goo-tabs.css](../components/goo-tabs/goo-tabs.css):1<br>[components/tracing-beam/tracing-beam.css](../components/tracing-beam/tracing-beam.css):3|
|spacing|`bottom`|`12px`|[components/accordion-gallery/accordion-gallery.css](../components/accordion-gallery/accordion-gallery.css):1<br>[components/fireworks/fireworks.css](../components/fireworks/fireworks.css):1<br>[components/follow-frame/follow-frame.css](../components/follow-frame/follow-frame.css):1|
|spacing|`gap`|`18px`|[components/field/preview.html](../components/field/preview.html):1<br>[components/meter/preview.html](../components/meter/preview.html):1<br>[components/qr-code/preview.html](../components/qr-code/preview.html):1|
|spacing|`left`|`16px`|[components/converge/converge.css](../components/converge/converge.css):1<br>[components/follow-frame/follow-frame.css](../components/follow-frame/follow-frame.css):1<br>[components/speed-dial/preview.html](../components/speed-dial/preview.html):1|
|spacing|`margin-bottom`|`10px`|[blocks/site-footer/site-footer.css](../blocks/site-footer/site-footer.css):1<br>[components/calendar/calendar.css](../components/calendar/calendar.css):1<br>[components/date-picker/date-picker.css](../components/date-picker/date-picker.css):1|
|spacing|`margin-bottom`|`11px`|[blocks/site-footer/site-footer.css](../blocks/site-footer/site-footer.css):1<br>[blocks/testimonials/testimonials.css](../blocks/testimonials/testimonials.css):1<br>[components/glow-cards/glow-cards.css](../components/glow-cards/glow-cards.css):1|
|spacing|`margin-bottom`|`14px`|[components/bar-chart/bar-chart.css](../components/bar-chart/bar-chart.css):1<br>[components/stacking-cards/stacking-cards.css](../components/stacking-cards/stacking-cards.css):1<br>[templates/checkout/checkout.css](../templates/checkout/checkout.css):1|
|spacing|`margin-bottom`|`16px`|[blocks/integrations/integrations.css](../blocks/integrations/integrations.css):1<br>[templates/checkout/checkout.css](../templates/checkout/checkout.css):1<br>[templates/product-page/product-page.css](../templates/product-page/product-page.css):1|
|spacing|`margin-top`|`11px`|[components/heatmap/heatmap.css](../components/heatmap/heatmap.css):1<br>[components/wagara/wagara.css](../components/wagara/wagara.css):1<br>[templates/checkout/checkout.css](../templates/checkout/checkout.css):1|
|spacing|`margin-top`|`22px`|[blocks/settings/settings.css](../blocks/settings/settings.css):1<br>[components/alert-dialog/alert-dialog.css](../components/alert-dialog/alert-dialog.css):1<br>[components/modal/modal.css](../components/modal/modal.css):1|
|spacing|`padding`|`0 12px`|[components/copy-field/copy-field.css](../components/copy-field/copy-field.css):1<br>[components/glow-button/glow-button.css](../components/glow-button/glow-button.css):1<br>[components/input/input.css](../components/input/input.css):1|
|spacing|`padding`|`0 6px`|[components/menubar/preview.html](../components/menubar/preview.html):1<br>[components/pagination/preview.html](../components/pagination/preview.html):1<br>[components/stepper/stepper.css](../components/stepper/stepper.css):1|
|spacing|`padding`|`10px`|[blocks/kanban/kanban.css](../blocks/kanban/kanban.css):1<br>[components/carousel-ring/carousel-ring.css](../components/carousel-ring/carousel-ring.css):1<br>[components/time-picker/time-picker.css](../components/time-picker/time-picker.css):1|
|spacing|`padding`|`10px 12px`|[components/reorder/reorder.css](../components/reorder/reorder.css):1<br>[components/textarea/textarea.css](../components/textarea/textarea.css):1<br>[components/transfer/transfer.css](../components/transfer/transfer.css):1|
|spacing|`padding`|`11px 14px`|[blocks/plan-compare/plan-compare.css](../blocks/plan-compare/plan-compare.css):1<br>[components/data-table/data-table.css](../components/data-table/data-table.css):2|
|spacing|`padding`|`14px 8px`|[components/sidebar/sidebar.css](../components/sidebar/sidebar.css):1<br>[components/torn-ticket/preview.html](../components/torn-ticket/preview.html):1<br>[components/torn-ticket/torn-ticket.css](../components/torn-ticket/torn-ticket.css):1|
|spacing|`padding`|`18px 20px`|[blocks/app-shell/app-shell.css](../blocks/app-shell/app-shell.css):1<br>[components/drawer/drawer.css](../components/drawer/drawer.css):1<br>[templates/dashboard/dashboard.css](../templates/dashboard/dashboard.css):1|
|spacing|`padding`|`3px`|[components/segmented/segmented.css](../components/segmented/segmented.css):1<br>[components/tabs/tabs.css](../components/tabs/tabs.css):1<br>[components/wagara/wagara.css](../components/wagara/wagara.css):1|
|spacing|`padding`|`9px 10px`|[components/command/command.css](../components/command/command.css):1<br>[components/dock/dock.css](../components/dock/dock.css):1<br>[components/navigation-menu/navigation-menu.css](../components/navigation-menu/navigation-menu.css):1|
|spacing|`top`|`3px`|[components/switch/switch.css](../components/switch/switch.css):1<br>[components/tabs/tabs.css](../components/tabs/tabs.css):1<br>[components/timeline/timeline.css](../components/timeline/timeline.css):1|
|spacing|`bottom`|`14px`|[blocks/cookie-consent/cookie-consent.css](../blocks/cookie-consent/cookie-consent.css):1<br>[templates/inbox/inbox.css](../templates/inbox/inbox.css):1|
|spacing|`bottom`|`18px`|[components/speed-dial/speed-dial.css](../components/speed-dial/speed-dial.css):1<br>[components/toast/toast.css](../components/toast/toast.css):1|
|spacing|`gap`|`34px`|[components/tategaki/tategaki.css](../components/tategaki/tategaki.css):1<br>[templates/blog-article/blog-article.css](../templates/blog-article/blog-article.css):1|
|spacing|`left`|`10px`|[components/comparison-slider/comparison-slider.css](../components/comparison-slider/comparison-slider.css):1<br>[components/input/input.css](../components/input/input.css):1|
|spacing|`left`|`18px`|[components/tour/examples.html](../components/tour/examples.html):1<br>[components/tour/preview.html](../components/tour/preview.html):1|
|spacing|`left`|`7px`|[components/tracing-beam/tracing-beam.css](../components/tracing-beam/tracing-beam.css):2|
|spacing|`margin`|`0 0 14px`|[components/typeset/typeset.css](../components/typeset/typeset.css):2|
|spacing|`margin`|`16px 10px 6px`|[components/sidebar/sidebar.css](../components/sidebar/sidebar.css):1<br>[templates/inbox/inbox.css](../templates/inbox/inbox.css):1|
|spacing|`margin`|`18px 0`|[components/typeset/typeset.css](../components/typeset/typeset.css):1<br>[templates/blog-article/blog-article.css](../templates/blog-article/blog-article.css):1|
|spacing|`margin`|`5px 4px`|[components/context-menu/context-menu.css](../components/context-menu/context-menu.css):1<br>[components/dropdown/dropdown.css](../components/dropdown/dropdown.css):1|
|spacing|`margin-bottom`|`20px`|[components/tracing-beam/tracing-beam.css](../components/tracing-beam/tracing-beam.css):1<br>[templates/checkout/preview.html](../templates/checkout/preview.html):1|
|spacing|`margin-bottom`|`22px`|[components/scrollspy/scrollspy.css](../components/scrollspy/scrollspy.css):1<br>[templates/blog-article/blog-article.css](../templates/blog-article/blog-article.css):1|
|spacing|`margin-bottom`|`3px`|[components/empty-state/empty-state.css](../components/empty-state/empty-state.css):1<br>[templates/product-page/product-page.css](../templates/product-page/product-page.css):1|
|spacing|`margin-bottom`|`6px`|[components/gauge/gauge.css](../components/gauge/gauge.css):1<br>[templates/blog-article/blog-article.css](../templates/blog-article/blog-article.css):1|
|spacing|`margin-inline-end`|`5px`|[components/radar-chart/radar-chart.css](../components/radar-chart/radar-chart.css):1<br>[components/scatter-chart/scatter-chart.css](../components/scatter-chart/scatter-chart.css):1|
|spacing|`margin-top`|`24px`|[blocks/site-footer/site-footer.css](../blocks/site-footer/site-footer.css):1<br>[templates/product-page/product-page.css](../templates/product-page/product-page.css):1|
|spacing|`padding`|`0 11px`|[components/input-group/input-group.css](../components/input-group/input-group.css):1<br>[components/transfer/transfer.css](../components/transfer/transfer.css):1|
|spacing|`padding`|`0 13px`|[components/segmented/segmented.css](../components/segmented/segmented.css):1<br>[components/toggle/toggle.css](../components/toggle/toggle.css):1|
|spacing|`padding`|`0 1px`|[components/candlestick-chart/candlestick-chart.css](../components/candlestick-chart/candlestick-chart.css):1<br>[components/line-chart/line-chart.css](../components/line-chart/line-chart.css):1|
|spacing|`padding`|`0 9px`|[components/badge/badge.css](../components/badge/badge.css):1<br>[templates/inbox/inbox.css](../templates/inbox/inbox.css):1|
|spacing|`padding`|`1.5px`|[components/beam-border/beam-border.css](../components/beam-border/beam-border.css):1<br>[components/glow-cards/glow-cards.css](../components/glow-cards/glow-cards.css):1|
|spacing|`padding`|`10px 0`|[components/glow-button/preview.html](../components/glow-button/preview.html):1<br>[components/tilt-card/preview.html](../components/tilt-card/preview.html):1|
|spacing|`padding`|`10px 14px`|[components/table/table.css](../components/table/table.css):1<br>[components/wagara/wagara.css](../components/wagara/wagara.css):1|
|spacing|`padding`|`12px 0 2px`|[blocks/use-cases/preview.html](../blocks/use-cases/preview.html):1<br>[components/sidebar/sidebar.css](../components/sidebar/sidebar.css):1|
|spacing|`padding`|`12px 8px 2px`|[blocks/app-shell/app-shell.css](../blocks/app-shell/app-shell.css):1<br>[components/sidebar/sidebar.css](../components/sidebar/sidebar.css):1|
|spacing|`padding`|`13px 0`|[templates/blog-article/blog-article.css](../templates/blog-article/blog-article.css):1<br>[templates/settings-page/settings-page.css](../templates/settings-page/settings-page.css):1|
|spacing|`padding`|`13px 18px`|[blocks/site-header/site-header.css](../blocks/site-header/site-header.css):1<br>[components/card/card.css](../components/card/card.css):1|
|spacing|`padding`|`13px 26px`|[components/burst-button/burst-button.css](../components/burst-button/burst-button.css):1<br>[components/jelly-buttons/jelly-buttons.css](../components/jelly-buttons/jelly-buttons.css):1|
|spacing|`padding`|`15px 17px`|[blocks/use-cases/use-cases.css](../blocks/use-cases/use-cases.css):1<br>[templates/blog-article/blog-article.css](../templates/blog-article/blog-article.css):1|
|spacing|`padding`|`16px 12px`|[blocks/app-shell/app-shell.css](../blocks/app-shell/app-shell.css):1<br>[templates/inbox/inbox.css](../templates/inbox/inbox.css):1|
|spacing|`padding`|`16px 18px`|[components/scrollspy/scrollspy.css](../components/scrollspy/scrollspy.css):1<br>[components/tabs/tabs.css](../components/tabs/tabs.css):1|
|spacing|`padding`|`17px`|[blocks/cookie-consent/cookie-consent.css](../blocks/cookie-consent/cookie-consent.css):1<br>[templates/blog-article/blog-article.css](../templates/blog-article/blog-article.css):1|
|spacing|`padding`|`1px 5px`|[components/typeset/typeset.css](../components/typeset/typeset.css):1<br>[templates/blog-article/blog-article.css](../templates/blog-article/blog-article.css):1|
|spacing|`padding`|`20px 22px`|[components/kata-rain/kata-rain.css](../components/kata-rain/kata-rain.css):1<br>[templates/settings-page/settings-page.css](../templates/settings-page/settings-page.css):1|
|spacing|`padding`|`26px 18px`|[components/file-upload/file-upload.css](../components/file-upload/file-upload.css):1<br>[templates/landing/landing.css](../templates/landing/landing.css):1|
|spacing|`padding`|`2px 0 2px 16px`|[components/typeset/typeset.css](../components/typeset/typeset.css):1<br>[templates/blog-article/blog-article.css](../templates/blog-article/blog-article.css):1|
|spacing|`padding`|`30px 26px`|[components/particle-net/particle-net.css](../components/particle-net/particle-net.css):1<br>[templates/blog-article/blog-article.css](../templates/blog-article/blog-article.css):1|
|spacing|`padding`|`4px`|[components/goo-tabs/goo-tabs.css](../components/goo-tabs/goo-tabs.css):1<br>[components/toggle/toggle.css](../components/toggle/toggle.css):1|
|spacing|`padding`|`4px 9px`|[components/dock/dock.css](../components/dock/dock.css):1<br>[components/follow-frame/follow-frame.css](../components/follow-frame/follow-frame.css):1|
|spacing|`padding`|`5px 8px`|[blocks/invoice/invoice.css](../blocks/invoice/invoice.css):1<br>[components/tooltip/tooltip.css](../components/tooltip/tooltip.css):1|
|spacing|`padding`|`6px`|[components/cascader/cascader.css](../components/cascader/cascader.css):1<br>[components/command/command.css](../components/command/command.css):1|
|spacing|`padding`|`6px 10px`|[components/scrollspy/scrollspy.css](../components/scrollspy/scrollspy.css):1<br>[components/sidebar/sidebar.css](../components/sidebar/sidebar.css):1|
|spacing|`padding`|`8px 14px`|[components/gravity-playground/gravity-playground.css](../components/gravity-playground/gravity-playground.css):1<br>[components/wagara/wagara.css](../components/wagara/wagara.css):1|
|spacing|`padding`|`9px 0`|[components/glass-panel/glass-panel.css](../components/glass-panel/glass-panel.css):1<br>[components/sidebar/sidebar.css](../components/sidebar/sidebar.css):1|
|spacing|`padding`|`9px 8px`|[blocks/invoice/invoice.css](../blocks/invoice/invoice.css):1<br>[components/scroll-area/scroll-area.css](../components/scroll-area/scroll-area.css):1|
|spacing|`padding-bottom`|`4px`|[components/carousel/carousel.css](../components/carousel/carousel.css):1<br>[components/heatmap/heatmap.css](../components/heatmap/heatmap.css):1|
|spacing|`padding-bottom`|`8px`|[components/select/combos.html](../components/select/combos.html):2|
|spacing|`padding-inline-end`|`6px`|[components/scroll-area/scroll-area.css](../components/scroll-area/scroll-area.css):1<br>[components/tracing-beam/tracing-beam.css](../components/tracing-beam/tracing-beam.css):1|
|spacing|`padding-inline-start`|`20px`|[components/typeset/typeset.css](../components/typeset/typeset.css):1<br>[templates/blog-article/blog-article.css](../templates/blog-article/blog-article.css):1|
|spacing|`padding-right`|`42px`|[components/date-picker/preview.html](../components/date-picker/preview.html):1<br>[components/time-picker/preview.html](../components/time-picker/preview.html):1|
|spacing|`padding-top`|`11px`|[blocks/order-confirmation/order-confirmation.css](../blocks/order-confirmation/order-confirmation.css):1<br>[templates/checkout/checkout.css](../templates/checkout/checkout.css):1|
|spacing|`padding-top`|`16px`|[blocks/site-footer/site-footer.css](../blocks/site-footer/site-footer.css):1<br>[components/hanko/hanko.css](../components/hanko/hanko.css):1|
|spacing|`right`|`10px`|[components/comparison-slider/comparison-slider.css](../components/comparison-slider/comparison-slider.css):1<br>[components/scroll-area/scroll-area.css](../components/scroll-area/scroll-area.css):1|
|spacing|`right`|`14px`|[blocks/cookie-consent/cookie-consent.css](../blocks/cookie-consent/cookie-consent.css):1<br>[components/accordion-gallery/accordion-gallery.css](../components/accordion-gallery/accordion-gallery.css):1|
|spacing|`right`|`6px`|[components/date-picker/date-picker.css](../components/date-picker/date-picker.css):1<br>[components/time-picker/time-picker.css](../components/time-picker/time-picker.css):1|
|spacing|`top`|`11px`|[components/dual-range/dual-range.css](../components/dual-range/dual-range.css):2|
|spacing|`top`|`14px`|[components/speed-dial/preview.html](../components/speed-dial/preview.html):1<br>[templates/blog-article/blog-article.css](../templates/blog-article/blog-article.css):1|
|spacing|`top`|`16px`|[components/timeline/timeline.css](../components/timeline/timeline.css):1<br>[templates/checkout/checkout.css](../templates/checkout/checkout.css):1|
|spacing|`top`|`78px`|[components/tour/examples.html](../components/tour/examples.html):1<br>[components/tour/preview.html](../components/tour/preview.html):1|
|spacing|`bottom`|`13px`|[components/accordion-gallery/accordion-gallery.css](../components/accordion-gallery/accordion-gallery.css):1|
|spacing|`bottom`|`2px`|[components/gauge/gauge.css](../components/gauge/gauge.css):1|
|spacing|`bottom`|`3px`|[components/tabs/tabs.css](../components/tabs/tabs.css):1|
|spacing|`bottom`|`calc(100% + 2px)`|[components/tooltip/tooltip.css](../components/tooltip/tooltip.css):1|
|spacing|`bottom`|`calc(100% + 7px)`|[components/tooltip/tooltip.css](../components/tooltip/tooltip.css):1|
|spacing|`bottom`|`calc(100% + 9px)`|[components/dock/dock.css](../components/dock/dock.css):1|
|spacing|`gap`|`1px`|[components/transfer/transfer.css](../components/transfer/transfer.css):1|
|spacing|`gap`|`24px`|[blocks/site-footer/site-footer.css](../blocks/site-footer/site-footer.css):1|
|spacing|`gap`|`28px`|[templates/product-page/product-page.css](../templates/product-page/product-page.css):1|
|spacing|`gap`|`44px`|[components/marquee/marquee.css](../components/marquee/marquee.css):1|
|spacing|`inset`|`26px`|[components/orbit/orbit.css](../components/orbit/orbit.css):1|
|spacing|`inset-inline-end`|`10px`|[components/select/select.css](../components/select/select.css):1|
|spacing|`inset-inline-end`|`18px`|[components/toast/toast.css](../components/toast/toast.css):1|
|spacing|`inset-inline-start`|`3px`|[components/switch/switch.css](../components/switch/switch.css):1|
|spacing|`left`|`118px`|[components/tour/preview.html](../components/tour/preview.html):1|
|spacing|`left`|`120px`|[components/tour/examples.html](../components/tour/examples.html):1|
|spacing|`left`|`13px`|[components/accordion-gallery/accordion-gallery.css](../components/accordion-gallery/accordion-gallery.css):1|
|spacing|`left`|`14px`|[blocks/cookie-consent/cookie-consent.css](../blocks/cookie-consent/cookie-consent.css):1|
|spacing|`left`|`15px`|[components/accordion-gallery/accordion-gallery.css](../components/accordion-gallery/accordion-gallery.css):1|
|spacing|`left`|`20px`|[blocks/pricing/pricing.css](../blocks/pricing/pricing.css):1|
|spacing|`left`|`28px`|[components/tour/tour.css](../components/tour/tour.css):1|
|spacing|`left`|`2px`|[components/meteors/meteors.css](../components/meteors/meteors.css):1|
|spacing|`left`|`3px`|[components/tracing-beam/tracing-beam.css](../components/tracing-beam/tracing-beam.css):1|
|spacing|`left`|`44px`|[components/tour/examples.html](../components/tour/examples.html):1|
|spacing|`left`|`4px`|[components/timeline/timeline.css](../components/timeline/timeline.css):1|
|spacing|`left`|`96px`|[components/tour/examples.html](../components/tour/examples.html):1|
|spacing|`left`|`calc(-50% + 16px)`|[components/steps/steps.css](../components/steps/steps.css):1|
|spacing|`margin`|`0 0 10px`|[components/typeset/typeset.css](../components/typeset/typeset.css):1|
|spacing|`margin`|`0 0 15px`|[templates/blog-article/blog-article.css](../templates/blog-article/blog-article.css):1|
|spacing|`margin`|`0 0 5px`|[components/tour/tour.css](../components/tour/tour.css):1|
|spacing|`margin`|`0 0 8px`|[components/typeset/typeset.css](../components/typeset/typeset.css):1|
|spacing|`margin`|`0 26px 0 2px`|[components/command/preview.html](../components/command/preview.html):1|
|spacing|`margin`|`0 auto 15px`|[components/result/result.css](../components/result/result.css):1|
|spacing|`margin`|`10px 0 0`|[components/reorder/reorder.css](../components/reorder/reorder.css):1|
|spacing|`margin`|`10px auto 22px`|[blocks/cta-band/cta-band.css](../blocks/cta-band/cta-band.css):1|
|spacing|`margin`|`11px 0 0`|[blocks/use-cases/use-cases.css](../blocks/use-cases/use-cases.css):1|
|spacing|`margin`|`12px 0 0`|[components/file-upload/file-upload.css](../components/file-upload/file-upload.css):1|
|spacing|`margin`|`12px 0 10px`|[templates/blog-article/blog-article.css](../templates/blog-article/blog-article.css):1|
|spacing|`margin`|`12px 0 2px`|[blocks/team/team.css](../blocks/team/team.css):1|
|spacing|`margin`|`14px 0`|[blocks/app-shell/app-shell.css](../blocks/app-shell/app-shell.css):1|
|spacing|`margin`|`14px 10px 6px`|[templates/dashboard/dashboard.css](../templates/dashboard/dashboard.css):1|
|spacing|`margin`|`15px 0 4px`|[templates/product-page/product-page.css](../templates/product-page/product-page.css):1|
|spacing|`margin`|`15px 0 8px`|[templates/product-page/product-page.css](../templates/product-page/product-page.css):1|
|spacing|`margin`|`18px 0 14px`|[blocks/pricing/pricing.css](../blocks/pricing/pricing.css):1|
|spacing|`margin`|`18px 0 20px`|[templates/blog-article/blog-article.css](../templates/blog-article/blog-article.css):1|
|spacing|`margin`|`20px 0`|[templates/blog-article/blog-article.css](../templates/blog-article/blog-article.css):1|
|spacing|`margin`|`22px 0`|[blocks/settings/settings.css](../blocks/settings/settings.css):1|
|spacing|`margin`|`22px 0 6px`|[components/typeset/typeset.css](../components/typeset/typeset.css):1|
|spacing|`margin`|`24px 0`|[components/typeset/typeset.css](../components/typeset/typeset.css):1|
|spacing|`margin`|`26px 0 10px`|[templates/blog-article/blog-article.css](../templates/blog-article/blog-article.css):1|
|spacing|`margin`|`2px 0 2px 25px`|[components/sidebar/sidebar.css](../components/sidebar/sidebar.css):1|
|spacing|`margin`|`30px 0 8px`|[components/typeset/typeset.css](../components/typeset/typeset.css):1|
|spacing|`margin`|`4px 0`|[components/typeset/typeset.css](../components/typeset/typeset.css):1|
|spacing|`margin`|`5px 8px`|[components/menubar/menubar.css](../components/menubar/menubar.css):1|
|spacing|`margin`|`6px 0 13px`|[blocks/cookie-consent/cookie-consent.css](../blocks/cookie-consent/cookie-consent.css):1|
|spacing|`margin`|`6px 0 5px`|[components/torn-ticket/torn-ticket.css](../components/torn-ticket/torn-ticket.css):1|
|spacing|`margin`|`6px auto`|[components/orbit/orbit.css](../components/orbit/orbit.css):1|
|spacing|`margin`|`7px 0 14px`|[components/tilt-card/preview.html](../components/tilt-card/preview.html):1|
|spacing|`margin`|`8px 0 6px`|[components/stacking-cards/stacking-cards.css](../components/stacking-cards/stacking-cards.css):1|
|spacing|`margin`|`8px 0 7px`|[components/kintsugi-card/kintsugi-card.css](../components/kintsugi-card/kintsugi-card.css):1|
|spacing|`margin`|`9px 0 7px`|[templates/product-page/product-page.css](../templates/product-page/product-page.css):1|
|spacing|`margin`|`9px 10px 4px`|[components/transfer/transfer.css](../components/transfer/transfer.css):1|
|spacing|`margin-bottom`|`-.12em`|[components/text-reveal/text-reveal.css](../components/text-reveal/text-reveal.css):1|
|spacing|`margin-bottom`|`13px`|[templates/checkout/checkout.css](../templates/checkout/checkout.css):1|
|spacing|`margin-bottom`|`15px`|[templates/blog-article/blog-article.css](../templates/blog-article/blog-article.css):1|
|spacing|`margin-bottom`|`1px`|[components/timeline/timeline.css](../components/timeline/timeline.css):1|
|spacing|`margin-bottom`|`2px`|[components/radio/preview.html](../components/radio/preview.html):1|
|spacing|`margin-bottom`|`4px`|[components/calendar/calendar.css](../components/calendar/calendar.css):1|
|spacing|`margin-bottom`|`8px`|[templates/blog-article/blog-article.css](../templates/blog-article/blog-article.css):1|
|spacing|`margin-inline-end`|`8px`|[components/tategaki/tategaki.css](../components/tategaki/tategaki.css):1|
|spacing|`margin-inline-end`|`9px`|[components/table/table.css](../components/table/table.css):1|
|spacing|`margin-inline-start`|`2px`|[components/typewriter/typewriter.css](../components/typewriter/typewriter.css):1|
|spacing|`margin-inline-start`|`5px`|[components/wagara/wagara.css](../components/wagara/wagara.css):1|
|spacing|`margin-inline-start`|`8px`|[components/tree/tree.css](../components/tree/tree.css):1|
|spacing|`margin-left`|`8px`|[components/menubar/preview.html](../components/menubar/preview.html):1|
|spacing|`margin-top`|`13px`|[components/color-picker/color-picker.css](../components/color-picker/color-picker.css):1|
|spacing|`margin-top`|`15px`|[templates/checkout/preview.html](../templates/checkout/preview.html):1|
|spacing|`margin-top`|`26px`|[templates/blog-article/blog-article.css](../templates/blog-article/blog-article.css):1|
|spacing|`padding`|`0 0 18px 22px`|[components/timeline/timeline.css](../components/timeline/timeline.css):1|
|spacing|`padding`|`0 17px 17px 41px`|[blocks/use-cases/use-cases.css](../blocks/use-cases/use-cases.css):1|
|spacing|`padding`|`0 18px`|[components/horizontal-reel/horizontal-reel.css](../components/horizontal-reel/horizontal-reel.css):1|
|spacing|`padding`|`0 26px`|[components/magnet/preview.html](../components/magnet/preview.html):1|
|spacing|`padding`|`0 26px 22px`|[components/noren/noren.css](../components/noren/noren.css):1|
|spacing|`padding`|`0 2px`|[components/bar-chart/bar-chart.css](../components/bar-chart/bar-chart.css):1|
|spacing|`padding`|`0 32px 0 12px`|[components/select/select.css](../components/select/select.css):1|
|spacing|`padding`|`0 5px`|[components/kbd/kbd.css](../components/kbd/kbd.css):1|
|spacing|`padding`|`0 7px`|[components/pagination/pagination.css](../components/pagination/pagination.css):1|
|spacing|`padding`|`0 7px 0 12px`|[components/chip/chip.css](../components/chip/chip.css):1|
|spacing|`padding`|`10px 12px 150px`|[components/navigation-menu/preview.html](../components/navigation-menu/preview.html):1|
|spacing|`padding`|`10px 13px`|[components/menubar/preview.html](../components/menubar/preview.html):1|
|spacing|`padding`|`10px 18px 14px`|[blocks/site-header/site-header.css](../blocks/site-header/site-header.css):1|
|spacing|`padding`|`10px 2px`|[components/descriptions/descriptions.css](../components/descriptions/descriptions.css):1|
|spacing|`padding`|`10px 6px 2px`|[templates/dashboard/dashboard.css](../templates/dashboard/dashboard.css):1|
|spacing|`padding`|`11px`|[components/calendar/calendar.css](../components/calendar/calendar.css):1|
|spacing|`padding`|`11px 0`|[blocks/app-shell/app-shell.css](../blocks/app-shell/app-shell.css):1|
|spacing|`padding`|`11px 12px`|[blocks/kanban/kanban.css](../blocks/kanban/kanban.css):1|
|spacing|`padding`|`11px 13px`|[components/collapsible/collapsible.css](../components/collapsible/collapsible.css):1|
|spacing|`padding`|`12px 13px`|[blocks/roadmap/roadmap.css](../blocks/roadmap/roadmap.css):1|
|spacing|`padding`|`12px 15px`|[components/list/list.css](../components/list/list.css):1|
|spacing|`padding`|`12px 24px`|[components/confetti-cannon/confetti-cannon.css](../components/confetti-cannon/confetti-cannon.css):1|
|spacing|`padding`|`12px 26px`|[components/glow-button/glow-button.css](../components/glow-button/glow-button.css):1|
|spacing|`padding`|`13px`|[components/collapsible/collapsible.css](../components/collapsible/collapsible.css):1|
|spacing|`padding`|`13px 14px`|[templates/inbox/inbox.css](../templates/inbox/inbox.css):1|
|spacing|`padding`|`13px 15px`|[components/accordion/accordion.css](../components/accordion/accordion.css):1|
|spacing|`padding`|`13px 16px`|[components/toast/toast.css](../components/toast/toast.css):1|
|spacing|`padding`|`13px 27px`|[components/liquid-button/liquid-button.css](../components/liquid-button/liquid-button.css):1|
|spacing|`padding`|`14px 10px`|[components/sidebar/sidebar.css](../components/sidebar/sidebar.css):1|
|spacing|`padding`|`14px 16px`|[components/command/command.css](../components/command/command.css):1|
|spacing|`padding`|`14px 18px 18px`|[components/card/card.css](../components/card/card.css):1|
|spacing|`padding`|`14px 6px`|[templates/landing/landing.css](../templates/landing/landing.css):1|
|spacing|`padding`|`16px 18px 0`|[components/card/card.css](../components/card/card.css):1|
|spacing|`padding`|`16px 20px`|[components/drawer/drawer.css](../components/drawer/drawer.css):1|
|spacing|`padding`|`16px 3px 2px`|[components/goo-tabs/goo-tabs.css](../components/goo-tabs/goo-tabs.css):1|
|spacing|`padding`|`16px 6px`|[components/burst-button/preview.html](../components/burst-button/preview.html):1|
|spacing|`padding`|`18px 14px`|[templates/dashboard/dashboard.css](../templates/dashboard/dashboard.css):1|
|spacing|`padding`|`18px 28px 4px`|[templates/landing/landing.css](../templates/landing/landing.css):1|
|spacing|`padding`|`19px 20px`|[components/torn-ticket/torn-ticket.css](../components/torn-ticket/torn-ticket.css):1|
|spacing|`padding`|`1px 7px`|[components/sidebar/sidebar.css](../components/sidebar/sidebar.css):1|
|spacing|`padding`|`1px 8px`|[blocks/kanban/kanban.css](../blocks/kanban/kanban.css):1|
|spacing|`padding`|`20px 0 16px`|[components/newtons-cradle/newtons-cradle.css](../components/newtons-cradle/newtons-cradle.css):1|
|spacing|`padding`|`22px 10px`|[components/command/command.css](../components/command/command.css):1|
|spacing|`padding`|`22px 20px`|[blocks/pricing/pricing.css](../blocks/pricing/pricing.css):1|
|spacing|`padding`|`22px 24px`|[templates/inbox/inbox.css](../templates/inbox/inbox.css):1|
|spacing|`padding`|`22px 24px 26px`|[templates/dashboard/dashboard.css](../templates/dashboard/dashboard.css):1|
|spacing|`padding`|`22px 28px 4px`|[templates/landing/landing.css](../templates/landing/landing.css):1|
|spacing|`padding`|`24px 18px`|[templates/settings-page/settings-page.css](../templates/settings-page/settings-page.css):1|
|spacing|`padding`|`26px 20px`|[components/result/result.css](../components/result/result.css):1|
|spacing|`padding`|`26px 22px`|[components/sparkles/examples.html](../components/sparkles/examples.html):1|
|spacing|`padding`|`28px`|[components/aurora/aurora.css](../components/aurora/aurora.css):1|
|spacing|`padding`|`28px 22px`|[components/meteors/meteors.css](../components/meteors/meteors.css):1|
|spacing|`padding`|`2px 0 12px`|[components/sidebar/sidebar.css](../components/sidebar/sidebar.css):1|
|spacing|`padding`|`2px 15px 15px`|[components/accordion/accordion.css](../components/accordion/accordion.css):1|
|spacing|`padding`|`2px 6px 14px`|[templates/dashboard/dashboard.css](../templates/dashboard/dashboard.css):1|
|spacing|`padding`|`2px 8px`|[components/stat/stat.css](../components/stat/stat.css):1|
|spacing|`padding`|`2px 8px 12px`|[components/sidebar/sidebar.css](../components/sidebar/sidebar.css):1|
|spacing|`padding`|`2px 8px 14px`|[blocks/app-shell/app-shell.css](../blocks/app-shell/app-shell.css):1|
|spacing|`padding`|`3.5px 0`|[blocks/site-footer/site-footer.css](../blocks/site-footer/site-footer.css):1|
|spacing|`padding`|`30px 28px`|[blocks/login/login.css](../blocks/login/login.css):1|
|spacing|`padding`|`34px 24px`|[components/sparkles/preview.html](../components/sparkles/preview.html):1|
|spacing|`padding`|`36px 22px`|[components/empty-state/empty-state.css](../components/empty-state/empty-state.css):1|
|spacing|`padding`|`36px 28px`|[templates/landing/landing.css](../templates/landing/landing.css):1|
|spacing|`padding`|`3px 0 5px`|[components/time-picker/time-picker.css](../components/time-picker/time-picker.css):1|
|spacing|`padding`|`3px 6px 10px`|[blocks/kanban/kanban.css](../blocks/kanban/kanban.css):1|
|spacing|`padding`|`3px 9px`|[components/comparison-slider/comparison-slider.css](../components/comparison-slider/comparison-slider.css):1|
|spacing|`padding`|`4.5px 7px`|[components/tree/tree.css](../components/tree/tree.css):1|
|spacing|`padding`|`46px 26px 42px`|[blocks/cta-band/cta-band.css](../blocks/cta-band/cta-band.css):1|
|spacing|`padding`|`4px 0`|[components/calendar/calendar.css](../components/calendar/calendar.css):1|
|spacing|`padding`|`4px 11px`|[components/reorder/reorder.css](../components/reorder/reorder.css):1|
|spacing|`padding`|`5px 0`|[components/funnel-chart/funnel-chart.css](../components/funnel-chart/funnel-chart.css):1|
|spacing|`padding`|`5px 0 5px 11px`|[templates/blog-article/blog-article.css](../templates/blog-article/blog-article.css):1|
|spacing|`padding`|`5px 10px`|[components/speed-dial/speed-dial.css](../components/speed-dial/speed-dial.css):1|
|spacing|`padding`|`5px 9px`|[components/converge/converge.css](../components/converge/converge.css):1|
|spacing|`padding`|`6px 0`|[templates/checkout/checkout.css](../templates/checkout/checkout.css):1|
|spacing|`padding`|`6px 10px 3px`|[components/dropdown/dropdown.css](../components/dropdown/dropdown.css):1|
|spacing|`padding`|`6px 11px`|[components/menubar/menubar.css](../components/menubar/menubar.css):1|
|spacing|`padding`|`6px 13px`|[components/particle-word/particle-word.css](../components/particle-word/particle-word.css):1|
|spacing|`padding`|`6px 14px`|[components/kaleidoscope/kaleidoscope.css](../components/kaleidoscope/kaleidoscope.css):1|
|spacing|`padding`|`6px 16px`|[components/descriptions/descriptions.css](../components/descriptions/descriptions.css):1|
|spacing|`padding`|`6px 2px`|[components/bottom-navigation/bottom-navigation.css](../components/bottom-navigation/bottom-navigation.css):1|
|spacing|`padding`|`6px 8px`|[components/menubar/preview.html](../components/menubar/preview.html):1|
|spacing|`padding`|`6px 8px calc(6px + env(safe-area-inset-bottom))`|[components/bottom-navigation/bottom-navigation.css](../components/bottom-navigation/bottom-navigation.css):1|
|spacing|`padding`|`7px 0`|[components/time-picker/time-picker.css](../components/time-picker/time-picker.css):1|
|spacing|`padding`|`7px 10px`|[templates/settings-page/settings-page.css](../templates/settings-page/settings-page.css):1|
|spacing|`padding`|`7px 13px`|[components/wagara/wagara.css](../components/wagara/wagara.css):1|
|spacing|`padding`|`7px 15px`|[components/tabs/tabs.css](../components/tabs/tabs.css):1|
|spacing|`padding`|`8px`|[components/navigation-menu/navigation-menu.css](../components/navigation-menu/navigation-menu.css):1|
|spacing|`padding`|`8px 12px`|[components/navigation-menu/navigation-menu.css](../components/navigation-menu/navigation-menu.css):1|
|spacing|`padding`|`8px 16px`|[components/goo-tabs/goo-tabs.css](../components/goo-tabs/goo-tabs.css):1|
|spacing|`padding`|`8px 2px 0`|[components/bar-chart/bar-chart.css](../components/bar-chart/bar-chart.css):1|
|spacing|`padding`|`9px 12px`|[components/file-upload/file-upload.css](../components/file-upload/file-upload.css):1|
|spacing|`padding`|`9px 2px`|[components/bottom-navigation/bottom-navigation.css](../components/bottom-navigation/bottom-navigation.css):1|
|spacing|`padding`|`9px 8px 0`|[blocks/invoice/invoice.css](../blocks/invoice/invoice.css):1|
|spacing|`padding-bottom`|`.12em`|[components/text-reveal/text-reveal.css](../components/text-reveal/text-reveal.css):1|
|spacing|`padding-bottom`|`26px`|[templates/landing/landing.css](../templates/landing/landing.css):1|
|spacing|`padding-inline-end`|`2px`|[components/time-picker/time-picker.css](../components/time-picker/time-picker.css):1|
|spacing|`padding-inline-end`|`4px`|[components/copy-field/copy-field.css](../components/copy-field/copy-field.css):1|
|spacing|`padding-inline-start`|`12px`|[components/copy-field/copy-field.css](../components/copy-field/copy-field.css):1|
|spacing|`padding-inline-start`|`16px`|[components/donut-chart/donut-chart.css](../components/donut-chart/donut-chart.css):1|
|spacing|`padding-inline-start`|`19px`|[components/tree/tree.css](../components/tree/tree.css):1|
|spacing|`padding-inline-start`|`22px`|[components/menubar/menubar.css](../components/menubar/menubar.css):1|
|spacing|`padding-inline-start`|`24px`|[components/tategaki/tategaki.css](../components/tategaki/tategaki.css):1|
|spacing|`padding-inline-start`|`34px`|[components/input/input.css](../components/input/input.css):1|
|spacing|`padding-right`|`44px`|[components/marquee/marquee.css](../components/marquee/marquee.css):1|
|spacing|`padding-top`|`104px`|[components/goo-cursor/goo-cursor.css](../components/goo-cursor/goo-cursor.css):1|
|spacing|`padding-top`|`106px`|[components/warp-tunnel/warp-tunnel.css](../components/warp-tunnel/warp-tunnel.css):1|
|spacing|`padding-top`|`1px`|[components/descriptions/descriptions.css](../components/descriptions/descriptions.css):1|
|spacing|`padding-top`|`22px`|[components/typeset/typeset.css](../components/typeset/typeset.css):1|
|spacing|`padding-top`|`30px`|[components/tooltip/preview.html](../components/tooltip/preview.html):1|
|spacing|`padding-top`|`6px`|[blocks/order-confirmation/order-confirmation.css](../blocks/order-confirmation/order-confirmation.css):1|
|spacing|`right`|`12px`|[templates/inbox/inbox.css](../templates/inbox/inbox.css):1|
|spacing|`right`|`18px`|[components/speed-dial/speed-dial.css](../components/speed-dial/speed-dial.css):1|
|spacing|`right`|`calc(50% + 16px)`|[components/steps/steps.css](../components/steps/steps.css):1|
|spacing|`right`|`calc(50% - 14px)`|[components/bottom-navigation/bottom-navigation.css](../components/bottom-navigation/bottom-navigation.css):1|
|spacing|`top`|`10px`|[components/comparison-slider/comparison-slider.css](../components/comparison-slider/comparison-slider.css):1|
|spacing|`top`|`13px`|[components/steps/steps.css](../components/steps/steps.css):1|
|spacing|`top`|`5px`|[components/bottom-navigation/bottom-navigation.css](../components/bottom-navigation/bottom-navigation.css):1|
|spacing|`top`|`6px`|[components/tour/examples.html](../components/tour/examples.html):1|
|spacing|`top`|`calc(100% + 10px)`|[components/hover-card/hover-card.css](../components/hover-card/hover-card.css):1|
|spacing|`top`|`calc(100% + 2px)`|[components/tooltip/tooltip.css](../components/tooltip/tooltip.css):1|
|spacing|`top`|`calc(100% + 4px)`|[components/menubar/menubar.css](../components/menubar/menubar.css):1|
|spacing|`top`|`calc(100% + 6px)`|[components/dropdown/dropdown.css](../components/dropdown/dropdown.css):1|
|spacing|`top`|`calc(100% + 7px)`|[components/tooltip/tooltip.css](../components/tooltip/tooltip.css):1|
|spacing|`top`|`calc(6px + var(--i) * 11px)`|[components/stacking-cards/stacking-cards.css](../components/stacking-cards/stacking-cards.css):1|
|font-size|`font-size`|`12.5px`|[blocks/app-shell/app-shell.css](../blocks/app-shell/app-shell.css):1<br>[blocks/cookie-consent/cookie-consent.css](../blocks/cookie-consent/cookie-consent.css):1<br>[blocks/filter-toolbar/filter-toolbar.css](../blocks/filter-toolbar/filter-toolbar.css):1<br>[blocks/invoice/invoice.css](../blocks/invoice/invoice.css):1<br>[blocks/kanban/kanban.css](../blocks/kanban/kanban.css):2<br>[blocks/settings/settings.css](../blocks/settings/settings.css):1<br>[blocks/site-footer/site-footer.css](../blocks/site-footer/site-footer.css):2<br>[blocks/team/team.css](../blocks/team/team.css):1<br>[blocks/use-cases/preview.html](../blocks/use-cases/preview.html):1<br>[components/accordion-gallery/accordion-gallery.css](../components/accordion-gallery/accordion-gallery.css):1<br>[components/bottom-navigation/examples.html](../components/bottom-navigation/examples.html):1<br>[components/bottom-navigation/preview.html](../components/bottom-navigation/preview.html):1<br>[components/bounce-letters/preview.html](../components/bounce-letters/preview.html):1<br>[components/burst-button/preview.html](../components/burst-button/preview.html):1<br>[components/calendar/calendar.css](../components/calendar/calendar.css):1<br>[components/card/card.css](../components/card/card.css):2<br>[components/card/combos.html](../components/card/combos.html):2<br>[components/carousel-ring/preview.html](../components/carousel-ring/preview.html):1<br>[components/carousel/carousel.css](../components/carousel/carousel.css):1<br>[components/cascader/preview.html](../components/cascader/preview.html):1<br>[components/chip/chip.css](../components/chip/chip.css):1<br>[components/color-picker/color-picker.css](../components/color-picker/color-picker.css):1<br>[components/comparison-slider/preview.html](../components/comparison-slider/preview.html):1<br>[components/copy-field/copy-field.css](../components/copy-field/copy-field.css):2<br>[components/data-table/data-table.css](../components/data-table/data-table.css):1<br>[components/descriptions/descriptions.css](../components/descriptions/descriptions.css):1<br>[components/dock/preview.html](../components/dock/preview.html):1<br>[components/donut-chart/donut-chart.css](../components/donut-chart/donut-chart.css):1<br>[components/funnel-chart/funnel-chart.css](../components/funnel-chart/funnel-chart.css):2<br>[components/glow-cards/glow-cards.css](../components/glow-cards/glow-cards.css):1<br>[components/glow-cards/preview.html](../components/glow-cards/preview.html):1<br>[components/gravity-playground/preview.html](../components/gravity-playground/preview.html):1<br>[components/hanko/preview.html](../components/hanko/preview.html):1<br>[components/horizontal-reel/preview.html](../components/horizontal-reel/preview.html):1<br>[components/hover-card/hover-card.css](../components/hover-card/hover-card.css):1<br>[components/input/combos.html](../components/input/combos.html):1<br>[components/input/input.css](../components/input/input.css):1<br>[components/jelly-buttons/preview.html](../components/jelly-buttons/preview.html):1<br>[components/kaleidoscope/kaleidoscope.css](../components/kaleidoscope/kaleidoscope.css):1<br>[components/kaleidoscope/preview.html](../components/kaleidoscope/preview.html):1<br>[components/liquid-button/preview.html](../components/liquid-button/preview.html):1<br>[components/magnet/preview.html](../components/magnet/preview.html):1<br>[components/menubar/preview.html](../components/menubar/preview.html):2<br>[components/meter/preview.html](../components/meter/preview.html):3<br>[components/navigation-menu/navigation-menu.css](../components/navigation-menu/navigation-menu.css):1<br>[components/navigation-menu/preview.html](../components/navigation-menu/preview.html):1<br>[components/pagination/preview.html](../components/pagination/preview.html):1<br>[components/particle-word/particle-word.css](../components/particle-word/particle-word.css):1<br>[components/particle-word/preview.html](../components/particle-word/preview.html):1<br>[components/popover/popover.css](../components/popover/popover.css):1<br>[components/progress/preview.html](../components/progress/preview.html):2<br>[components/qr-code/examples.html](../components/qr-code/examples.html):1<br>[components/qr-code/preview.html](../components/qr-code/preview.html):1<br>[components/qr-code/qr-code.css](../components/qr-code/qr-code.css):1<br>[components/radio/preview.html](../components/radio/preview.html):1<br>[components/scramble/preview.html](../components/scramble/preview.html):1<br>[components/segmented/segmented.css](../components/segmented/segmented.css):1<br>[components/select/select.css](../components/select/select.css):1<br>[components/slider/preview.html](../components/slider/preview.html):2<br>[components/sparkles/examples.html](../components/sparkles/examples.html):1<br>[components/speed-dial/preview.html](../components/speed-dial/preview.html):1<br>[components/speed-dial/speed-dial.css](../components/speed-dial/speed-dial.css):1<br>[components/stacking-cards/preview.html](../components/stacking-cards/preview.html):1<br>[components/stepper/preview.html](../components/stepper/preview.html):2<br>[components/tategaki/tategaki.css](../components/tategaki/tategaki.css):1<br>[components/textarea/preview.html](../components/textarea/preview.html):1<br>[components/tilt-card/tilt-card.css](../components/tilt-card/tilt-card.css):2<br>[components/time-picker/preview.html](../components/time-picker/preview.html):1<br>[components/toast/combos.html](../components/toast/combos.html):1<br>[components/torn-ticket/torn-ticket.css](../components/torn-ticket/torn-ticket.css):1<br>[components/transfer/preview.html](../components/transfer/preview.html):2<br>[components/transfer/transfer.css](../components/transfer/transfer.css):1<br>[components/typeset/typeset.css](../components/typeset/typeset.css):1<br>[components/wagara/wagara.css](../components/wagara/wagara.css):3<br>[templates/blog-article/blog-article.css](../templates/blog-article/blog-article.css):3<br>[templates/checkout/checkout.css](../templates/checkout/checkout.css):1<br>[templates/inbox/inbox.css](../templates/inbox/inbox.css):1<br>[templates/product-page/preview.html](../templates/product-page/preview.html):1<br>[templates/product-page/product-page.css](../templates/product-page/product-page.css):6<br>[templates/settings-page/settings-page.css](../templates/settings-page/settings-page.css):2|
|font-size|`font-size`|`13px`|[blocks/app-shell/app-shell.css](../blocks/app-shell/app-shell.css):1<br>[blocks/faq/faq.css](../blocks/faq/faq.css):1<br>[blocks/integrations/integrations.css](../blocks/integrations/integrations.css):2<br>[blocks/invoice/invoice.css](../blocks/invoice/invoice.css):2<br>[blocks/login/login.css](../blocks/login/login.css):3<br>[blocks/order-confirmation/order-confirmation.css](../blocks/order-confirmation/order-confirmation.css):2<br>[blocks/pricing/pricing.css](../blocks/pricing/pricing.css):4<br>[blocks/roadmap/roadmap.css](../blocks/roadmap/roadmap.css):1<br>[blocks/site-footer/site-footer.css](../blocks/site-footer/site-footer.css):1<br>[blocks/testimonials/testimonials.css](../blocks/testimonials/testimonials.css):1<br>[blocks/use-cases/use-cases.css](../blocks/use-cases/use-cases.css):2<br>[components/bar-chart/bar-chart.css](../components/bar-chart/bar-chart.css):1<br>[components/beam-border/preview.html](../components/beam-border/preview.html):1<br>[components/breadcrumbs/breadcrumbs.css](../components/breadcrumbs/breadcrumbs.css):1<br>[components/calendar/calendar.css](../components/calendar/calendar.css):1<br>[components/candlestick-chart/candlestick-chart.css](../components/candlestick-chart/candlestick-chart.css):1<br>[components/card/examples.html](../components/card/examples.html):4<br>[components/collapsible/collapsible.css](../components/collapsible/collapsible.css):1<br>[components/command/command.css](../components/command/command.css):1<br>[components/context-menu/context-menu.css](../components/context-menu/context-menu.css):2<br>[components/date-picker/date-picker.css](../components/date-picker/date-picker.css):1<br>[components/donut-chart/donut-chart.css](../components/donut-chart/donut-chart.css):1<br>[components/dual-range/dual-range.css](../components/dual-range/dual-range.css):1<br>[components/empty-state/empty-state.css](../components/empty-state/empty-state.css):1<br>[components/field/field.css](../components/field/field.css):1<br>[components/file-upload/file-upload.css](../components/file-upload/file-upload.css):1<br>[components/gauge/gauge.css](../components/gauge/gauge.css):1<br>[components/glass-panel/glass-panel.css](../components/glass-panel/glass-panel.css):1<br>[components/goo-cursor/goo-cursor.css](../components/goo-cursor/goo-cursor.css):1<br>[components/gravity-playground/gravity-playground.css](../components/gravity-playground/gravity-playground.css):1<br>[components/hanko/hanko.css](../components/hanko/hanko.css):1<br>[components/heatmap/heatmap.css](../components/heatmap/heatmap.css):1<br>[components/input-group/input-group.css](../components/input-group/input-group.css):1<br>[components/kintsugi-card/kintsugi-card.css](../components/kintsugi-card/kintsugi-card.css):1<br>[components/line-chart/line-chart.css](../components/line-chart/line-chart.css):1<br>[components/marquee/preview.html](../components/marquee/preview.html):6<br>[components/menubar/menubar.css](../components/menubar/menubar.css):2<br>[components/meteors/meteors.css](../components/meteors/meteors.css):1<br>[components/pagination/pagination.css](../components/pagination/pagination.css):1<br>[components/particle-net/particle-net.css](../components/particle-net/particle-net.css):1<br>[components/qr-code/examples.html](../components/qr-code/examples.html):1<br>[components/rating/preview.html](../components/rating/preview.html):1<br>[components/reorder/reorder.css](../components/reorder/reorder.css):1<br>[components/scroll-area/scroll-area.css](../components/scroll-area/scroll-area.css):1<br>[components/scrollspy/scrollspy.css](../components/scrollspy/scrollspy.css):2<br>[components/separator/preview.html](../components/separator/preview.html):1<br>[components/sidebar/examples.html](../components/sidebar/examples.html):2<br>[components/sidebar/preview.html](../components/sidebar/preview.html):1<br>[components/sidebar/sidebar.css](../components/sidebar/sidebar.css):2<br>[components/split-panel/split-panel.css](../components/split-panel/split-panel.css):2<br>[components/spotlight/examples.html](../components/spotlight/examples.html):2<br>[components/stacking-cards/stacking-cards.css](../components/stacking-cards/stacking-cards.css):1<br>[components/tabs/tabs.css](../components/tabs/tabs.css):1<br>[components/timeline/timeline.css](../components/timeline/timeline.css):1<br>[components/toggle/toggle.css](../components/toggle/toggle.css):1<br>[components/tour/tour.css](../components/tour/tour.css):1<br>[components/tracing-beam/tracing-beam.css](../components/tracing-beam/tracing-beam.css):1<br>[components/transfer/transfer.css](../components/transfer/transfer.css):1<br>[components/wagara/wagara.css](../components/wagara/wagara.css):1<br>[templates/checkout/checkout.css](../templates/checkout/checkout.css):2<br>[templates/dashboard/dashboard.css](../templates/dashboard/dashboard.css):2<br>[templates/inbox/inbox.css](../templates/inbox/inbox.css):3<br>[templates/product-page/product-page.css](../templates/product-page/product-page.css):1<br>[templates/settings-page/settings-page.css](../templates/settings-page/settings-page.css):1|
|font-size|`font-size`|`13.5px`|[blocks/app-shell/app-shell.css](../blocks/app-shell/app-shell.css):2<br>[blocks/faq/faq.css](../blocks/faq/faq.css):1<br>[blocks/invoice/invoice.css](../blocks/invoice/invoice.css):1<br>[blocks/kanban/kanban.css](../blocks/kanban/kanban.css):1<br>[blocks/order-confirmation/order-confirmation.css](../blocks/order-confirmation/order-confirmation.css):1<br>[blocks/plan-compare/plan-compare.css](../blocks/plan-compare/plan-compare.css):1<br>[blocks/pricing/pricing.css](../blocks/pricing/pricing.css):1<br>[blocks/roadmap/roadmap.css](../blocks/roadmap/roadmap.css):1<br>[blocks/settings/settings.css](../blocks/settings/settings.css):1<br>[blocks/site-header/site-header.css](../blocks/site-header/site-header.css):1<br>[components/accordion-gallery/accordion-gallery.css](../components/accordion-gallery/accordion-gallery.css):1<br>[components/accordion/accordion.css](../components/accordion/accordion.css):2<br>[components/alert-dialog/alert-dialog.css](../components/alert-dialog/alert-dialog.css):1<br>[components/alert/alert.css](../components/alert/alert.css):1<br>[components/aurora/aurora.css](../components/aurora/aurora.css):1<br>[components/avatar/combos.html](../components/avatar/combos.html):2<br>[components/badge/examples.html](../components/badge/examples.html):3<br>[components/card/card.css](../components/card/card.css):1<br>[components/cascader/cascader.css](../components/cascader/cascader.css):1<br>[components/checkbox/checkbox.css](../components/checkbox/checkbox.css):1<br>[components/collapsible/collapsible.css](../components/collapsible/collapsible.css):1<br>[components/command/command.css](../components/command/command.css):1<br>[components/data-table/data-table.css](../components/data-table/data-table.css):1<br>[components/date-picker/date-picker.css](../components/date-picker/date-picker.css):1<br>[components/descriptions/descriptions.css](../components/descriptions/descriptions.css):1<br>[components/drawer/drawer.css](../components/drawer/drawer.css):1<br>[components/dropdown/dropdown.css](../components/dropdown/dropdown.css):1<br>[components/file-upload/file-upload.css](../components/file-upload/file-upload.css):1<br>[components/glow-button/glow-button.css](../components/glow-button/glow-button.css):1<br>[components/goo-tabs/goo-tabs.css](../components/goo-tabs/goo-tabs.css):2<br>[components/hanko/hanko.css](../components/hanko/hanko.css):1<br>[components/hover-card/hover-card.css](../components/hover-card/hover-card.css):1<br>[components/hover-card/preview.html](../components/hover-card/preview.html):1<br>[components/input/input.css](../components/input/input.css):1<br>[components/kbd/preview.html](../components/kbd/preview.html):1<br>[components/list/list.css](../components/list/list.css):1<br>[components/modal/combos.html](../components/modal/combos.html):1<br>[components/modal/modal.css](../components/modal/modal.css):1<br>[components/navigation-menu/navigation-menu.css](../components/navigation-menu/navigation-menu.css):2<br>[components/popover/popover.css](../components/popover/popover.css):1<br>[components/radio/radio.css](../components/radio/radio.css):1<br>[components/result/result.css](../components/result/result.css):1<br>[components/select/select.css](../components/select/select.css):1<br>[components/separator/preview.html](../components/separator/preview.html):2<br>[components/sidebar/sidebar.css](../components/sidebar/sidebar.css):1<br>[components/spotlight/preview.html](../components/spotlight/preview.html):1<br>[components/stepper/stepper.css](../components/stepper/stepper.css):1<br>[components/switch/switch.css](../components/switch/switch.css):1<br>[components/table/table.css](../components/table/table.css):1<br>[components/tabs/tabs.css](../components/tabs/tabs.css):1<br>[components/tag-input/tag-input.css](../components/tag-input/tag-input.css):1<br>[components/textarea/textarea.css](../components/textarea/textarea.css):1<br>[components/time-picker/time-picker.css](../components/time-picker/time-picker.css):1<br>[components/timeline/timeline.css](../components/timeline/timeline.css):1<br>[components/toast/toast.css](../components/toast/toast.css):1<br>[components/tree/tree.css](../components/tree/tree.css):1<br>[templates/blog-article/blog-article.css](../templates/blog-article/blog-article.css):2<br>[templates/dashboard/dashboard.css](../templates/dashboard/dashboard.css):1<br>[templates/inbox/inbox.css](../templates/inbox/inbox.css):2<br>[templates/settings-page/settings-page.css](../templates/settings-page/settings-page.css):2|
|font-size|`font-size`|`12px`|[blocks/invoice/invoice.css](../blocks/invoice/invoice.css):1<br>[blocks/roadmap/roadmap.css](../blocks/roadmap/roadmap.css):1<br>[blocks/settings/settings.css](../blocks/settings/settings.css):1<br>[blocks/site-footer/site-footer.css](../blocks/site-footer/site-footer.css):1<br>[blocks/team/team.css](../blocks/team/team.css):1<br>[components/aspect-ratio/aspect-ratio.css](../components/aspect-ratio/aspect-ratio.css):1<br>[components/avatar/combos.html](../components/avatar/combos.html):1<br>[components/bar-chart/bar-chart.css](../components/bar-chart/bar-chart.css):1<br>[components/candlestick-chart/candlestick-chart.css](../components/candlestick-chart/candlestick-chart.css):1<br>[components/color-picker/color-picker.css](../components/color-picker/color-picker.css):1<br>[components/counter/preview.html](../components/counter/preview.html):3<br>[components/donut-chart/donut-chart.css](../components/donut-chart/donut-chart.css):1<br>[components/field/field.css](../components/field/field.css):2<br>[components/file-upload/file-upload.css](../components/file-upload/file-upload.css):1<br>[components/fireworks/fireworks.css](../components/fireworks/fireworks.css):1<br>[components/follow-frame/follow-frame.css](../components/follow-frame/follow-frame.css):1<br>[components/funnel-chart/funnel-chart.css](../components/funnel-chart/funnel-chart.css):1<br>[components/glass-panel/glass-panel.css](../components/glass-panel/glass-panel.css):1<br>[components/hanko/hanko.css](../components/hanko/hanko.css):1<br>[components/heatmap/heatmap.css](../components/heatmap/heatmap.css):1<br>[components/horizontal-reel/horizontal-reel.css](../components/horizontal-reel/horizontal-reel.css):1<br>[components/input/input.css](../components/input/input.css):2<br>[components/line-chart/line-chart.css](../components/line-chart/line-chart.css):1<br>[components/list/list.css](../components/list/list.css):2<br>[components/noren/noren.css](../components/noren/noren.css):1<br>[components/radio/preview.html](../components/radio/preview.html):1<br>[components/scatter-chart/scatter-chart.css](../components/scatter-chart/scatter-chart.css):1<br>[components/separator/separator.css](../components/separator/separator.css):1<br>[components/sidebar/sidebar.css](../components/sidebar/sidebar.css):1<br>[components/sparkline/examples.html](../components/sparkline/examples.html):6<br>[components/spotlight/preview.html](../components/spotlight/preview.html):1<br>[components/steps/steps.css](../components/steps/steps.css):2<br>[components/textarea/preview.html](../components/textarea/preview.html):1<br>[components/toast/toast.css](../components/toast/toast.css):1<br>[templates/blog-article/blog-article.css](../templates/blog-article/blog-article.css):2<br>[templates/inbox/inbox.css](../templates/inbox/inbox.css):2<br>[templates/product-page/product-page.css](../templates/product-page/product-page.css):1<br>[templates/settings-page/settings-page.css](../templates/settings-page/settings-page.css):1|
|font-size|`font-size`|`11px`|[blocks/invoice/invoice.css](../blocks/invoice/invoice.css):1<br>[blocks/logo-cloud/logo-cloud.css](../blocks/logo-cloud/logo-cloud.css):1<br>[blocks/site-footer/site-footer.css](../blocks/site-footer/site-footer.css):1<br>[blocks/use-cases/use-cases.css](../blocks/use-cases/use-cases.css):1<br>[components/bar-chart/bar-chart.css](../components/bar-chart/bar-chart.css):2<br>[components/beam-border/preview.html](../components/beam-border/preview.html):1<br>[components/calendar/calendar.css](../components/calendar/calendar.css):1<br>[components/candlestick-chart/candlestick-chart.css](../components/candlestick-chart/candlestick-chart.css):1<br>[components/carousel-ring/carousel-ring.css](../components/carousel-ring/carousel-ring.css):1<br>[components/command/command.css](../components/command/command.css):1<br>[components/comparison-slider/comparison-slider.css](../components/comparison-slider/comparison-slider.css):1<br>[components/context-menu/context-menu.css](../components/context-menu/context-menu.css):1<br>[components/converge/converge.css](../components/converge/converge.css):1<br>[components/data-table/data-table.css](../components/data-table/data-table.css):1<br>[components/dock/dock.css](../components/dock/dock.css):1<br>[components/donut-chart/donut-chart.css](../components/donut-chart/donut-chart.css):1<br>[components/dropdown/dropdown.css](../components/dropdown/dropdown.css):1<br>[components/field/field.css](../components/field/field.css):2<br>[components/follow-frame/follow-frame.css](../components/follow-frame/follow-frame.css):1<br>[components/funnel-chart/funnel-chart.css](../components/funnel-chart/funnel-chart.css):1<br>[components/glass-panel/glass-panel.css](../components/glass-panel/glass-panel.css):1<br>[components/heatmap/heatmap.css](../components/heatmap/heatmap.css):1<br>[components/kbd/kbd.css](../components/kbd/kbd.css):1<br>[components/kintsugi-card/kintsugi-card.css](../components/kintsugi-card/kintsugi-card.css):2<br>[components/line-chart/line-chart.css](../components/line-chart/line-chart.css):1<br>[components/reorder/reorder.css](../components/reorder/reorder.css):1<br>[components/scroll-area/scroll-area.css](../components/scroll-area/scroll-area.css):1<br>[components/sidebar/sidebar.css](../components/sidebar/sidebar.css):1<br>[components/sparkles/preview.html](../components/sparkles/preview.html):1<br>[components/split-panel/split-panel.css](../components/split-panel/split-panel.css):1<br>[components/stat/stat.css](../components/stat/stat.css):1<br>[components/table/table.css](../components/table/table.css):1<br>[components/timeline/timeline.css](../components/timeline/timeline.css):1<br>[components/torn-ticket/torn-ticket.css](../components/torn-ticket/torn-ticket.css):1<br>[templates/blog-article/blog-article.css](../templates/blog-article/blog-article.css):2<br>[templates/inbox/inbox.css](../templates/inbox/inbox.css):1|
|font-size|`font-size`|`11.5px`|[blocks/app-shell/app-shell.css](../blocks/app-shell/app-shell.css):1<br>[blocks/integrations/integrations.css](../blocks/integrations/integrations.css):1<br>[blocks/invoice/invoice.css](../blocks/invoice/invoice.css):1<br>[blocks/kanban/kanban.css](../blocks/kanban/kanban.css):1<br>[blocks/testimonials/testimonials.css](../blocks/testimonials/testimonials.css):1<br>[components/avatar/avatar.css](../components/avatar/avatar.css):1<br>[components/badge/badge.css](../components/badge/badge.css):1<br>[components/file-upload/file-upload.css](../components/file-upload/file-upload.css):1<br>[components/gauge/gauge.css](../components/gauge/gauge.css):1<br>[components/glass-panel/glass-panel.css](../components/glass-panel/glass-panel.css):1<br>[components/menubar/menubar.css](../components/menubar/menubar.css):1<br>[components/radar-chart/radar-chart.css](../components/radar-chart/radar-chart.css):1<br>[components/reorder/reorder.css](../components/reorder/reorder.css):2<br>[components/scatter-chart/scatter-chart.css](../components/scatter-chart/scatter-chart.css):1<br>[components/sidebar/sidebar.css](../components/sidebar/sidebar.css):2<br>[components/stacking-cards/stacking-cards.css](../components/stacking-cards/stacking-cards.css):1<br>[components/stat/stat.css](../components/stat/stat.css):1<br>[components/table/table.css](../components/table/table.css):1<br>[components/tooltip/tooltip.css](../components/tooltip/tooltip.css):1<br>[components/typeset/typeset.css](../components/typeset/typeset.css):1<br>[components/wagara/wagara.css](../components/wagara/wagara.css):1<br>[templates/checkout/checkout.css](../templates/checkout/checkout.css):1<br>[templates/dashboard/dashboard.css](../templates/dashboard/dashboard.css):2<br>[templates/inbox/inbox.css](../templates/inbox/inbox.css):1|
|font-size|`font-size`|`14px`|[blocks/app-shell/app-shell.css](../blocks/app-shell/app-shell.css):1<br>[blocks/cookie-consent/cookie-consent.css](../blocks/cookie-consent/cookie-consent.css):1<br>[blocks/cta-band/cta-band.css](../blocks/cta-band/cta-band.css):1<br>[blocks/plan-compare/plan-compare.css](../blocks/plan-compare/plan-compare.css):1<br>[blocks/site-header/site-header.css](../blocks/site-header/site-header.css):1<br>[blocks/testimonials/testimonials.css](../blocks/testimonials/testimonials.css):1<br>[blocks/use-cases/use-cases.css](../blocks/use-cases/use-cases.css):1<br>[components/avatar/avatar.css](../components/avatar/avatar.css):1<br>[components/bottom-navigation/examples.html](../components/bottom-navigation/examples.html):1<br>[components/bottom-navigation/preview.html](../components/bottom-navigation/preview.html):1<br>[components/calendar/calendar.css](../components/calendar/calendar.css):1<br>[components/carousel/carousel.css](../components/carousel/carousel.css):1<br>[components/empty-state/empty-state.css](../components/empty-state/empty-state.css):1<br>[components/scrollspy/scrollspy.css](../components/scrollspy/scrollspy.css):1<br>[components/select/select.css](../components/select/select.css):1<br>[components/sidebar/sidebar.css](../components/sidebar/sidebar.css):1<br>[components/tategaki/tategaki.css](../components/tategaki/tategaki.css):1<br>[components/torn-ticket/torn-ticket.css](../components/torn-ticket/torn-ticket.css):1<br>[components/tour/tour.css](../components/tour/tour.css):1<br>[components/tracing-beam/tracing-beam.css](../components/tracing-beam/tracing-beam.css):1<br>[components/warp-tunnel/warp-tunnel.css](../components/warp-tunnel/warp-tunnel.css):1<br>[templates/blog-article/blog-article.css](../templates/blog-article/blog-article.css):1<br>[templates/inbox/inbox.css](../templates/inbox/inbox.css):1<br>[templates/product-page/product-page.css](../templates/product-page/product-page.css):1|
|font-size|`font-size`|`15px`|[blocks/invoice/invoice.css](../blocks/invoice/invoice.css):1<br>[blocks/settings/settings.css](../blocks/settings/settings.css):1<br>[blocks/site-footer/site-footer.css](../blocks/site-footer/site-footer.css):1<br>[blocks/site-header/site-header.css](../blocks/site-header/site-header.css):1<br>[blocks/team/team.css](../blocks/team/team.css):1<br>[components/command/command.css](../components/command/command.css):1<br>[components/drawer/drawer.css](../components/drawer/drawer.css):1<br>[components/hanko/hanko.css](../components/hanko/hanko.css):1<br>[components/marquee/preview.html](../components/marquee/preview.html):6<br>[components/sidebar/examples.html](../components/sidebar/examples.html):2<br>[components/sidebar/preview.html](../components/sidebar/preview.html):1<br>[components/spotlight/examples.html](../components/spotlight/examples.html):1<br>[components/typeset/typeset.css](../components/typeset/typeset.css):1<br>[templates/checkout/checkout.css](../templates/checkout/checkout.css):1<br>[templates/product-page/product-page.css](../templates/product-page/product-page.css):1|
|font-size|`font-size`|`14.5px`|[blocks/logo-cloud/logo-cloud.css](../blocks/logo-cloud/logo-cloud.css):1<br>[blocks/order-confirmation/order-confirmation.css](../blocks/order-confirmation/order-confirmation.css):1<br>[components/blur-in/examples.html](../components/blur-in/examples.html):1<br>[components/burst-button/burst-button.css](../components/burst-button/burst-button.css):1<br>[components/card/card.css](../components/card/card.css):1<br>[components/card/examples.html](../components/card/examples.html):2<br>[components/carousel-ring/carousel-ring.css](../components/carousel-ring/carousel-ring.css):1<br>[components/confetti-cannon/confetti-cannon.css](../components/confetti-cannon/confetti-cannon.css):1<br>[components/glow-button/glow-button.css](../components/glow-button/glow-button.css):1<br>[components/glow-cards/glow-cards.css](../components/glow-cards/glow-cards.css):1<br>[components/horizontal-reel/horizontal-reel.css](../components/horizontal-reel/horizontal-reel.css):1<br>[components/jelly-buttons/jelly-buttons.css](../components/jelly-buttons/jelly-buttons.css):1<br>[components/kintsugi-card/kintsugi-card.css](../components/kintsugi-card/kintsugi-card.css):1<br>[components/liquid-button/liquid-button.css](../components/liquid-button/liquid-button.css):1<br>[components/qr-code/preview.html](../components/qr-code/preview.html):1<br>[templates/checkout/checkout.css](../templates/checkout/checkout.css):2<br>[templates/dashboard/dashboard.css](../templates/dashboard/dashboard.css):1|
|font-size|`font-size`|`16px`|[components/command/command.css](../components/command/command.css):1<br>[components/input/input.css](../components/input/input.css):1<br>[components/select/select.css](../components/select/select.css):1<br>[components/stepper/stepper.css](../components/stepper/stepper.css):1<br>[components/tag-input/tag-input.css](../components/tag-input/tag-input.css):1<br>[components/textarea/textarea.css](../components/textarea/textarea.css):1<br>[components/typeset/typeset.css](../components/typeset/typeset.css):1<br>[components/wagara/wagara.css](../components/wagara/wagara.css):1<br>[templates/product-page/product-page.css](../templates/product-page/product-page.css):1|
|font-size|`font-size`|`19px`|[blocks/faq/faq.css](../blocks/faq/faq.css):1<br>[blocks/login/login.css](../blocks/login/login.css):1<br>[components/aurora/aurora.css](../components/aurora/aurora.css):1<br>[components/input-otp/input-otp.css](../components/input-otp/input-otp.css):1<br>[components/scramble/preview.html](../components/scramble/preview.html):1<br>[components/spotlight/preview.html](../components/spotlight/preview.html):1<br>[components/stacking-cards/stacking-cards.css](../components/stacking-cards/stacking-cards.css):1<br>[templates/checkout/checkout.css](../templates/checkout/checkout.css):1<br>[templates/settings-page/settings-page.css](../templates/settings-page/settings-page.css):1|
|font-size|`font-size`|`15.5px`|[blocks/use-cases/use-cases.css](../blocks/use-cases/use-cases.css):1<br>[components/qr-code/examples.html](../components/qr-code/examples.html):1<br>[components/typeset/typeset.css](../components/typeset/typeset.css):1<br>[templates/blog-article/blog-article.css](../templates/blog-article/blog-article.css):1<br>[templates/landing/landing.css](../templates/landing/landing.css):1<br>[templates/settings-page/settings-page.css](../templates/settings-page/settings-page.css):1|
|font-size|`font-size`|`16.5px`|[components/alert-dialog/alert-dialog.css](../components/alert-dialog/alert-dialog.css):1<br>[components/beam-border/preview.html](../components/beam-border/preview.html):1<br>[components/modal/modal.css](../components/modal/modal.css):1<br>[components/sparkles/examples.html](../components/sparkles/examples.html):1<br>[templates/blog-article/blog-article.css](../templates/blog-article/blog-article.css):2|
|font-size|`font-size`|`24px`|[components/shine-text/examples.html](../components/shine-text/examples.html):1<br>[components/sparkline/examples.html](../components/sparkline/examples.html):3<br>[components/word-rotate/preview.html](../components/word-rotate/preview.html):1<br>[templates/product-page/product-page.css](../templates/product-page/product-page.css):1|
|font-size|`font-size`|`10.5px`|[components/bottom-navigation/bottom-navigation.css](../components/bottom-navigation/bottom-navigation.css):1<br>[components/date-picker/date-picker.css](../components/date-picker/date-picker.css):1<br>[components/meter/meter.css](../components/meter/meter.css):1<br>[components/tategaki/tategaki.css](../components/tategaki/tategaki.css):1<br>[components/time-picker/time-picker.css](../components/time-picker/time-picker.css):1|
|font-size|`font-size`|`17px`|[blocks/integrations/integrations.css](../blocks/integrations/integrations.css):1<br>[blocks/invoice/invoice.css](../blocks/invoice/invoice.css):1<br>[components/result/result.css](../components/result/result.css):1<br>[components/tilt-card/tilt-card.css](../components/tilt-card/tilt-card.css):1<br>[components/typeset/typeset.css](../components/typeset/typeset.css):1|
|font-size|`font-size`|`21px`|[blocks/pricing/pricing.css](../blocks/pricing/pricing.css):1<br>[components/donut-chart/donut-chart.css](../components/donut-chart/donut-chart.css):1<br>[components/meteors/meteors.css](../components/meteors/meteors.css):1<br>[components/typewriter/preview.html](../components/typewriter/preview.html):1<br>[templates/product-page/product-page.css](../templates/product-page/product-page.css):1|
|font-size|`font-size`|`29px`|[blocks/use-cases/preview.html](../blocks/use-cases/preview.html):1<br>[components/bounce-letters/preview.html](../components/bounce-letters/preview.html):1<br>[components/hanko/hanko.css](../components/hanko/hanko.css):1<br>[components/typeset/typeset.css](../components/typeset/typeset.css):1<br>[templates/blog-article/blog-article.css](../templates/blog-article/blog-article.css):1|
|font-size|`font-size`|`20px`|[components/particle-net/particle-net.css](../components/particle-net/particle-net.css):1<br>[components/sparkles/preview.html](../components/sparkles/preview.html):1<br>[components/typeset/typeset.css](../components/typeset/typeset.css):1<br>[templates/dashboard/dashboard.css](../templates/dashboard/dashboard.css):1|
|font-size|`font-size`|`30px`|[components/counter/preview.html](../components/counter/preview.html):3|
|font-size|`font-size`|`.86em`|[components/typeset/typeset.css](../components/typeset/typeset.css):1<br>[templates/blog-article/blog-article.css](../templates/blog-article/blog-article.css):1|
|font-size|`font-size`|`18.5px`|[components/kintsugi-card/kintsugi-card.css](../components/kintsugi-card/kintsugi-card.css):1<br>[components/torn-ticket/torn-ticket.css](../components/torn-ticket/torn-ticket.css):1|
|font-size|`font-size`|`18px`|[blocks/order-confirmation/order-confirmation.css](../blocks/order-confirmation/order-confirmation.css):1<br>[templates/inbox/inbox.css](../templates/inbox/inbox.css):1|
|font-size|`font-size`|`23px`|[components/blur-in/preview.html](../components/blur-in/preview.html):1<br>[templates/product-page/product-page.css](../templates/product-page/product-page.css):1|
|font-size|`font-size`|`25px`|[blocks/cta-band/cta-band.css](../blocks/cta-band/cta-band.css):1<br>[components/typeset/examples.html](../components/typeset/examples.html):1|
|font-size|`font-size`|`31px`|[components/shine-text/preview.html](../components/shine-text/preview.html):1<br>[templates/landing/landing.css](../templates/landing/landing.css):1|
|font-size|`font-size`|`10px`|[components/torn-ticket/torn-ticket.css](../components/torn-ticket/torn-ticket.css):1|
|font-size|`font-size`|`19.5px`|[templates/blog-article/blog-article.css](../templates/blog-article/blog-article.css):1|
|font-size|`font-size`|`26px`|[components/stat/stat.css](../components/stat/stat.css):1|
|font-size|`font-size`|`27px`|[components/gauge/gauge.css](../components/gauge/gauge.css):1|
|font-size|`font-size`|`32px`|[blocks/pricing/pricing.css](../blocks/pricing/pricing.css):1|
|font-size|`font-size`|`41px`|[templates/landing/landing.css](../templates/landing/landing.css):1|
|font-size|`font-size`|`44px`|[components/tategaki/tategaki.css](../components/tategaki/tategaki.css):1|
|font-size|`font-size`|`9.5px`|[components/avatar/avatar.css](../components/avatar/avatar.css):1|
|font-size|`font-size`|`clamp(22px,4vw,30px)`|[components/text-reveal/preview.html](../components/text-reveal/preview.html):1|

## 実装するときの順序・保留条件

1. radiusの8/12/6/99px、durationの130/180/220ms等、数値も役割も一致するものを先に別PRで移行する。各PRは1〜2種類に限定する。
2. radius14pxなど件数が多い未定義値は、13/14/16を同一スケールに寄せるか、共有値として保存するかをデザイン判断する。system/tokens.jsonとの整合も必要。
3. spacingのcalc換算は同値でも、光学調整の意味を失わないかを確認する。font-sizeの近似や削減は今回実施しない。
4. shadow、Labのgradient、radial-gradientの芯の幾何、独自easingは自動で近い値に丸めない。必要ならローカル値を残し、検査ポリシーと設計の判断を別PRにする。
5. 通常/hover/active/focus/disabled、light/dark、RTL、reduced-motion、Foundry倍率とradius=0をブラウザーで確認する。見た目が変わるPRには同一条件の前後画像を添付する。
6. 各実装後はcheck.py JSONを再取得し、部品ページ・registry・MCP・LLM向けデータをbuild.pyで再生成する。検査を弱めたり、一律allowlistで数字を合わせたりしない。

## 再現・検証

```sh
python3 check.py --json /tmp/token-migration-check.json > /tmp/token-migration-check.log
# 終了1は今回の既存違反。JSONのsummaryとitems[].checks[id=token-values].findingsを集計する。
python3 build.py
```

433所見の種類別・値別・UI/Lab別・ファイル別の合計が一致することを確認。補足のspacing/font-sizeは独立した表として合計する。部品・トークン・検査器を変更せず、再実行のJSONが変更前と一致することも確認する。設計案の実装・見た目・contrast・実機動作・スクリーンリーダーはこの資料だけでは検証していない。

## Accuracy revision after PR #16

Snapshot: 2026-11-04 (Asia/Tokyo). This section supersedes the older measured counts above. Findings count property/kind records, not individual numeric tokens. Warning counts are findings, not the number of warning checks.

Before: **21 / 164**. After: **29 / 164**. UI 19 / 121; Lab 10 / 43.

### Rule changes and measured effects

Token reductions are sequential marginal changes in radius → color-scheme → easing → border → scaled duration → marked data colors order. Classification changes alone remove no findings. No per-component allowlist entries were added.

| Rule | Change and reason | Findings removed |
|---|---|---:|
| radius | Permit circular 50%; keep pixel radii checked | 38 |
| radius-full | Classify UI pixel radii ≥99px; require shared full-radius token | 0 (11 reclassified) |
| color | Ignore browser color-scheme behavior; retain paint checks | 4 |
| easing | Permit standard CSS timing functions/keywords; custom curves still require tokens | 20 |
| border | Permit 1–3px geometry, including fractions; retain paint checks | 35 |
| duration | A complete product controlled by the trusted motion multiplier follows Foundry | 1 |
| inline data colors | Only marked inline color declarations in preview/examples represent sample data | 8 |
| shadow-ring | Classify literal ring constructions, including local aliases | 0 (12 reclassified) |
| focus-visible | Read dependency evidence; deduplicate file/tag/classes; reject unrelated ancestor evidence | 324 (456 → 132) |
| shared-token-scope | Move two Toast-only colors from global tokens onto its root | 2 |

All previously passing targets remain passing. The changed focus count includes deduplication, not newly implemented keyboard behavior. tokens.css already contains an outline-only safety net; it does not implement the shared --k-ring rule planned for P7.

### Current check findings

| Check | Before | After |
|---|---:|---:|
| accessible-label | 1 | 1 |
| button-type | 0 | 0 |
| focus-visible | 456 | 132 |
| js-global-bindings | 57 | 57 |
| js-single-instance | 24 | 24 |
| legacy-contract | 0 | 0 |
| reduced-motion | 0 | 0 |
| shared-token-scope | 2 | 0 |
| spacing-values | 892 | 892 |
| token-values | 464 | 358 |
| type-values | 638 | 638 |
| variant-hover | 0 | 0 |

| token-values kind | Findings |
|---|---:|
| border | 1 |
| color | 23 |
| duration | 107 |
| easing | 10 |
| radius | 157 |
| radius-full | 11 |
| shadow | 37 |
| shadow-ring | 12 |

### Shared token proposals — no token additions in this revision

Each count below is the number of current token-values findings that the stated replacement can remove. Exact matches preserve the default value. Near matches require design review and are counted separately. Counts across overlapping proposals must not be summed. Local aliases are expanded before matching. Lab geometry is outside the radius count.

| Shared token proposal | Default value | Exact findings removed | Targets |
|---|---|---:|---|
| `--k-shadow-popover` | `0 20px 44px -14px rgba(16,24,40,.22)` | 4 | `components/cascader`, `components/date-picker`, `components/navigation-menu`, `components/time-picker` |
| `--k-shadow-modal` | `0 30px 80px -20px rgba(0,0,0,.4)` | 2 | `components/alert-dialog`, `components/modal` |
| `--k-shadow-xs` | `0 1px 2px rgba(16,24,40,.05)` | 2 | `blocks/kanban`, `components/button` |
| `--k-backdrop` | `rgba(24,24,27,.45)` | 4 | `components/alert-dialog`, `components/command`, `components/drawer`, `components/modal` |

The existing `--k-shadow-overlay` has different geometry/opacity. Do not alias all overlay shadows to it just to clear findings. Toast’s black .45 shadow also differs from the proposed zinc .22 popover shadow. Those variants require screenshots before normalization.

#### Radius scale linked to Foundry

At the current 8px base, define the following six shared levels. These are proposals, including updates/aliases for existing names. Do not add them in this PR. A zero base makes every level zero, including full. Full preserves the existing 99px default; it is not a guarantee of a pill on arbitrarily large boxes.

| Level | Proposed shared definition | Observed UI literals | Findings removable after agreed normalization | Exact-default subset |
|---|---|---|---:|---:|
| xs | `--k-radius-xs: calc(var(--k-radius) * 0.25)` | 2px, 2.5px, 3px | 10 | 2 |
| sm | `--k-radius-sm: calc(var(--k-radius) * 0.75)` | 4px, 5px, 6px | 11 | 5 |
| md | `--k-radius-md: var(--k-radius)` | 7px, 8px, 9px | 41 | 22 |
| lg | `--k-radius-lg: calc(var(--k-radius) * 1.5)` | 10px, 11px, 12px, 13px | 35 | 12 |
| xl | `--k-radius-xl: calc(var(--k-radius) * 2)` | 14px, 16px, 18px | 59 | 12 |
| full | `--k-radius-full: calc(var(--k-radius) * 12.375)` | 99px | 11 | 11 |

Mixed-corner declarations requiring more than one scale token: **1**: `components/hanko` `9px 11px 10px 12px`.

The scale covers all current UI radius findings only after the visual normalization is reviewed. The existing --k-radius-sm (6px), --k-radius-lg (12px) and --k-radius-full (99px) can be made relative to the base; --k-radius-md should alias --k-radius, not replace the Foundry base.

#### UI motion tiers

Use aliases of the existing 130ms / 180ms / 220ms shared tokens, then multiply by `var(--k-mscale, 1)` at use sites. These tiers stay within KATA.md’s 130–220ms UI interval. Keep artistic animation cycles and stagger delays out of this automatic mapping.

| Proposal | Definition | Candidate findings removed | Exact-duration subset |
|---|---|---:|---:|
| `--k-duration-fast` | `var(--k-dur-1)` (130ms) | 22 | 7 |
| `--k-duration-base` | `var(--k-dur-2)` (180ms) | 9 | 8 |
| `--k-duration-slow` | `var(--k-dur-3)` (220ms) | 3 | 1 |

Candidate counts assume replacing every raw time in that declaration and verifying the resulting interaction. For example, 120ms → 130ms changes timing; preserve it only through a reviewed policy decision. Durations outside these bands are not claimed as solved.

#### Custom easing

UI does not currently fail easing; these counts refer to the Lab-required easing findings. Keep the existing `--k-ease` as the default. Do not silently replace spring curves with that non-overshooting curve.

| Shared proposal | Curve | Exact findings removed | Optional near-match findings |
|---|---|---:|---:|
| `--k-ease-spring` | `cubic-bezier(.3,2.3,.4,1)` | 1 | 2 |
| `--k-ease-bounce` | `cubic-bezier(.6,-0.1,.2,1.25)` | 1 | 0 |

A declaration with two copies of the same curve is one finding; replace both to remove it. The spring near-match count is conditional on visual review. Cubic-bezier values in other curves remain open.

### Remaining limitations

Static selector matching is conservative and does not model the full CSS cascade, every pseudo-class or visual ring clipping. P7 must measure computed focus in a browser. Local-variable provenance merges possible definitions conservatively; it does not execute selectors or keyframes. This revision does not validate all CSS grammar or establish screen-reader behavior. Toast screenshots prove pixel equality in Chromium light/dark, not accessibility: its pre-existing dark text/background contrast problem remains open.


## Confirmed shared shape migration

This approved implementation supersedes the earlier radius/shadow proposals;
it does not change checker rules. Canonical values are in `system/tokens.json`;
`tools/sync_shape_tokens.py` generates the radius/elevation adapter in `tokens.css`.
Build renders and publishes the same JSON on `/design-system/`. Foundry modifies
the base only and preserves a saved zero.

| Observed UI radius | Shared stage | At base 8px | Runtime definition |
|---|---|---:|---|
| 2–3px (including 2.5px) | xs | 3px | calc(var(--k-radius) * .375) |
| 4–6px | sm | 6px | calc(var(--k-radius) * .75) |
| 7–9px | md | 8px | var(--k-radius) |
| 10–13px | lg | 12px | calc(var(--k-radius) * 1.5) |
| 14–18px | xl | 16px | calc(var(--k-radius) * 2) |
| ≥99px | full | 999px | 999px (fixed pill) |

There were no out-of-table radius literals in the failing findings. Mixed corner
values are mapped per corner, preserving zeros. Circles (50%) and Lab geometry
are unchanged. Existing sm/lg/full names are retained; full was actually 99px
in main and is updated to the requested 999px. The earlier full-relative proposal
is not implemented: full is explicitly fixed in the approved contract.

The elevation tiers are xs (0 1px 2px), sm (0 1px 4px), pop
(0 20px 44px -14px), and modal (0 30px 80px -20px). Light values use the most
frequent matching existing recipes; ties favor the documented tiny-shadow
recipe. Dark variants retain geometry with stronger black opacity.
The existing --k-shadow-overlay name is retained as an alias of --k-shadow-pop.
Two shared rings (--k-ring-inset / --k-ring-line) supplement existing focus rings.
Backdrops use color-mix with zinc-900 at 45% in light and zinc-950 at 70% in dark.
Only Modal / Drawer / Command / Alert Dialog backdrop paint changes here.

Audit: **29 / 164 → 53 / 164**. Radius 157 → 0; radius-full 11 → 0; shadow 37 → 0; shadow-ring 12 → 0. Duration remains 107; easing remains 10; independent backdrop replacements reduce color findings 23 → 19. Spacing/type warning findings remain 892 / 638.

Full target/declaration mapping, pixel measurements, the 4.5:1 dark contrast list, screenshots and scale assertions are recorded in [the review evidence](review/shared-shape/README.md). Colors in shadows follow the shadow migration; unrelated paint, duration and easing are untouched.

### Historical initial shadow mapping ledger

Lab rows in this initial ledger are superseded by the regression correction below.

| Observed shadow | Shared replacement | Targets |
|---|---|---|
| `-24px 0 60px -24px rgba(0,0,0,.35)` | `var(--k-shadow-modal)` | `components/drawer` |
| `0 0 0 1px rgba(24,24,27,.25)` | `var(--k-ring-line)` | `components/comparison-slider` |
| `0 0 0 1px var(--k-line)` | `var(--k-ring-line)` | `templates/product-page` |
| `0 0 0 2px var(--k-accent)` | `var(--k-ring)` | `templates/product-page` |
| `0 0 0 2px var(--k-bg),0 0 0 4px var(--k-accent)` | `var(--k-ring)` | `components/color-picker` |
| `0 0 0 2px var(--k-ink)` | `var(--k-ring)` | `templates/product-page` |
| `0 0 0 3px var(--k-accent-bg)` | `var(--k-ring)` | `components/input-otp`, `components/tag-input` |
| `0 0 0 4px var(--k-accent-bg)` | `var(--k-ring)` | `components/tracing-beam` |
| `0 0 0 5px var(--k-accent-bg-strong)` | `var(--k-ring)` | `components/tour` |
| `0 0 10px 2px rgba(255,255,255,.3)` | `var(--k-shadow-sm)` | `components/meteors` |
| `0 0 18px -4px var(--k-accent-bg)` | `var(--k-shadow-sm)` | `components/glow-button` |
| `0 0 26px -6px var(--k-accent)` | `var(--k-shadow-sm)` | `components/glow-button` |
| `0 0 46px color-mix(in srgb,var(--k-accent) 45%,transparent)` | `var(--k-shadow-pop)` | `components/converge` |
| `0 12px 26px -10px rgba(16,24,40,.4)` | `var(--k-shadow-pop)` | `components/orbit` |
| `0 14px 28px -14px rgba(16,24,40,.28)` | `var(--k-shadow-pop)` | `components/torn-ticket` |
| `0 14px 34px -12px rgba(16,24,40,.25)` | `var(--k-shadow-pop)` | `blocks/cookie-consent` |
| `0 16px 40px -12px rgba(16,24,40,.18)` | `var(--k-shadow-pop)` | `components/hover-card` |
| `0 16px 40px -14px rgba(16,24,40,.25)` | `var(--k-shadow-pop)` | `components/dropdown` |
| `0 18px 40px -12px rgba(16,24,40,.25)` | `var(--k-shadow-pop)` | `components/menubar` |
| `0 18px 40px -18px rgba(0,0,0,.45)` | `var(--k-shadow-pop)` | `components/glass-panel` |
| `0 18px 44px -14px rgba(16,24,40,.28)` | `var(--k-shadow-pop)` | `components/tour` |
| `0 1px 2px rgba(16,24,40,.04)` | `var(--k-shadow-xs)` | `components/input` |
| `0 1px 2px rgba(16,24,40,.05)` | `var(--k-shadow-xs)` | `blocks/kanban`, `components/button` |
| `0 1px 2px rgba(16,24,40,.09)` | `var(--k-shadow-xs)` | `components/segmented` |
| `0 1px 2px rgba(16,24,40,.18)` | `var(--k-shadow-xs)` | `components/slider` |
| `0 1px 3px rgba(0,0,0,.3),inset 0 0 0 1px rgba(0,0,0,.08)` | `var(--k-shadow-xs),var(--k-ring-inset)` | `components/switch` |
| `0 1px 3px rgba(16,24,40,.14)` | `var(--k-shadow-xs)` | `components/tabs` |
| `0 1px 4px rgba(16,24,40,.18)` | `var(--k-shadow-sm)` | `components/dual-range` |
| `0 20px 44px -12px rgba(16,24,40,.28)` | `var(--k-shadow-pop)` | `components/context-menu` |
| `0 20px 44px -14px rgba(0,0,0,.45)` | `var(--k-shadow-pop)` | `components/toast` |
| `0 20px 44px -14px rgba(16,24,40,.22)` | `var(--k-shadow-pop)` | `components/cascader`, `components/date-picker`, `components/navigation-menu`, `components/time-picker` |
| `0 2px 10px rgba(16,24,40,.3)` | `var(--k-shadow-sm)` | `components/comparison-slider` |
| `0 2px 8px rgba(16,24,40,.08)` | `var(--k-shadow-sm)` | `components/speed-dial` |
| `0 2px 8px rgba(16,24,40,.1)` | `var(--k-shadow-sm)` | `components/speed-dial` |
| `0 30px 80px -20px rgba(0,0,0,.4)` | `var(--k-shadow-modal)` | `components/alert-dialog`, `components/modal` |
| `0 30px 80px -20px rgba(0,0,0,.45)` | `var(--k-shadow-modal)` | `components/command` |
| `0 3px 7px rgba(16,24,40,.25)` | `var(--k-shadow-sm)` | `components/newtons-cradle` |
| `0 4px 12px rgba(16,24,40,.1)` | `var(--k-shadow-sm)` | `components/orbit` |
| `0 6px 18px rgba(16,24,40,.28)` | `var(--k-shadow-sm)` | `components/speed-dial` |
| `inset 0 0 0 1px currentColor` | `var(--k-ring-inset)` | `components/button` |


## PR #19 regression correction: effect geometry and ring semantics

Lab shadow geometry is restored to 9efb97d. The corrected rule checks paint
provenance in box-shadow/text-shadow/drop-shadow, including local aliases and
fallbacks; it does not force glow geometry through UI elevation stages. Literal
rgba/hex/named paint still fails. KATA.md and tests/mold/lab-shadows.json document
and test both outcomes. Glass Panel / Torn Ticket remain UI; Glow Button is Lab.

Seven Lab components restore ten declarations. Palette-based color-mix preserves
alpha and fixed light/neutral intent. Selected/offset rings are separate shared
tokens; Input OTP / Tag Input retain focus rings. Both Drawer edges showed >=8px
of shadow, so no edge token or Drawer change is made.

The score remains 53/164 (UI 42/121, Lab 11/43). A rule-only change on the initial
PR source adds zero passes. On restored sources the old rule would pass 52/164;
the corrected rule retains Tracing Beam's pass, without hiding other Lab issues.
[Full geometry, fixtures, edge measurements and three-way images](review/shape-regressions/README.md).
