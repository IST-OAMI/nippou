"""カテゴリ分類モジュール"""

from dataclasses import dataclass
from .log_parser import LogEntry

CATEGORIES = ["MTG", "資料作成", "検証", "開発", "テスト", "環境構築", "調査", "リリース", "レビュー", "その他"]
PROJECTS = ["NOK_インフラ支援", "IST_インフラ対応"]

# アプリ名・キーワードからカテゴリを推測するルール
CATEGORY_RULES: list[tuple[list[str], str]] = [
    (["Zoom", "Teams", "Meet", "Slack huddle", "MTG", "ミーティング", "会議"], "MTG"),
    (["Keynote", "PowerPoint", "Slides", "資料", "ドキュメント", "Confluence"], "資料作成"),
    (["Terraform", "検証", "verify", "validation"], "検証"),
    (["VSCode", "Visual Studio Code", "IntelliJ", "vim", "コード", "実装", "開発"], "開発"),
    (["test", "テスト", "pytest", "Jest"], "テスト"),
    (["Docker", "AWS", "Azure", "GCP", "環境構築", "セットアップ"], "環境構築"),
    (["Chrome", "Safari", "Firefox", "ブラウザ", "調査", "検索"], "調査"),
    (["リリース", "deploy", "デプロイ"], "リリース"),
    (["PR", "Pull Request", "レビュー", "review", "GitHub"], "レビュー"),
]

# プロジェクト判定キーワード
PROJECT_RULES: list[tuple[list[str], str]] = [
    (["NOK", "nok"], "NOK_インフラ支援"),
    (["IST", "ist"], "IST_インフラ対応"),
]


@dataclass
class CategorizedEntry:
    entry: LogEntry
    category: str
    project: str


def categorize(entry: LogEntry) -> CategorizedEntry:
    """ログエントリにカテゴリとプロジェクトを割り当てる。"""
    text = f"{entry.app} {entry.title} {entry.summary}"
    category = _match_category(text)
    project = _match_project(text)
    return CategorizedEntry(entry=entry, category=category, project=project)


def categorize_all(entries: list[LogEntry]) -> list[CategorizedEntry]:
    """全エントリを分類する。"""
    return [categorize(e) for e in entries]


def _match_category(text: str) -> str:
    """テキストからカテゴリを推測する。"""
    text_lower = text.lower()
    for keywords, category in CATEGORY_RULES:
        if any(kw.lower() in text_lower for kw in keywords):
            return category
    return "その他"


def _match_project(text: str) -> str:
    """テキストからプロジェクトを推測する。"""
    text_lower = text.lower()
    for keywords, project in PROJECT_RULES:
        if any(kw.lower() in text_lower for kw in keywords):
            return project
    return PROJECTS[0]  # デフォルトはNOK
