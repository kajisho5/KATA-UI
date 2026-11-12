# Pixel Switch 詳細設計書

作成：2026-11-12　対象：kajisho5/KATA-UI　状態：オーナー依頼で実装（試作を確認のうえ「どんどんやってください」、2026-11-12）

## 1. 何を作るか（要件）

- ツマミに 11×11 のドット絵を描いたスイッチ。切り替えると点が散って、別の絵に組み直る。
- 同時に、光の弧がツマミの縁を一周する（`@property` の角度を 210° → 570° に動かす）。
- 絵の組は4種類：theme（太陽／月）、sound（消音／音あり）、bell（通知オフ／通知）、power（電源／稲妻）。
- 大きさは2段：標準 168×88px、`.k-pxs-sm` で 84×44px。
- 分類は Motion（Lab）、状態は beta。

### 1-1. ロードマップとの関係

ROADMAP の原則1「Phase 1 が終わるまで新しい部品を足さない」に対する、オーナー依頼の例外です（2026-11-12、チャットで試作を見たうえでの依頼）。ROADMAP と HANDOFF に例外として記録します。

### 1-2. やらないこと

- 絵の組を属性で自由に渡す仕組み（`MAPS` を JS の中で書き換える形にする。コードは利用者のもの）
- アプリの配色を自動で切り替えること（部品は `change` を出すだけ。使い方に例を書く）

## 2. 技術選定

既存の部品と同じ、素の HTML・CSS・JavaScript（依存なし、ビルドなし）。新しい技術は使いません（既存リポの技術は変えないため比較表は作っていません）。

- 点はキャンバスではなく `<span>` で描く。色を CSS の `currentColor` で決められるので、ダーク切り替えや Foundry の色変更にそのまま追従する。
- 点の動きは Web Animations API（`element.animate`）。長さは `720ms × --k-mscale`、曲線は `--k-ease-in-out` をその場で読む。

## 3. 画面構成（`pixel-switch.svg` 参照）

```
label.k-pxs[data-pxs="theme|sound|bell|power"]
  input[type=checkbox][role=switch][aria-label]   … 全面を覆う本体（透明）
  span.k-pxs-track                                 … 溝
  span.k-pxs-knob                                  … ツマミ（::before が光の弧）
    span.k-pxs-bloom                               … 弧をぼかした光
    span.k-pxs-dots                                … 点（JS が作る）
```

## 4. 色（すべて `--k-*` トークン）

| 部分 | theme OFF | theme ON | ほか OFF | ほか ON |
|---|---|---|---|---|
| 溝 | zinc-200 | zinc-950 | bg-soft | bg-soft |
| ツマミ | zinc-50 | zinc-800 | bg | bg |
| 点 | zinc-900 | zinc-50 | ink-2 | ink |
| 外枠の線 | zinc-500 | zinc-500 | ink-3 | ink-3 |
| 光 | yamabuki | asagi-300 | なし | accent |

theme の組は固定色（ページがダークでも太陽は明るい、月は暗い）。ほかの組はページの配色に合わせて入れ替わる。

## 5. 状態

- hover：外枠の線が一段濃くなる。active：ツマミが 96% に縮む。disabled：50% の濃さ、カーソル not-allowed。
- focus-visible：溝のまわりに `--k-ring`。
- 動きを減らす設定、または `--k-mscale: 0`：点もツマミも一瞬で切り替わる。
- 切り替え中にもう一度押すと、点はその場から新しい絵へ向かう（`commitStyles` してから次の動き）。

## 6. データ構造

```js
const MAPS = {
  theme: [[/* OFF: 11 行 × 11 文字、'#' が点 */], [/* ON */]],
  ...
};
```

点の数は、2枚の絵のうち多いほうに合わせる。余った点は中央で消える。

## 7. フォルダ構成（増えるもの）

```
components/pixel-switch/{meta.json, preview.html, pixel-switch.css, pixel-switch.js}
tests/pixel-switch-multi.html            … 3組・1組は RTL・スクリプト2回読み込み
tests/test_pixel_switch_browser.py       … 点の位置、切り替え、中断、キー操作、RTL、動きを減らす設定
docs/design/pixel-switch.md, pixel-switch.svg
```

## 8. 確かめられないこと

- スクリーンリーダーでの読み上げ、Safari・Firefox・実機での見た目と動き
