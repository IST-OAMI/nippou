"""アクティブウィンドウ情報取得モジュール"""

import subprocess


def get_active_window() -> dict[str, str]:
    """アクティブウィンドウのアプリ名とタイトルを返す。"""
    app = _run_osascript(
        'tell application "System Events" to get name of first application process whose frontmost is true'
    )
    title = _run_osascript(
        'tell application "System Events" to get name of front window of (first application process whose frontmost is true)'
    )
    return {"app": app, "title": title}


def _run_osascript(script: str) -> str:
    """osascriptを実行して結果を返す。エラー時は空文字。"""
    try:
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True, text=True, timeout=5,
        )
        return result.stdout.strip()
    except (subprocess.TimeoutExpired, subprocess.SubprocessError):
        return ""
