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

2. 出力されたスクショパスをReadツールで画像として読み込み、アプリ名と合わせて以下を判断する:
   - 画面に表示されている内容から作業内容を1行で簡潔に記述
   - プロジェクト推測（NOK関連かIST関連か）

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

- summaryは日本語で簡潔に書く（例: 「Terraformモジュールの検証作業」）
- プロジェクト名がわかれば[NOK]や[IST]をprefixに付ける（例: 「[NOK] サーバー構成図の作成」）
- スクショが真っ暗（スリープ中等）の場合は「離席中」とする
