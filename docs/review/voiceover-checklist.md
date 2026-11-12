# VoiceOver（iPhone）での確認表 — Phase 1 の残り39部品

作成：2026-11-12。Button と同じやり方で、iPhone の VoiceOver を使って1部品ずつ確かめるための表です。

## やり方

1. iPhone の「設定」→「アクセシビリティ」→「VoiceOver」をオンにする（サイドボタンの3回押しで切り替えられるように設定しておくと楽です）。
2. Safari で各部品のページを開く。
3. 1本指で右にスワイプして、「Preview」（見本）の中まで進む。
4. 下の「聞こえるはず」と「やること」を確かめる。
5. チャットで「input OK」のように送る。気になる点があれば「tabs：Details が選択中と読まれなかった」のように一言で。

送ってもらった結果を私が `docs/review/<部品>/screen-reader.md` に記録し、その部品を Stable にします（tests/test_stable_release.py が記録の有無を確かめます）。

**操作の早見表**：右スワイプ＝次へ、左スワイプ＝前へ、ダブルタップ＝押す、上下スワイプ＝値を変える（スライダなど）、2本指で Z を書く＝取り消し（Esc と同じ）。

**「聞こえるはず」について**：Chromium（パソコン用ブラウザ）が作る読み上げ情報から機械的に取り出した、名前と役割の目安です。iPhone の VoiceOver は Safari の情報を使うので、言い方や順番が少し違うことがあります。名前が読まれない・役割が違う・状態（オン/オフ、選択中など）が読まれない、を見つけるのが目的です。

Home の「First five」（Button, Input, Badge, Tabs, Toast）のうち、残り4つを先に並べています。

## 1. Input（First five）

ページ：https://kata-ui.dev/components/input/

やること：3つの入力欄にそれぞれ移動し、ダブルタップでキーボードが出ることを確かめる。

聞こえるはず（目安）：
- 「Email」、テキストフィールド
- 「Used for invoice delivery」、文字
- 「Full name」、テキストフィールド
- 「tanaka」、文字
- 「Please enter your full name」、文字
- 「Search」、テキストフィールド

## 2. Badge（First five）

ページ：https://kata-ui.dev/components/badge/

やること：右スワイプで各バッジの文字が順に読まれることを確かめる（押せる物ではない）。

聞こえるはず（目安）：
- 「Draft」、文字
- 「Live」、文字
- 「Needs action」、文字
- 「In review」、文字
- 「Pro」、文字
- 「3 left」、文字

## 3. Tabs（First five）

ページ：https://kata-ui.dev/components/tabs/

やること：「Details」タブに移動してダブルタップ → 中身が Details に変わり、「選択中」と読まれる。

聞こえるはず（目安）：
- タブの並び
- 「Overview」、タブ、選択中
- 「Details」、タブ
- 「History」、タブ
- 「Overview」、タブの中身
- 「Overview panel — the essentials of the project live here.」、文字

## 4. Toast（First five）

ページ：https://kata-ui.dev/components/toast/

やること：「Show toast」をダブルタップ → 出てきたお知らせの文が自動で読み上げられる。

聞こえるはず（目安）：
- 「Show toast」、ボタン
- 状態のお知らせ（普段は無音）

## 5. Field

ページ：https://kata-ui.dev/components/field/

やること：各入力欄で、名前のあと少し間をおいて下の説明文（ヒントやエラー）が読まれることを確かめる。

聞こえるはず（目安）：
- 「Workspace name」、文字
- 「Optional」、文字
- 「Workspace name Optional」、テキストフィールド
- 「Acme Studio」、文字
- 「Shown in menus and the sidebar. You can change it later.」、文字
- 「Billing email」、文字
- 「Required」、文字
- 「Billing email Required」、テキストフィールド
- 「accounts@acme」、文字
- 「That address is missing its domain.」、文字

## 6. Textarea

ページ：https://kata-ui.dev/components/textarea/

やること：入力欄の名前が読まれ、そのあと下の説明文が読めることを確かめる。

聞こえるはず（目安）：
- 「Release notes」、テキストフィールド
- 「Fixed the export dialog. Copy buttons now confirm with a che」、文字
- 「Markdown is fine. 62 / 280」、文字

## 7. Select

ページ：https://kata-ui.dev/components/select/

やること：「Plan」をダブルタップ → 選択肢の一覧が出て、選べる。

