"""作業時間算出モジュール"""

import math
from collections import defaultdict
from .categorizer import CategorizedEntry

TOTAL_WORK_HOURS = 8.0


def calculate_hours(entries: list[CategorizedEntry]) -> dict[str, dict[str, float]]:
    """カテゴリ・プロジェクト別の作業時間を0.5h単位で算出する。

    Returns:
        {"NOK_インフラ支援）【MTG】": 1.0, ...} のような辞書
    """
    if not entries:
        return {}

    # エントリ間の時間差から各作業の所要時間を推定
    raw_minutes: dict[str, float] = defaultdict(float)

    for i, ce in enumerate(entries):
        if i + 1 < len(entries):
            delta = (entries[i + 1].entry.timestamp - ce.entry.timestamp).total_seconds() / 60
        else:
            delta = 30  # 最後のエントリはデフォルト30分

        key = f"{ce.project}）【{ce.category}】"
        raw_minutes[key] += delta

    # 0.5h単位に丸める
    raw_hours = {k: v / 60 for k, v in raw_minutes.items()}
    rounded = {k: _round_half(v) for k, v in raw_hours.items()}

    # 合計が8.0hになるよう調整
    rounded = _adjust_total(rounded, TOTAL_WORK_HOURS)

    return rounded


def _round_half(hours: float) -> float:
    """0.5h単位に丸める（最小0.5h）。"""
    return max(0.5, math.floor(hours * 2 + 0.5) / 2)


def _adjust_total(hours: dict[str, float], target: float) -> dict[str, float]:
    """合計がtargetになるよう最大項目で調整する。"""
    total = sum(hours.values())
    diff = target - total

    if abs(diff) < 0.01 or not hours:
        return hours

    # 差分を0.5h単位に丸める
    diff_rounded = round(diff * 2) / 2

    if diff_rounded == 0:
        return hours

    # 最も時間の長い項目で調整
    max_key = max(hours, key=hours.get)
    adjusted = dict(hours)
    adjusted[max_key] = max(0.5, adjusted[max_key] + diff_rounded)
    return adjusted
