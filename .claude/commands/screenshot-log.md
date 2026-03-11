---
description: スクリーンショットを撮影し、作業内容を分析してログに記録する
---

# screenshot-log

スクリーンショットとアクティブアプリ名から作業内容を分析し、日次ログに追記する。

## 手順

1. Bashツールでスクショ撮影とアクティブアプリ名を取得する:
```bash
python3 -c "
from src.screenshot import capture_screenshot
from src.active_app import get_active_app

path = capture_screenshot()
app = get_active_app()
print(f'screenshot: {path}')
print(f'app: {app}')
"
```

2. 出力されたスクショパスをReadツールで画像として読み込み、**画面内容を徹底的に読み取って**以下を判断する:
   - **具体的な作業内容**を1行で記述する（後述の「分析ガイド」に従う）
   - プロジェクト推測（NOK関連かIST関連か）

### 分析ガイド — summaryの解像度を上げる

スクショから以下を可能な限り読み取り、summaryに反映すること:

- **ブラウザ**: タブタイトル、URL（ドメイン・パス）、ページ内の見出し・本文のキーワード
  - 良い例: 「AWS EC2 Linuxインスタンスの起動手順を調査」「SSM Agentの接続トラブルシュート」「Terraformドキュメントでaws_instance設定を確認」
  - 悪い例: 「ブラウザでの調査・確認作業」（←具体性ゼロ、禁止）
- **ターミナル**: 実行中のコマンド、ディレクトリ、出力内容
  - 良い例: 「terraform planでEC2モジュールの差分確認」「ssh経由でNginxログを調査」
  - 悪い例: 「ターミナルでの作業」（←禁止）
- **エディタ(VS Code等)**: 開いているファイル名、編集中のコード内容、言語
  - 良い例: 「main.tfのセキュリティグループ設定を編集」
  - 悪い例: 「VS Codeでの作業」（←禁止）
- **デスクトップのみ表示（ウィンドウなし）**: メニューバーのアプリ名だけ記載し「デスクトップ表示中」とする。無理に作業内容を推測しない

3. Bashツールでログ追記+スクショ削除を一括実行する:
```bash
python3 -c "
from src.screenshot import delete_screenshot
from src.log_writer import append_log
from pathlib import Path
append_log(app='<アプリ名>', title='<画面から読み取ったタイトル>', summary='<分析した作業内容>')
delete_screenshot(Path('<スクショパス>'))
print('記録完了')
"
```

## 注意事項

- summaryは日本語で**具体的に**書く
  - OK: 「AWS EC2 Linuxのセキュリティグループ設定を調査」「SSM Agent接続エラーの対処法を検索」
  - NG: 「ブラウザでの調査・確認作業」「ターミナルでの作業」「VS Codeでの作業」← **この粒度は禁止**
- 画面に読み取れるサービス名・技術名・ファイル名があれば必ず含める
- プロジェクト名がわかれば[NOK]や[IST]をprefixに付ける（例: 「[NOK] サーバー構成図の作成」）
- スクショが真っ暗（スリープ中等）の場合は「離席中」とする
- デスクトップ壁紙のみでウィンドウが見えない場合は「デスクトップ表示中」とし、作業内容を捏造しない
