"""Write docs/review/voiceover-checklist.md for the Phase 1 parts that lack a screen-reader record.

Usage: python3 build.py && python3 -m tools.voiceover_checklist

For each part, the built page /components/<slug>/ is opened in Chromium and the
accessibility tree under the preview stage (#stage) gives the names, roles and
states listed under "聞こえるはず". VoiceOver on iOS reads WebKit's tree, so its
wording and order can differ; the list is a guide for the owner's iPhone pass.
"""
import functools
import os
import shutil
import http.server
import json
import sys
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHROMIUM = os.environ.get('CHROMIUM_PATH') or shutil.which('chromium') or '/usr/bin/chromium'
SLUGS = 'input badge tabs toast field textarea select checkbox radio switch modal dropdown popover tooltip card accordion alert table pagination breadcrumbs alert-dialog drawer combobox date-picker slider toggle segmented avatar progress skeleton spinner empty-state separator sidebar command context-menu hover-card data-table file-upload'.split()


class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


SKIP = {'generic', 'none', 'StaticText', 'InlineTextBox', 'LineBreak', 'paragraph', 'group',
        'LayoutTable', 'LayoutTableRow', 'LayoutTableCell'}
SHOWN_UNNAMED = {'separator', 'progressbar', 'img', 'table', 'tablist', 'tabpanel', 'list', 'listitem',
                 'status', 'alert', 'dialog'}
STATES = ('checked', 'pressed', 'expanded', 'selected', 'disabled', 'busy')


def walk(nodes):
    """(role, name, states) in reading order for one subtree of the Chromium AX tree."""
    by = {n['nodeId']: n for n in nodes}
    out = []

    def rec(n):
        role = (n.get('role') or {}).get('value', '')
        name = ((n.get('name') or {}).get('value') or '').strip()
        props = {p['name']: p['value'].get('value') for p in n.get('properties', []) if 'value' in p}
        if not n.get('ignored') and role == 'StaticText' and name and not any(name in o[1] for o in out[-3:]):
            out.append(('text', name[:60], []))
        elif not n.get('ignored') and role not in SKIP and (name or role in SHOWN_UNNAMED):
            states = [k for k in STATES if props.get(k) not in (None, False, 'false')]
            out.append((role, name[:60], [k if props[k] in (True, 'true') else f'{k}={props[k]}' for k in states]))
        for c in n.get('childIds', []):
            if c in by:
                rec(by[c])
    rec(nodes[0])
    return out


def collect(slugs):
    from playwright.sync_api import sync_playwright
    srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Q, directory=str(ROOT / 'dist')))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    res = {}
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROMIUM, args=['--no-sandbox'])
            page = browser.new_page(viewport={'width': 1280, 'height': 900}, reduced_motion='reduce')
            for slug in slugs:
                page.goto(f'http://127.0.0.1:{srv.server_port}/components/{slug}/')
                page.wait_for_timeout(300)
                cdp = page.context.new_cdp_session(page)
                doc = cdp.send('DOM.getDocument', {'depth': 0})
                node = cdp.send('DOM.querySelector', {'nodeId': doc['root']['nodeId'], 'selector': '#stage'})['nodeId']
                stage = cdp.send('Accessibility.getPartialAXTree', {'nodeId': node, 'fetchRelatives': False})['nodes'][0]
                full = cdp.send('Accessibility.getFullAXTree')['nodes']
                by = {n['nodeId']: n for n in full}
                sub = []

                def gather(n):
                    sub.append(n)
                    for c in n.get('childIds', []):
                        if c in by:
                            gather(by[c])
                gather(next(n for n in full if n.get('backendDOMNodeId') == stage.get('backendDOMNodeId')))
                res[slug] = walk(sub)
                cdp.detach()
            browser.close()
    finally:
        srv.shutdown()
        srv.server_close()
    return res


