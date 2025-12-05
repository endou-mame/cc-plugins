# スキル設定詳細

## ディレクトリ構造

```
.claude/skills/{skill-name}/
├── SKILL.md          # 必須: メタデータ + 本文
├── scripts/          # 実行可能スクリプト
├── references/       # 参照ドキュメント
└── assets/           # 出力用ファイル（テンプレート等）
```

## SKILL.md フォーマット

```yaml
---
name: my-skill           # 小文字・数字・ハイフンのみ、64文字以内
description: 説明文       # 1024文字以内、トリガー条件を含める
allowed-tools: Read, Bash # オプション: 使用可能ツールの制限
---

# 本文（Markdown）

ここに知識・手順を記述
```

## 権限設定（必須）

`.claude/settings.json`:

```json
{
  "permissions": {
    "allow": ["Skill(*)"]
  }
}
```

**注意**: `allowed-tools` は権限を **制限** するもの。権限の **付与** は settings.json で行う。

## description の書き方

悪い例:
```yaml
description: このプロジェクトの技術スタック
```

良い例:
```yaml
description: コードを書く時、ライブラリを選ぶ時に参照する技術スタック情報。「API呼び出し」「HTTPクライアント」「テストフレームワーク」で使用。
```

ポイント:
- 具体的なトリガーワードを含める
- 使用シーンを明記
- 「〇〇するとき」という条件を書く

## スキルの用途

スキルは **共有知識ベース** として最も効果的:

```
.claude/skills/domain-knowledge/SKILL.md  # 共有知識
.claude/agents/
├── code-generator.md      # ← 参照可能
├── code-reviewer.md       # ← 参照可能
└── test-writer.md         # ← 参照可能
```

サブエージェントから `Skill` または `Read` + `Glob` でアクセス可能。

## 発動確認

```bash
# スキルが認識されているか確認
claude -p "test" --output-format json | jq '.[] | select(.type == "system") | .skills'

# 権限拒否されていないか確認
claude -p "..." --output-format json | jq '.[] | select(.type == "result") | .permission_denials'
```
