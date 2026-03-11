"""日報生成モジュール"""

from datetime import datetime
from pathlib import Path
from .categorizer import CategorizedEntry
from .time_calculator import calculate_hours

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"

WEEKDAYS = ["月", "火", "水", "木", "金", "土", "日"]


def generate_report(
    entries: list[CategorizedEntry],
    activities: list[str],
    learnings: list[str],
    date: datetime | None = None,
) -> Path:
    """日報Markdownを生成してoutput/YYYY-MM-DD.mdに保存する。

    Args:
        entries: 分類済みログエントリ
        activities: やったことリスト（各項目は "タイトル\\n- 詳細1\\n- 詳細2" 形式）
        learnings: 学んだことリスト（同上）
        date: 対象日（デフォルトは今日）
    """
    d = date or datetime.now()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    hours = calculate_hours(entries)
    report = _build_report(d, hours, entries, activities, learnings)

    output_file = OUTPUT_DIR / f"{d.strftime('%Y-%m-%d')}.md"
    output_file.write_text(report, encoding="utf-8")
    return output_file


def _build_report(
    date: datetime,
    hours: dict[str, float],
    entries: list[CategorizedEntry],
    activities: list[str],
    learnings: list[str],
) -> str:
    weekday = WEEKDAYS[date.weekday()]
    date_str = f"{date.month:02d}.{date.day:02d}（{weekday}）"

    # 作業実績行
    work_lines = []
    for key, h in hours.items():
        # keyは "NOK_インフラ支援）【MTG】" 形式
        # 同カテゴリのエントリからサマリーを集約
        summaries = _collect_summaries(entries, key)
        summary_text = "、".join(summaries) if summaries else ""
        work_lines.append(f"{key} {summary_text} {h:.1f}h")

    work_section = "\n".join(work_lines)

    # やったこと
    activities_section = _build_numbered_list(activities)

    # 学んだこと
    learnings_section = _build_numbered_list(learnings)

    return f"""
【今日の作業実績】
{date_str} 8.0h+休憩1.0h
{work_section}


【状況報告(所感や現場での人間関係等)】
【「振り返り・気づき」（うまくいった点／いかなかった点とその理由）】
＜所感＞
・
・

＜やったこと＞
{activities_section}


【「学んだこと」（得られた発見・原則・理論化）】
{learnings_section}


【「明日／次に活かす具体策」（実験・アクションプラン）】
・
・

------------------------------------------------------------
【人間関係】
良好です
"""


def _collect_summaries(entries: list[CategorizedEntry], key: str) -> list[str]:
    """指定キーに一致するエントリのサマリーを重複排除で返す。"""
    seen = set()
    result = []
    for ce in entries:
        entry_key = f"{ce.project}）【{ce.category}】"
        if entry_key == key and ce.entry.summary not in seen:
            seen.add(ce.entry.summary)
            result.append(ce.entry.summary)
    return result


def _build_numbered_list(items: list[str]) -> str:
    """番号付きリストを生成する。各項目は改行区切りの詳細を含む。"""
    if not items:
        return "1. \n  - \n  - "

    lines = []
    for i, item in enumerate(items, 1):
        parts = item.split("\n")
        lines.append(f"{i}. {parts[0]}")
        for detail in parts[1:]:
            lines.append(f"  {detail}" if detail.startswith("- ") else f"  - {detail}")
        if len(parts) == 1:
            lines.append("  - ")
            lines.append("  - ")
        lines.append("")
    return "\n".join(lines).rstrip()