def main():
    ax = collect(SLUGS)
    meta={s: json.load(open(ROOT / 'components' / s / 'meta.json', encoding='utf-8')) for s in ax}
    ROLE={'textbox':'テキストフィールド','button':'ボタン','switch':'スイッチ','checkbox':'チェックボックス','radio':'ラジオボタン','tab':'タブ','tablist':'タブの並び','tabpanel':'タブの中身','slider':'スライダ','link':'リンク','heading':'見出し','combobox':'ポップアップ/コンボボックス','option':'選択肢','navigation':'ナビゲーション','list':'リスト','listitem':'リストの項目','table':'表','columnheader':'列見出し','rowheader':'行見出し','cell':'セル','row':'行','region':'領域','status':'状態のお知らせ（普段は無音）','progressbar':'進行状況','image':'画像','separator':'区切り','radiogroup':'ラジオボタンのまとまり','DisclosureTriangle':'開閉ボタン','dialog':'ダイアログ','menu':'メニュー','menuitem':'メニュー項目','text':'文字','gridcell':'セル','alert':'警告'}
    ST={'checked':'オン/チェックあり','selected':'選択中','pressed':'押されている','expanded':'開いている','disabled':'使えない（淡色）'}
    # Steps owners do with VoiceOver on iPhone. Swipe right = next item; double-tap = activate;
    # two-finger scrub (Z) = Escape.
    DO={
    'input':'3つの入力欄にそれぞれ移動し、ダブルタップでキーボードが出ることを確かめる。',
    'badge':'右スワイプで各バッジの文字が順に読まれることを確かめる（押せる物ではない）。',
    'tabs':'「Details」タブに移動してダブルタップ → 中身が Details に変わり、「選択中」と読まれる。',
    'toast':'「Show toast」をダブルタップ → 出てきたお知らせの文が自動で読み上げられる。',
    'field':'各入力欄で、名前のあと少し間をおいて下の説明文（ヒントやエラー）が読まれることを確かめる。',
    'textarea':'入力欄の名前が読まれ、そのあと下の説明文が読めることを確かめる。',
    'select':'「Plan」をダブルタップ → 選択肢の一覧が出て、選べる。',
    'checkbox':'チェックボックスをダブルタップ → 「オン/オフ」が切り替わって読まれる。ラジオボタンも同じ。',
    'radio':'「Yearly」をダブルタップ → 選択が移る。「Lifetime (sold out)」は使えないと読まれる。',
    'switch':'各スイッチをダブルタップ → オン/オフが切り替わって読まれる。',
    'modal':'「Open modal」をダブルタップ → ダイアログの中に移る。2本指で Z を書く（取り消しの動作）と閉じて、元のボタンに戻る。',
    'dropdown':'「Actions」をダブルタップ → メニューが開いて項目を選べる。2本指で Z を書くと閉じてボタンに戻る。',
    'popover':'「Share」をダブルタップ → 中身が出て、その中へ移動できる。2本指で Z を書くと閉じる。',
    'tooltip':'各ボタンの名前（Copy など）が読まれる。説明の吹き出しの文は名前に混ざらない。',
    'card':'見出し「Usage this month」から順に、文とボタンが読まれる。',
    'accordion':'各質問をダブルタップ → 開く/閉じるが読まれ、開いたら答えの文が読める。',
    'alert':'4つのお知らせの見出しと本文が順に読まれる（アイコンは読まれない）。',
    'table':'表の中を移動し、列見出し（Project / Owner / Status / Amount）と中身が対応して読まれる。',
    'pagination':'「Pagination」のまとまりの中で、今のページが「現在のページ」と読まれる。',
    'breadcrumbs':'「Breadcrumb」のまとまりの中で、Home → Projects … と読まれ、最後が今のページと読まれる。',
    'alert-dialog':'「Delete project」をダブルタップ → 確認ダイアログの中へ移る。最初は取り消し側のボタンにいる。',
    'drawer':'「Open drawer」をダブルタップ → 横から出た面の中へ移る。2本指で Z を書くと閉じて元のボタンに戻る。',
    'combobox':'「Framework」をダブルタップして文字を入れる → 候補の数が読み上げられ、候補を選べる。',
    'date-picker':'「Open calendar」をダブルタップ → カレンダーの中で日付を選ぶと入力欄に入る。',
    'slider':'「Volume」で上下にスワイプ → 値が増減して読まれる。',
    'toggle':'各ボタンをダブルタップ → 「押されている」かどうかが切り替わって読まれる。',
    'segmented':'「Range」の中で別の項目をダブルタップ → 選択が移る。',
    'avatar':'人の画像が名前つきで読まれる（例：「Aki Morita, online」）。頭文字だけのものは読まれなくてよい。',
    'progress':'各バーが名前と割合（例：Uploading footage 68%）で読まれる。',
    'skeleton':'「Loading profile」が読まれる。灰色の帯そのものは読まれない。',
    'spinner':'「Loading」が読まれる。「Saving…」ボタンは使えないと読まれる。',
    'empty-state':'見出し「No exports yet」、説明文、ボタンの順に読まれる。絵は読まれない。',
    'separator':'区切り線が「区切り」と読まれる（飾りの線は読まれない）。',
    'sidebar':'「Sidebar preview」の中で、項目が順に読まれ、「Projects」は開いている/閉じていると読まれる。',
    'command':'「Search…」をダブルタップ → 検索の画面が開く。文字を入れると結果の数が読まれる。2本指で Z を書くと閉じる。',
    'context-menu':'この部品は右クリック・Shift+F10・メニューキーで開きます。iPhone だけでは開けないので、範囲の文字が読まれることだけ確かめてください（メニュー本体の読み上げは、キーボードのある端末での確認が別に必要です）。',
    'hover-card':'「Aoi Kimura」のリンクに移動したとき、カードの内容が読まれるか確かめる。読まれなくても不具合とは限りません（触る端末では Popover を使う前提の部品です）。どちらだったかを教えてください。',
    'data-table':'「Select all rows」をダブルタップ → 全部の行が選ばれる。列見出しのボタンで並び替えができ、並び順が読まれる。',
    'file-upload':'「Drop files here, or browse」をダブルタップ → ファイルを選ぶ画面が出る。一覧のファイル名と大きさが読まれる。',
    }
    FIRST=['input','badge','tabs','toast']
    order=FIRST+[s for s in ax if s not in FIRST]
    out=['# VoiceOver（iPhone）での確認表 — Phase 1 の残り39部品','',
    '作成：2026-11-12。Button と同じやり方で、iPhone の VoiceOver を使って1部品ずつ確かめるための表です。',
    '',
    '## やり方',
    '',
    '1. iPhone の「設定」→「アクセシビリティ」→「VoiceOver」をオンにする（サイドボタンの3回押しで切り替えられるように設定しておくと楽です）。',
    '2. Safari で各部品のページを開く。',
    '3. 1本指で右にスワイプして、「Preview」（見本）の中まで進む。',
    '4. 下の「聞こえるはず」と「やること」を確かめる。',
    '5. チャットで「input OK」のように送る。気になる点があれば「tabs：Details が選択中と読まれなかった」のように一言で。',
    '',
    '送ってもらった結果を私が `docs/review/<部品>/screen-reader.md` に記録し、その部品を Stable にします（tests/test_stable_release.py が記録の有無を確かめます）。',
    '',
    '**操作の早見表**：右スワイプ＝次へ、左スワイプ＝前へ、ダブルタップ＝押す、上下スワイプ＝値を変える（スライダなど）、2本指で Z を書く＝取り消し（Esc と同じ）。',
    '',
    '**「聞こえるはず」について**：Chromium（パソコン用ブラウザ）が作る読み上げ情報から機械的に取り出した、名前と役割の目安です。iPhone の VoiceOver は Safari の情報を使うので、言い方や順番が少し違うことがあります。名前が読まれない・役割が違う・状態（オン/オフ、選択中など）が読まれない、を見つけるのが目的です。',
    '',
    'Home の「First five」（Button, Input, Badge, Tabs, Toast）のうち、残り4つを先に並べています。',
    '']
    for n,s in enumerate(order,1):
        m=meta[s]
        out.append(f'## {n}. {m["title"]}'+('（First five）' if s in FIRST else ''))
        out.append('')
        out.append(f'ページ：https://kata-ui.dev/components/{s}/')
        out.append('')
        out.append(f'やること：{DO[s]}')
        out.append('')
        seq=ax[s]
        # A label read just before its own control is the same announcement; keep the control.
        seq=[it for k,it in enumerate(seq) if not (it[0]=='text' and k+1<len(seq) and seq[k+1][0]!='text' and seq[k+1][1].startswith(it[1]))]
        ax[s]=seq
        items=seq[:10]
        if items:
            out.append('聞こえるはず（目安）：')
            for role,name,st in items:
                r=ROLE.get(role,role)
                stt='、'.join(ST.get(x.split('=')[0],x) for x in st)
                label=f'「{name}」' if name else ''
                out.append(f'- {label}{"、" if label else ""}{r}{"、"+stt if stt else ""}')
            if len(ax[s])>10: out.append(f'- …ほか {len(ax[s])-10} 項目')
        out.append('')
    (ROOT / 'docs' / 'review' / 'voiceover-checklist.md').write_text('\n'.join(out) + '\n', encoding='utf-8')
    print(len(order), 'parts')
    return 0


if __name__ == '__main__':
    sys.exit(main())
