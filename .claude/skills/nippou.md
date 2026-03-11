---
description: 当日の作業ログから日報を自動生成する
---

# nippou

当日の作業ログ（logs/YYYY-MM-DD.md）を読み込み、template.mdに沿った日報を生成する。

## 手順

1. Bashツールで当日のログを解析し、カテゴリ分類と時間算出を行う:
```bash
python3 -c "
from src.log_parser import parse_log
from src.categorizer import categorize_all
from src.time_calculator import calculate_hours
import json

entries = parse_log()
categorized = categorize_all(entries)
hours = calculate_hours(categorized)

print('=== 分類結果 ===')
for ce in categorized:
    print(f'{ce.entry.timestamp.strftime(\"%H:%M\")} [{ce.project}][{ce.category}] {ce.entry.summary}')
print()
print('=== 時間配分 ===')
for key, h in hours.items():
    print(f'{key} {h:.1f}h')
"
```

2. Readツールで当日のログファイル `logs/YYYY-MM-DD.md` を読み込み、全体の作業内容を把握する。

3. ログ全体を見て以下を生成する:
   - **やったこと**: 作業を3〜5項目にグルーピングし、各項目に2〜3個の詳細を付ける
   - **学んだこと**: 作業から得られた学びを抽象化して3項目にまとめる（技術的な発見、プロセスの改善点など）

4. Bashツールで日報を生成する:
```bash
python3 -c "
from src.log_parser import parse_log
from src.categorizer import categorize_all
from src.report_generator import generate_report

entries = parse_log()
categorized = categorize_all(entries)

activities = [
    '<やったこと1タイトル>\n- <詳細1>\n- <詳細2>',
    '<やったこと2タイトル>\n- <詳細1>\n- <詳細2>',
    '<やったこと3タイトル>\n- <詳細1>\n- <詳細2>',
]
learnings = [
    '<学んだこと1タイトル>\n- <詳細1>\n- <詳細2>',
    '<学んだこと2タイトル>\n- <詳細1>\n- <詳細2>',
    '<学んだこと3タイトル>\n- <詳細1>\n- <詳細2>',
]

path = generate_report(categorized, activities, learnings)
print(f'日報を生成しました: {path}')
"
```

5. Readツールで生成された `output/YYYY-MM-DD.md` を読み込み、内容をユーザーに表示する。

## 注意事項

- activitiesとlearningsの中身はステップ3で考えた内容を埋める
- 学んだことは具体的な作業内容ではなく、抽象化した知見にする（例: 「Terraformのstate管理ではbackend設定の一貫性が重要」）
- 所感・明日活かす具体策は空欄のまま残す（ユーザーが手動で記入）
