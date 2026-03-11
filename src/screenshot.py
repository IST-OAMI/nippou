"""スクリーンショット撮影モジュール"""

import subprocess
import time
from datetime import datetime
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
SCREENSHOT_DIR = PROJECT_DIR / "tmp"
APP_PATH = PROJECT_DIR / "ScreenshotHelper.app"
CONFIG_PATH = SCREENSHOT_DIR / "screencapture_config.txt"


def capture_screenshot() -> Path:
    """スクリーンショットを撮影し、プロジェクト内tmpディレクトリに保存する。"""
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    path = SCREENSHOT_DIR / filename

    # configファイルに出力先を書き込み
    CONFIG_PATH.write_text(str(path))

    # .appとして起動（独自のTCCコンテキストで実行される）
    subprocess.run(["open", str(APP_PATH)], check=True)

    # 出力ファイルの出現を待つ（最大10秒）
    for _ in range(100):
        if path.exists() and path.stat().st_size > 0:
            return path
        time.sleep(0.1)

    raise RuntimeError(f"Screenshot capture failed: {path} not created")


def delete_screenshot(path: Path) -> None:
    """スクリーンショットファイルを削除する。"""
    path.unlink(missing_ok=True)
