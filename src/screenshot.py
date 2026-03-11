"""スクリーンショット撮影モジュール"""

import subprocess
from datetime import datetime
from pathlib import Path

SCREENSHOT_DIR = Path(__file__).resolve().parent.parent / "tmp"


def capture_screenshot() -> Path:
    """スクリーンショットを撮影し、プロジェクト内tmpディレクトリに保存する。"""
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    path = SCREENSHOT_DIR / filename
    subprocess.run(["screencapture", "-x", str(path)], check=True)
    return path


def delete_screenshot(path: Path) -> None:
    """スクリーンショットファイルを削除する。"""
    path.unlink(missing_ok=True)
