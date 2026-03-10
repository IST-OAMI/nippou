# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

日報を自動生成するPythonプロジェクト。スクリーンショットとアクティブウィンドウ情報をClaude Codeで分析し、テンプレートに沿った日報Markdownを出力する。

## アーキテクチャ

### スキル構成

- **`/screenshot-log`**: `/loop 5m` で定期実行。スクショ撮影→ウィンドウタイトル取得→CC分析→ログ追記→スクショ削除
- **`/nippou`**: 終業時に手動実行。当日ログから日報を自動生成

### データフロー

```
screencapture + osascript(ウィンドウタイトル)
  → CCが分析・テキスト化
  → logs/YYYY-MM-DD.md に追記
  → /nippou で output/YYYY-MM-DD.md に日報生成
```

### 日報の自動生成箇所

- **【今日の作業実績】**: カテゴリ自動分類 + 0.5h単位の時間算出
- **＜やったこと＞**: 作業内容の詳細
- **【学んだこと】**: ログから学びを抽象化

### 手動記入箇所

- ＜所感＞
- 【明日／次に活かす具体策】
- 【人間関係】

### プロジェクト判定

スクショ内容とウィンドウタイトルから `NOK_インフラ支援` / `IST_インフラ対応` を推測

## ファイル構成

- `template.md` - 日報テンプレート
- `category.md` - プロジェクト別カテゴリ定義
- `logs/YYYY-MM-DD.md` - 日次作業ログ（スクショ分析結果の蓄積）
- `output/YYYY-MM-DD.md` - 生成された日報
