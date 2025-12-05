---
description: プロジェクトを分析し、最適な Claude Code 設定（CLAUDE.md, skills, agents, hooks, commands）を自動生成
argument-hint: "[path/to/project]"
---

# Claude Code 設定生成

cc-builder スキルを使用してプロジェクトを分析し、最適な Claude Code 設定を生成する。

## 実行方法

1. cc-builder スキルを呼び出す:
   - `skill: "cc-builder:cc-builder"`

2. スキル指示に従い、以下の順序で処理を実行:
   - プロジェクト分析（analyze-project.py）
   - 生成判断
   - 設定ファイル生成
   - 検証（validate-output.py）
   - 完了報告

## 対象パス

- 引数でパスが指定された場合: 指定されたパスを対象とする
- 引数がない場合: 現在の作業ディレクトリを対象とする

## 生成物

条件に応じて以下を生成する。

| 生成物 | 条件 | 生成先 |
|-------|------|-------|
| CLAUDE.md | 常に | プロジェクトルート |
| code-explorer エージェント | 常に | .claude/agents/ |
| /feature コマンド | 常に | .claude/commands/ |
| hooks.json | lint/format コマンドあり | .claude/ |
| code-reviewer エージェント | テストあり | .claude/agents/ |
| /test コマンド | テストフレームワークあり | .claude/commands/ |
| /review コマンド | Git リポジトリ | .claude/commands/ |
| settings.json | 常に | .claude/ |

## 注意事項

- 既存の CLAUDE.md がある場合は、上書き前に確認を求めること
- カスタマイズ済みの設定がある場合は、マージ方針をユーザーに確認すること
