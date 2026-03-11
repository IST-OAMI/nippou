"""アクティブアプリ取得モジュール（権限不要）"""

import subprocess


def get_active_app() -> str:
    """最前面アプリ名を返す。lsappinfoを使用しSystem Events権限不要。"""
    try:
        front = subprocess.run(
            ["lsappinfo", "front"],
            capture_output=True, text=True, timeout=5,
        )
        app_id = front.stdout.strip()
        if not app_id:
            return ""

        info = subprocess.run(
            ["lsappinfo", "info", "-only", "name", app_id],
            capture_output=True, text=True, timeout=5,
        )
        # "LSDisplayName"="アプリ名" の形式からアプリ名を抽出
        line = info.stdout.strip()
        if '"LSDisplayName"="' in line:
            return line.split('"LSDisplayName"="')[1].rstrip('"')
        return ""
    except (subprocess.TimeoutExpired, subprocess.SubprocessError):
        return ""
