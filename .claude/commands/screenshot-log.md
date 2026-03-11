---
description: スクリーンショットを撮影し、作業内容を分析してログに記録する
---

# screenshot-log

スクリーンショットから作業内容を分析し、日次ログに追記する。

## 手順

1. Bashツールでスクショを撮影する:
```bash
python3 -c "
from src.screenshot import capture_screenshot
print(capture_screenshot())
"
```

2. 出力されたスクショパスをReadツールで画像として読み込み、以下を判断する:
   - 使用中のアプリ名
   - 何の作業をしているか（1行で簡潔に）
   - プロジェクト推測（NOK関連かIST関連か）

3. Bashツールでログに追記する:
```bash
python3 -c "
from src.log_writer import append_log
append_log(app='<判定したアプリ名>', title='<画面から読み取ったタイトル>', summary='<分析した作業内容>')
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
- プロジェクト名がわかれば[NOK]や[IST]をprefixに付ける（例: 「[NOK] サーバー構成図の作成」）
- スクショが真っ暗（スリープ中等）の場合は「離席中」とする