聞こえるはず（目安）：
- 「Plan」、ポップアップ/コンボボックス
- 「Starter」、選択肢
- 「Studio」、選択肢、選択中
- 「Scale」、選択肢
- 「Region」、ポップアップ/コンボボックス
- 「Tokyo」、選択肢、選択中
- 「Osaka」、選択肢
- 「Remote」、選択肢
- 「Availability」、ポップアップ/コンボボックス、使えない（淡色）
- 「Locked」、選択肢、使えない（淡色）

## 8. Checkbox / Radio

ページ：https://kata-ui.dev/components/checkbox/

やること：チェックボックスをダブルタップ → 「オン/オフ」が切り替わって読まれる。ラジオボタンも同じ。

聞こえるはず（目安）：
- 「Send estimate」、チェックボックス、オン/チェックあり
- 「Include travel」、チェックボックス
- 「End of month」、ラジオボタン、オン/チェックあり
- 「End of next month」、ラジオボタン

## 9. Radio group

ページ：https://kata-ui.dev/components/radio/

やること：「Yearly」をダブルタップ → 選択が移る。「Lifetime (sold out)」は使えないと読まれる。

聞こえるはず（目安）：
- 「Billing cycle」、文字
- 「Monthly」、ラジオボタン、オン/チェックあり
- 「Yearly −20%」、ラジオボタン
- 「Lifetime (sold out)」、ラジオボタン、使えない（淡色）

## 10. Switch

ページ：https://kata-ui.dev/components/switch/

やること：各スイッチをダブルタップ → オン/オフが切り替わって読まれる。

聞こえるはず（目安）：
- 「Notifications」、スイッチ、オン/チェックあり
- 「Auto-save」、スイッチ、オン/チェックあり
- 「Public」、スイッチ

## 11. Modal

ページ：https://kata-ui.dev/components/modal/

やること：「Open modal」をダブルタップ → ダイアログの中に移る。2本指で Z を書く（取り消しの動作）と閉じて、元のボタンに戻る。

聞こえるはず（目安）：
- 「Open modal」、ボタン

## 12. Dropdown

ページ：https://kata-ui.dev/components/dropdown/

やること：「Actions」をダブルタップ → メニューが開いて項目を選べる。2本指で Z を書くと閉じてボタンに戻る。

聞こえるはず（目安）：
- 「Actions」、ボタン

## 13. Popover

ページ：https://kata-ui.dev/components/popover/

やること：「Share」をダブルタップ → 中身が出て、その中へ移動できる。2本指で Z を書くと閉じる。

聞こえるはず（目安）：
- 「Share」、ボタン

## 14. Tooltip

ページ：https://kata-ui.dev/components/tooltip/

やること：各ボタンの名前（Copy など）が読まれる。説明の吹き出しの文は名前に混ざらない。

聞こえるはず（目安）：
- 「Copy」、ボタン
- 「Settings」、ボタン
- 「Save」、ボタン

## 15. Card

ページ：https://kata-ui.dev/components/card/

やること：見出し「Usage this month」から順に、文とボタンが読まれる。

聞こえるはず（目安）：
- 「Usage this month」、見出し
- 「Across all projects in this workspace.」、文字
- 「On track」、文字
- 「Build minutes are at 62% with nine days left. The deploy que」、文字
- 「Updated 2 hours ago」、文字
- 「Details」、ボタン
- 「Open report」、ボタン

## 16. Accordion

ページ：https://kata-ui.dev/components/accordion/

やること：各質問をダブルタップ → 開く/閉じるが読まれ、開いたら答えの文が読める。

聞こえるはず（目安）：
- 「Is there a build step?」、開閉ボタン、開いている
- 「No. Copy the CSS, paste the markup. This accordion itself ru」、文字
- 「Does it work in dark mode?」、開閉ボタン
- 「Can I change the radius?」、開閉ボタン

## 17. Alert

ページ：https://kata-ui.dev/components/alert/

やること：4つのお知らせの見出しと本文が順に読まれる（アイコンは読まれない）。

聞こえるはず（目安）：
- 「Deploy scheduled.」、文字
- 「The new version goes out at 02:00 JST. No action needed.」、文字
- 「Backup complete.」、文字
- 「All 128 files verified against the manifest.」、文字
- 「Storage at 86%.」、文字
- 「Exports stop working at 100%. Clear old previews or raise th」、文字
- 「Payment failed.」、文字
- 「The card on file was declined. Update it before the next inv」、文字

## 18. Table

ページ：https://kata-ui.dev/components/table/

やること：表の中を移動し、列見出し（Project / Owner / Status / Amount）と中身が対応して読まれる。

