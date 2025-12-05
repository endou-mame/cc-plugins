# cc-plugins

Claude Code の拡張機能作成を支援するプラグイン集。

## インストール方法

### 1. マーケットプレイスを追加

```
/plugin marketplace add endou-mame/cc-plugins
```

### 2. プラグインをインストール

```
/plugin install cc-helper@cc-plugins
```

## 含まれるプラグイン

### cc-helper

CLAUDE.md、Skills、Sub Agent の作成を支援するスキル。

以下の場合に使用:

1. CLAUDE.md ファイルの作成・改善
2. Skills の構造設計（SKILL.md、scripts/、references/、assets/）
3. Sub Agent の発動率最適化
4. CLAUDE.md/Skills/Sub Agent の関係性理解
5. スキルやエージェントが発動しない問題のデバッグ

### cc-skill-agent-guide

このスキルは以下のトピックをカバーします:

- **スキルの作成方法**: SKILL.md のフォーマット、権限設定
- **サブエージェントの作成方法**: agents/ ディレクトリの構成
- **CLAUDE.md のベストプラクティス**: WHAT/WHY/HOW 構造、Progressive Disclosure
- **発動率を上げる方法**: description の書き方、起動条件の明記

## 使用方法

スキルをインストール後、以下のようなプロンプトで呼び出せます:

- 「CLAUDE.md を作成したい」
- 「スキルを作りたい」
- 「エージェントの発動率を上げたい」
- 「スキルが発動しない」

## 主な内容

### CLAUDE.md ガイド

- WHAT/WHY/HOW フレームワーク
- トークン予算（150-200 命令、300 行以下）
- Progressive Disclosure パターン
- エージェント起動条件の記述方法

### Skill 構造ガイド

- SKILL.md の書き方
- description 最適化（トリガーメカニズム）
- バンドルリソースの使い分け（scripts/、references/、assets/）

### Sub Agent ガイド

- エージェントファイル形式
- 発動率最適化テクニック（約 25% → 100%）
- CLAUDE.md との連携

### 発動メカニズム

- 各コンポーネントの発動条件
- デバッグ方法
- 最適化戦略

## 注意事項

Skill ツールを使用するには、settings.json で許可が必要な場合があります:

```json
{
  "permissions": {
    "allow": ["Skill(*)"]
  }
}
```

## ライセンス

MIT
