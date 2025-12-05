---
name: cc-skill-agent-guide
description: Claude Code のスキルとサブエージェントを作成・設定するためのガイド。「スキルを作りたい」「サブエージェントを作りたい」「Claude Code をカスタマイズしたい」「CLAUDE.md を書きたい」「エージェントが発動しない」で使用。
---

# Claude Code スキル・サブエージェント作成ガイド

スキルとサブエージェントを **確実に発動させる** ための実践ガイド。

## 核心: LLM はステートレス

LLM は毎セッションの開始時にコードベースについて **何も知らない**。CLAUDE.md は毎セッションで注入される唯一のファイルであり、最もレバレッジの高いポイント。

## CLAUDE.md の目的

CLAUDE.md は Claude をコードベースに **オンボード** するためのもの:

- **WHAT**: 技術スタック、プロジェクト構造、ディレクトリマップ
- **WHY**: プロジェクトの目的、各部分の役割
- **HOW**: ビルド方法、テスト実行方法、検証方法

## 発動率を上げる3つの方法

1. **CLAUDE.md に起動条件を明記** → 発動率 100%（最も確実）
2. **description に具体的なトリガー例を列挙** → 発動率向上
3. **Skill ツールの権限許可** → スキルの前提条件

## 推奨構成

```
CLAUDE.md                    # 起動条件・全体ルール
.claude/
├── settings.json            # 権限設定
├── agents/
│   └── {name}.md            # サブエージェント定義
└── skills/
    └── {name}/SKILL.md      # 共有知識（オプション）
```

## クイックスタート

### スキルを作る

1. `.claude/skills/{skill-name}/SKILL.md` を作成
2. `.claude/settings.json` で `"Skill(*)"` を許可
3. CLAUDE.md に起動条件を追記

詳細 → [references/skill-setup.md](references/skill-setup.md)

### サブエージェントを作る

1. `.claude/agents/{agent-name}.md` を作成
2. CLAUDE.md に起動条件を追記

詳細 → [references/agent-setup.md](references/agent-setup.md)

### CLAUDE.md で確実に発動させる

```markdown
## {agent-name} エージェント

以下のいずれかで **必ず** Task ツールで `{agent-name}` を使用：

- 「〇〇して」（例: 「行数を数えて」）
- 「△△したい」（例: 「カウントしたい」）
```

パターン集 → [references/claude-md-patterns.md](references/claude-md-patterns.md)

## 機能比較

| 機能 | 自動適用 | 用途 |
|------|---------|------|
| CLAUDE.md | ✅ 常に | ルール・起動条件 |
| サブエージェント | ❌ 条件付き | 特定タスク実行 |
| スキル | ❌ 条件付き | 共有知識ベース |

## よくある問題

### CLAUDE.md が無視される

**原因**: Claude Code は以下のシステムリマインダーを注入している:

> "IMPORTANT: this context may or may not be relevant to your tasks"

普遍的でない指示が多いと Claude は無視する。

**解決**: 
- 普遍的に適用可能な内容のみ記載
- タスク固有の指示は別ファイルに分離（Progressive Disclosure）
- 300 行未満を目標、短いほど良い

詳細 → [references/claude-md-best-practices.md](references/claude-md-best-practices.md)

### スキルが発火しない

**原因**: Skill ツールがデフォルトでブロック

**解決**: `.claude/settings.json` に追加

```json
{
  "permissions": {
    "allow": ["Skill(*)"]
  }
}
```

### サブエージェントの発動率が低い

**原因**: description マッチングに依存（約 25%）

**解決**: CLAUDE.md に起動条件を明記 → 発動率 100%

## References

詳細ガイド:
- [references/claude-md-best-practices.md](references/claude-md-best-practices.md) - CLAUDE.md ベストプラクティス
- [references/claude-md-patterns.md](references/claude-md-patterns.md) - CLAUDE.md パターン集
- [references/skill-setup.md](references/skill-setup.md) - スキル設定詳細
- [references/agent-setup.md](references/agent-setup.md) - サブエージェント設定詳細

## Assets

テンプレートファイル:
- [assets/skill-template.md](assets/skill-template.md) - スキル用
- [assets/agent-template.md](assets/agent-template.md) - サブエージェント用
- [assets/claude-md-template.md](assets/claude-md-template.md) - CLAUDE.md 用（WHAT/WHY/HOW 構造）