聞こえるはず（目安）：
- 「Projects」、領域
- 表
- 「Project」、列見出し
- 「Owner」、列見出し
- 「Status」、列見出し
- 「Amount」、列見出し
- 「Product launch」、セル
- 「Yamada」、セル
- 「Confirmed」、セル
- 「$860」、セル
- …ほか 8 項目

## 19. Pagination

ページ：https://kata-ui.dev/components/pagination/

やること：「Pagination」のまとまりの中で、今のページが「現在のページ」と読まれる。

聞こえるはず（目安）：
- 「Pagination」、ナビゲーション
- 「Previous page」、リンク
- 「1」、リンク
- 「2」、リンク
- 「3」、リンク
- 「4」、リンク
- 「18」、リンク
- 「Next page」、リンク
- 「Pagination, first page」、ナビゲーション
- 「1」、リンク
- …ほか 7 項目

## 20. Breadcrumbs

ページ：https://kata-ui.dev/components/breadcrumbs/

やること：「Breadcrumb」のまとまりの中で、Home → Projects … と読まれ、最後が今のページと読まれる。

聞こえるはず（目安）：
- 「Breadcrumb」、ナビゲーション
- リスト
- リストの項目
- 「Home」、リンク
- リストの項目
- 「Projects」、リンク
- リストの項目
- 「kata-ui」、リンク
- リストの項目
- 「Components」、文字

## 21. Alert Dialog

ページ：https://kata-ui.dev/components/alert-dialog/

やること：「Delete project」をダブルタップ → 確認ダイアログの中へ移る。最初は取り消し側のボタンにいる。

聞こえるはず（目安）：
- 「Delete project」、ボタン

## 22. Drawer

ページ：https://kata-ui.dev/components/drawer/

やること：「Open drawer」をダブルタップ → 横から出た面の中へ移る。2本指で Z を書くと閉じて元のボタンに戻る。

聞こえるはず（目安）：
- 「Open drawer」、ボタン

## 23. Combobox

ページ：https://kata-ui.dev/components/combobox/

やること：「Framework」をダブルタップして文字を入れる → 候補の数が読み上げられ、候補を選べる。

聞こえるはず（目安）：
- 「Framework」、ポップアップ/コンボボックス
- 「Astro」、文字
- 状態のお知らせ（普段は無音）

## 24. Date Picker

ページ：https://kata-ui.dev/components/date-picker/

やること：「Open calendar」をダブルタップ → カレンダーの中で日付を選ぶと入力欄に入る。

聞こえるはず（目安）：
- 「Date」、テキストフィールド
- 「Open calendar」、ボタン

## 25. Slider

ページ：https://kata-ui.dev/components/slider/

やること：「Volume」で上下にスワイプ → 値が増減して読まれる。

聞こえるはず（目安）：
- 「Volume」、スライダ
- 「Brightness」、スライダ

## 26. Toggle

ページ：https://kata-ui.dev/components/toggle/

やること：各ボタンをダブルタップ → 「押されている」かどうかが切り替わって読まれる。

聞こえるはず（目安）：
- 「Pinned」、ボタン、押されている
- 「Bold」、ボタン、押されている
- 「Italic」、ボタン
- 「Underline」、ボタン

## 27. Segmented control

ページ：https://kata-ui.dev/components/segmented/

やること：「Range」の中で別の項目をダブルタップ → 選択が移る。

聞こえるはず（目安）：
- 「Range」、ラジオボタンのまとまり
- 「Day」、ラジオボタン、オン/チェックあり
- 「Week」、ラジオボタン
- 「Month」、ラジオボタン
- 「Density」、ラジオボタンのまとまり
- 「Comfort」、ラジオボタン
- 「Compact」、ラジオボタン、オン/チェックあり

## 28. Avatar

ページ：https://kata-ui.dev/components/avatar/

やること：人の画像が名前つきで読まれる（例：「Aki Morita, online」）。頭文字だけのものは読まれなくてよい。

聞こえるはず（目安）：
- 「Aki Morita, online」、画像
- 「AM」、文字
- 「Ren A., Mio T., Jun O. and 3 more」、画像
- 「RA」、文字
- 「MT」、文字
- 「JO」、文字
- 「+3」、文字

## 29. Progress

ページ：https://kata-ui.dev/components/progress/

やること：各バーが名前と割合（例：Uploading footage 68%）で読まれる。

聞こえるはず（目安）：
- 「Uploading footage」、文字
- 「68%」、文字
- 「Uploading footage」、進行状況
- 「Verifying files」、文字
- 「92%」、文字
- 「Verifying files」、進行状況

