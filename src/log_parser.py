"""ログ解析モジュール"""

import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

LOGS_DIR = Path(__file__).resolve().parent.parent / "logs"


@dataclass
class LogEntry:
    timestamp: datetime
    app: str
    title: str
    summary: str


def parse_log(date: datetime | None = None) -> list[LogEntry]:
    """指定日のログファイルを読み込み、構造化データのリストを返す。"""
    d = date or datetime.now()
    log_file = LOGS_DIR / f"{d.strftime('%Y-%m-%d')}.md"

    if not log_file.exists():
        return []

    text = log_file.read_text(encoding="utf-8")
    entries = []
    blocks = re.split(r"(?=^## \d{2}:\d{2})", text, flags=re.MULTILINE)

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        time_match = re.match(r"^## (\d{2}:\d{2})", block)
        if not time_match:
            continue

        ts = datetime.strptime(
            f"{d.strftime('%Y-%m-%d')} {time_match.group(1)}", "%Y-%m-%d %H:%M"
        )
        app = _extract_field(block, "アプリ")
        title = _extract_field(block, "タイトル")
        summary = _extract_field(block, "作業内容")

        entries.append(LogEntry(timestamp=ts, app=app, title=title, summary=summary))

    return entries


def _extract_field(block: str, field_name: str) -> str:
    """ログブロックからフィールドを抽出する。"""
    match = re.search(rf"^- {field_name}: (.+)$", block, re.MULTILINE)
    return match.group(1).strip() if match else ""
