---
description: スクリーンショットを撮影し、作業内容を分析してログに記録する
---

# screenshot-log

1. Read ツールで `/Users/user/nippou/.claude/commands/screenshot_log_agent_prompt.txt` を読み込む。
2. その内容を `general-purpose` サブエージェントに渡して実行する。
3. サブエージェントの返答（1行）をそのままユーザーに表示する。
4. CronList で `/screenshot-log` のジョブが存在しない場合のみ `/loop 5m /screenshot-log` を実行する。
