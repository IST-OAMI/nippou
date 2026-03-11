"""スクリーンショット撮影モジュール"""

import subprocess
import tempfile
from pathlib import Path


def capture_screenshot() -> Path:
    """スクリーンショットを撮影し、一時ファイルのパスを返す。"""
    tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False, dir=tempfile.gettempdir())
    tmp.close()
    path = Path(tmp.name)
    subprocess.run(["screencapture", "-x", str(path)], check=True)
    return path


def delete_screenshot(path: Path) -> None:
    """スクリーンショットファイルを削除する。"""
    path.unlink(missing_ok=True)
