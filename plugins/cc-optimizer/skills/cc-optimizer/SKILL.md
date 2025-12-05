---
name: cc-optimizer
description: プロジェクト構造を分析し CLAUDE.md、skills、hooks、agents、commands を自動生成するスキル。「Claude 設定を生成」「CLAUDE.md を作成」「プロジェクトを初期化」「Claude をセットアップ」と言われた場合に使用。既存設定がある場合は「Claude 設定を更新」「再解析」で最新化。
---

# CC Optimizer

プロジェクト構造を分析し、最適な Claude Code 設定を自動生成する。

## ワークフロー

### 1. プロジェクト分析

`scripts/analyze-project.py` を実行してプロジェクト情報を取得:

```bash
python3 {SKILL_PATH}/scripts/analyze-project.py {PROJECT_PATH}
```

出力される JSON:
- projectName: プロジェクト名
- purpose: プロジェクト目的
- languages: 使用言語
- frameworks: フレームワーク
- commands: ビルド/テスト/リントコマンド
- directories: ディレクトリ構造
- existingClaudeConfig: 既存設定

### 2. 生成判断

分析結果から生成する設定を決定:

| 条件 | 生成物 |
|-----|-------|
| 常に | CLAUDE.md, code-explorer エージェント, /feature コマンド |
| lint/format コマンドあり | hooks.json（Stop hook） |
| テストあり | code-reviewer エージェント, /test コマンド |
| Git リポジトリ | /review コマンド |

### 3. 設定生成

#### CLAUDE.md 生成

[references/claude-md-patterns.md](references/claude-md-patterns.md) のパターンに従い生成。

原則:
- 60 行以下を目標
- WHAT/WHY/HOW 構造
- エージェント起動条件を必ず含める

テンプレート: `assets/templates/claude-md.template.md`

#### エージェント生成

[references/agent-patterns.md](references/agent-patterns.md) のパターンに従い生成。

常に生成:
- code-explorer: コードベース探索

条件付き生成:
- code-reviewer: テストがある場合
- test-generator: テストフレームワークがある場合

テンプレート: `assets/templates/agent.template.md`

生成先: `{PROJECT_PATH}/.claude/agents/`

#### Hooks 生成

[references/hook-patterns.md](references/hook-patterns.md) のパターンに従い生成。

lint/format コマンドがある場合、Stop hook を生成。

テンプレート: `assets/templates/hook.template.json`

生成先: `{PROJECT_PATH}/.claude/hooks.json`

#### コマンド生成

[references/command-patterns.md](references/command-patterns.md) のパターンに従い生成。

常に生成:
- /feature: 機能開発

条件付き生成:
- /fix: テストがある場合
- /review: Git リポジトリの場合
- /test: テストフレームワークがある場合

テンプレート: `assets/templates/command.template.md`

生成先: `{PROJECT_PATH}/.claude/commands/`

#### settings.json 生成

Skill 権限を許可する設定を生成:

```json
{
  "permissions": {
    "allow": ["Skill(*)"]
  }
}
```

テンプレート: `assets/templates/settings.template.json`

生成先: `{PROJECT_PATH}/.claude/settings.json`

### 4. 検証

`scripts/validate-output.py` を実行して生成結果を検証:

```bash
python3 {SKILL_PATH}/scripts/validate-output.py {PROJECT_PATH}
```

検証項目:
- CLAUDE.md の行数（300 行未満）
- スキルの frontmatter
- エージェントの必須フィールド
- hooks.json の構造

### 5. 完了報告

生成したファイル一覧と次のステップを報告:

```
生成完了:
- CLAUDE.md
- .claude/agents/code-explorer.md
- .claude/hooks.json
- .claude/commands/feature.md
- .claude/settings.json

次のステップ:
1. CLAUDE.md を確認し、プロジェクト目的を必要に応じて編集
2. Claude Code を再起動して設定を反映
```

## 更新モード

既存設定がある場合（existingClaudeConfig.hasCLAUDEmd = true）:

1. 既存 CLAUDE.md を読み込み
2. 現在のプロジェクト状態と比較
3. 差分を特定（新しいフレームワーク、コマンド変更など）
4. 既存のカスタマイズを保持しつつ更新を提案
5. ユーザー確認後、マージして更新

## References

生成パターンの詳細:

- [references/claude-md-patterns.md](references/claude-md-patterns.md) - CLAUDE.md のベストプラクティス
- [references/skill-patterns.md](references/skill-patterns.md) - スキル生成パターン
- [references/agent-patterns.md](references/agent-patterns.md) - エージェント生成パターン
- [references/hook-patterns.md](references/hook-patterns.md) - Hook 生成パターン
- [references/command-patterns.md](references/command-patterns.md) - コマンド生成パターン
- [references/tech-stack-detection.md](references/tech-stack-detection.md) - 技術スタック検出ロジック
