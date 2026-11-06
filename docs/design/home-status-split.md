# ホームページに Stable / Beta の数を出す：設計書（案）

作成：2026-11-06　状態：**案 A に決定・実装済み（PR #89）**

## 1. 要件
ROADMAP Phase 1「Show the measured Stable / Beta split on the home page」。部品の meta.json に書かれた状態（stable / beta）を build.py が数え、ホームページの一番上に出す。手で数字を書かない（部品の状態が変われば自動で変わる）。

## 2. 事実（2026-11-06 の main で数えた）
- 部品は全部で136。meta.json の状態は **stable 13・beta 123**。
- stable の13部品：bottom-navigation, button-group, calendar, collapsible, descriptions, input-group, navigation-menu, result, scrollspy, shine-text, time-picker, transfer, typeset。
- **この13部品は、Phase 1 の決まり（チェック＋スクリーンリーダー確認を記録してから Stable）を通っていません。** 昔のラベルのままです。T4 では、同じような昔の stable（Badge・Sidebar など）を beta に直してきました。
- T4 で仕上げた40部品は、スクリーンリーダー確認がまだなので全部 beta です。

## 3. 決めてほしいこと（どちらかを選んでください）

| 案 | 表示 | よい点 | 気になる点 |
|---|---|---|---|
| **A（おすすめ）** | 先に13部品を beta に直し、**Stable 0 · Beta 136** と出す | 決まりどおりで、数字にうそがない。スクリーンリーダー確認が済んだ部品から Stable が増えていく | 見た目の数字は弱い |
| B | 今のまま **Stable 13 · Beta 123** と出す | 作業が小さい | 決まりを通っていない13部品を Stable と数えることになる |

おすすめは A です。KATA UI は「数字はチェックの結果から出す」をうたっているので、決まりを通っていない Stable を数えると、その約束とずれます。

## 4. 画面（`home-status-split.svg` 参照）
ヒーローの一番上の小さな行（いまは「136 components · 21 blocks · 7 templates」）に、状態の内訳を足します。

- 変更前：`136 components · 21 blocks · 7 templates`
- 変更後：`136 components (0 stable · 136 beta) · 21 blocks · 7 templates`（案 A の場合）
- 「stable」「beta」は部品一覧の絞り込み `/components/?status=…` へのリンクにする（一覧ページがこの指定を読むように足した）。

文字の大きさ・色・フォントは今の行と同じです（新しい部品や色は足しません）。

## 5. 作り
- `build.py`：部品の meta.json から stable / beta を数える関数を足し、ヒーローの行に入れる。
- テスト：`tests/test_home_status_split.py`（生成されたホームの数字が meta.json の数と一致するか）。
- 案 A の場合：13部品の meta.json の状態を beta にし、HANDOFF・ROADMAP に理由を書く。

## 6. 確かめられないこと
- スクリーンリーダー、Safari、Firefox、実機。