## 30. Skeleton

ページ：https://kata-ui.dev/components/skeleton/

やること：「Loading profile」が読まれる。灰色の帯そのものは読まれない。

聞こえるはず（目安）：
- 状態のお知らせ（普段は無音）
- 「Loading profile」、文字

## 31. Spinner

ページ：https://kata-ui.dev/components/spinner/

やること：「Loading」が読まれる。「Saving…」ボタンは使えないと読まれる。

聞こえるはず（目安）：
- 「Loading」、状態のお知らせ（普段は無音）
- 「Loading」、状態のお知らせ（普段は無音）
- 「Loading」、状態のお知らせ（普段は無音）
- 「Saving…」、ボタン、使えない（淡色）

## 32. Empty state

ページ：https://kata-ui.dev/components/empty-state/

やること：見出し「No exports yet」、説明文、ボタンの順に読まれる。絵は読まれない。

聞こえるはず（目安）：
- 「No exports yet」、見出し
- 「Exports you create will appear here, ready to download or sh」、文字
- 「Create export」、ボタン

## 33. Separator

ページ：https://kata-ui.dev/components/separator/

やること：区切り線が「区切り」と読まれる（飾りの線は読まれない）。

聞こえるはず（目安）：
- 「Account details」、文字
- 区切り
- 「Billing address」、文字
- 「OR」、文字
- 「Docs」、文字
- 「Support」、文字
- 「Community」、文字

## 34. Sidebar

ページ：https://kata-ui.dev/components/sidebar/

やること：「Sidebar preview」の中で、項目が順に読まれ、「Projects」は開いている/閉じていると読まれる。

聞こえるはず（目安）：
- 「Sidebar preview」、ナビゲーション
- 「Northwind」、文字
- 「MAIN」、文字
- 「Overview」、リンク
- 「Projects」、ボタン、開いている
- 「Website rebuild」、リンク
- 「Mobile app」、リンク
- 「Brand refresh」、リンク
- 「Calendar 3」、リンク
- 「Reports」、リンク
- …ほか 7 項目

## 35. Command

ページ：https://kata-ui.dev/components/command/

やること：「Search…」をダブルタップ → 検索の画面が開く。文字を入れると結果の数が読まれる。2本指で Z を書くと閉じる。

聞こえるはず（目安）：
- 「Search… ⌘ K」、ボタン

## 36. Context Menu

ページ：https://kata-ui.dev/components/context-menu/

やること：この部品は右クリック・Shift+F10・メニューキーで開きます。iPhone だけでは開けないので、範囲の文字が読まれることだけ確かめてください（メニュー本体の読み上げは、キーボードのある端末での確認が別に必要です）。

聞こえるはず（目安）：
- 「Right-click in this area」、文字
- 「(or press Shift+F10)」、文字

## 37. Hover Card

ページ：https://kata-ui.dev/components/hover-card/

やること：「Aoi Kimura」のリンクに移動したとき、カードの内容が読まれるか確かめる。読まれなくても不具合とは限りません（触る端末では Popover を使う前提の部品です）。どちらだったかを教えてください。

聞こえるはず（目安）：
- 「The release notes were drafted by」、文字
- 「Aoi Kimura」、リンク
- 「and are ready for review.」、文字

## 38. Data Table

ページ：https://kata-ui.dev/components/data-table/

やること：「Select all rows」をダブルタップ → 全部の行が選ばれる。列見出しのボタンで並び替えができ、並び順が読まれる。

聞こえるはず（目安）：
- 「Members」、領域
- 「Members」、表
- 「Select all rows」、列見出し
- 「Select all rows」、チェックボックス
- 「NAME」、列見出し
- 「NAME」、ボタン
- 「ROLE」、列見出し
- 「STATUS」、列見出し
- 「BILLED」、列見出し
- 「BILLED」、ボタン
- …ほか 34 項目

## 39. File Upload

ページ：https://kata-ui.dev/components/file-upload/

やること：「Drop files here, or browse」をダブルタップ → ファイルを選ぶ画面が出る。一覧のファイル名と大きさが読まれる。

聞こえるはず（目安）：
- 「Drop files here, or browse PNG, JPG or PDF — up to 10 MB eac」、ボタン
- 「PNG, JPG or PDF — up to 10 MB each」、文字
- リスト
- リストの項目
- 「q3-board-deck.pdf」、文字
- 「2.4 MB」、文字
- 「Remove q3-board-deck.pdf」、ボタン
- 状態のお知らせ（普段は無音）

