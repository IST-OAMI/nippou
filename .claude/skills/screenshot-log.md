---
description: スクリーンショットを撮影し、作業内容を分析してログに記録する
---

# screenshot-log

スクリーンショットとアクティブウィンドウ情報から作業内容を分析し、日次ログに追記する。

## 手順

1. Bashツールで以下のPythonスクリプトを実行し、スクショ撮影とウィンドウ情報取得を行う:
```bash
python3 -c "
from src.screenshot import capture_screenshot
from src.window_info import get_active_window
import json

path = capture_screenshot()
window = get_active_window()
print(json.dumps({'screenshot': str(path), 'app': window['app'], 'title': window['title']}))
"
```

2. 出力されたスクリーンショットのパスをReadツールで読み込み（画像として分析される）、ウィンドウ情報と合わせて以下を判断する:
   - 何の作業をしているか（1行で簡潔に）
   - プロジェクト推測の手がかり（NOK関連かIST関連か）

3. Bashツールで以下のPythonスクリプトを実行し、ログに追記する:
```bash
python3 -c "
from src.log_writer import append_log
append_log(app='<アプリ名>', title='<タイトル>', summary='<分析した作業内容>')
"
```

4. Bashツールでスクショを削除する:
```bash
python3 -c "
from src.screenshot import delete_screenshot
from pathlib import Path
delete_screenshot(Path('<スクショパス>'))
"
```

## 注意事項

- summaryは日本語で簡潔に書く（例: 「Terraformモジュールの検証作業」）
- プロジェクト名がわかる場合はsummaryに含める（例: 「[NOK] サーバー構成図の作成」）
- スクショが真っ暗（スリープ中等）の場合は「離席中」とする
