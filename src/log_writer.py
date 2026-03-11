"""作業ログ書き込みモジュール"""

from datetime import datetime
from pathlib import Path

LOGS_DIR = Path(__file__).resolve().parent.parent / "logs"


def append_log(app: str, title: str, summary: str, timestamp: datetime | None = None) -> Path:
    """作業ログにエントリを追記する。"""
    ts = timestamp or datetime.now()
    log_file = LOGS_DIR / f"{ts.strftime('%Y-%m-%d')}.md"
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    entry = f"""## {ts.strftime('%H:%M')}
- アプリ: {app}
- タイトル: {title}
- 作業内容: {summary}

"""
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(entry)

    return log_file
